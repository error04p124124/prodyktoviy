# 🚀 Развертывание на продакшн сервере

## Подготовка к развертыванию

### 1. Обновление settings.py для продакшн

Создайте файл `grocery_store/settings_prod.py`:

```python
from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'your-ip-address']

# Безопасность
SECRET_KEY = 'your-super-secret-key-here-generate-new-one'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# База данных PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'grocery_store_db',
        'USER': 'postgres_user',
        'PASSWORD': 'strong_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Redis для Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Статические и медиа файлы
STATIC_ROOT = '/var/www/grocery_store/static/'
MEDIA_ROOT = '/var/www/grocery_store/media/'

# Email (для уведомлений)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### 2. Установка зависимостей для продакшн

Обновите `requirements.txt`:

```
Django==4.2.7
Pillow==10.1.0
channels==4.0.0
channels-redis==4.1.0
django-crispy-forms==2.1
crispy-bootstrap5==0.7
daphne==4.0.0
redis==5.0.1
psycopg2-binary==2.9.9
gunicorn==21.2.0
whitenoise==6.6.0
```

## Установка на Ubuntu Server

### 1. Установка системных пакетов

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y redis-server
sudo apt install -y nginx
```

### 2. Настройка PostgreSQL

```bash
# Вход в PostgreSQL
sudo -u postgres psql

# Создание базы данных и пользователя
CREATE DATABASE grocery_store_db;
CREATE USER grocery_user WITH PASSWORD 'your_password';
ALTER ROLE grocery_user SET client_encoding TO 'utf8';
ALTER ROLE grocery_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE grocery_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE grocery_store_db TO grocery_user;
\q
```

### 3. Настройка Redis

```bash
sudo systemctl start redis
sudo systemctl enable redis
```

### 4. Клонирование и настройка проекта

```bash
# Создание директории
sudo mkdir -p /var/www/grocery_store
sudo chown $USER:$USER /var/www/grocery_store
cd /var/www/grocery_store

# Копирование файлов проекта
# (используйте git clone или scp для загрузки файлов)

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate --settings=grocery_store.settings_prod

# Сбор статических файлов
python manage.py collectstatic --settings=grocery_store.settings_prod --noinput

# Создание суперпользователя
python manage.py createsuperuser --settings=grocery_store.settings_prod
```

### 5. Настройка Gunicorn

Создайте файл `/etc/systemd/system/grocery_store.service`:

```ini
[Unit]
Description=Grocery Store Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/grocery_store
Environment="DJANGO_SETTINGS_MODULE=grocery_store.settings_prod"
ExecStart=/var/www/grocery_store/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/grocery_store/grocery_store.sock \
    grocery_store.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 6. Настройка Daphne для WebSocket

Создайте файл `/etc/systemd/system/grocery_store_daphne.service`:

```ini
[Unit]
Description=Grocery Store Daphne WebSocket
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/grocery_store
Environment="DJANGO_SETTINGS_MODULE=grocery_store.settings_prod"
ExecStart=/var/www/grocery_store/venv/bin/daphne \
    -b 0.0.0.0 \
    -p 8001 \
    grocery_store.asgi:application

[Install]
WantedBy=multi-user.target
```

### 7. Настройка Nginx

Создайте файл `/etc/nginx/sites-available/grocery_store`:

```nginx
upstream grocery_store_server {
    server unix:/var/www/grocery_store/grocery_store.sock fail_timeout=0;
}

upstream grocery_store_websocket {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/grocery_store/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/grocery_store/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    location /ws/ {
        proxy_pass http://grocery_store_websocket;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://grocery_store_server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Активируйте конфигурацию:

```bash
sudo ln -s /etc/nginx/sites-available/grocery_store /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Настройка SSL (Let's Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 9. Запуск сервисов

```bash
# Запуск Gunicorn
sudo systemctl start grocery_store
sudo systemctl enable grocery_store

# Запуск Daphne
sudo systemctl start grocery_store_daphne
sudo systemctl enable grocery_store_daphne

# Проверка статуса
sudo systemctl status grocery_store
sudo systemctl status grocery_store_daphne
```

## Настройка резервного копирования

### Скрипт резервного копирования

Создайте файл `/var/www/grocery_store/backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/grocery_store"
DATE=$(date +%Y%m%d_%H%M%S)

# Создание директории для бэкапов
mkdir -p $BACKUP_DIR

# Бэкап базы данных
pg_dump -U grocery_user grocery_store_db > $BACKUP_DIR/db_$DATE.sql

# Бэкап медиа файлов
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C /var/www/grocery_store media/

# Удаление старых бэкапов (старше 30 дней)
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
```

Сделайте скрипт исполняемым:

```bash
chmod +x /var/www/grocery_store/backup.sh
```

Добавьте в crontab (каждый день в 2:00):

```bash
sudo crontab -e

# Добавьте строку:
0 2 * * * /var/www/grocery_store/backup.sh
```

## Мониторинг и логи

### Просмотр логов

```bash
# Логи Django
sudo journalctl -u grocery_store -f

# Логи Daphne
sudo journalctl -u grocery_store_daphne -f

# Логи Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Обновление приложения

```bash
cd /var/www/grocery_store
source venv/bin/activate

# Получение обновлений
git pull  # если используете git

# Установка новых зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate --settings=grocery_store.settings_prod

# Сбор статических файлов
python manage.py collectstatic --settings=grocery_store.settings_prod --noinput

# Перезапуск сервисов
sudo systemctl restart grocery_store
sudo systemctl restart grocery_store_daphne
```

## Оптимизация производительности

### 1. Кэширование (Redis)

В `settings_prod.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 2. Компрессия статических файлов

```bash
pip install django-compressor
```

### 3. CDN для статических файлов

Настройте AWS S3 или другой CDN для статических файлов.

## Безопасность

### 1. Firewall

```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. Fail2Ban

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Автоматические обновления безопасности

```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## Проверка работоспособности

1. **Откройте браузер:** http://your-domain.com
2. **Проверьте вход в систему**
3. **Проверьте работу чата** (WebSocket)
4. **Проверьте загрузку изображений**
5. **Проверьте графики в отчетах**

## Решение проблем

### Ошибка подключения к базе данных

```bash
sudo systemctl status postgresql
sudo -u postgres psql -c "SELECT 1"
```

### WebSocket не работает

```bash
sudo systemctl status grocery_store_daphne
sudo systemctl status redis
```

### Статические файлы не загружаются

```bash
sudo chown -R www-data:www-data /var/www/grocery_store/static/
sudo chmod -R 755 /var/www/grocery_store/static/
```

---

**Поздравляем! Ваше приложение развернуто на продакшн сервере! 🎉**
