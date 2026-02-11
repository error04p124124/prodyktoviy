# 📁 Структура проекта

```
d:\1\  (grocery_store_project)
│
├── 📂 grocery_store/              # Основной проект Django
│   ├── __init__.py
│   ├── asgi.py                   # Конфигурация ASGI (WebSocket)
│   ├── wsgi.py                   # Конфигурация WSGI
│   ├── settings.py               # Настройки проекта
│   └── urls.py                   # Главные URL-маршруты
│
├── 📂 accounts/                   # Приложение пользователей
│   ├── models.py                 # CustomUser модель
│   ├── views.py                  # Вход, выход, профиль
│   ├── forms.py                  # Формы регистрации и профиля
│   ├── urls.py                   # URL-маршруты
│   ├── admin.py                  # Настройки админки
│   └── apps.py
│
├── 📂 products/                   # Приложение товаров
│   ├── models.py                 # Product, Category, Supply, PriceHistory
│   ├── views.py                  # CRUD товаров, поставки, цены
│   ├── forms.py                  # Формы товаров и поставок
│   ├── urls.py                   # URL-маршруты
│   ├── admin.py                  # Настройки админки
│   ├── apps.py
│   └── 📂 management/
│       └── 📂 commands/
│           └── setup_initial_data.py  # Команда создания категорий
│
├── 📂 sales/                      # Приложение продаж
│   ├── models.py                 # Sale модель
│   ├── views.py                  # Регистрация продаж, история
│   ├── forms.py                  # Форма продажи
│   ├── urls.py                   # URL-маршруты
│   ├── admin.py                  # Настройки админки
│   └── apps.py
│
├── 📂 inventory/                  # Приложение инвентаризации
│   ├── models.py                 # WriteOff, Inventory модели
│   ├── views.py                  # Списания, инвентаризации
│   ├── forms.py                  # Формы списаний и инвентаризаций
│   ├── urls.py                   # URL-маршруты
│   ├── admin.py                  # Настройки админки
│   └── apps.py
│
├── 📂 chat/                       # Приложение чата
│   ├── models.py                 # ChatMessage модель
│   ├── views.py                  # Отображение чата
│   ├── consumers.py              # WebSocket consumer
│   ├── routing.py                # WebSocket маршруты
│   ├── urls.py                   # URL-маршруты
│   ├── admin.py                  # Настройки админки
│   └── apps.py
│
├── 📂 reports/                    # Приложение отчетов
│   ├── models.py                 # (пустой - отчеты из других моделей)
│   ├── views.py                  # API для графиков и статистики
│   ├── urls.py                   # URL-маршруты
│   ├── admin.py
│   └── apps.py
│
├── 📂 templates/                  # HTML-шаблоны
│   ├── base.html                 # Базовый шаблон
│   │
│   ├── 📂 accounts/
│   │   ├── login.html           # Страница входа
│   │   └── profile.html         # Страница профиля
│   │
│   ├── 📂 products/
│   │   ├── dashboard.html       # Главная страница
│   │   ├── product_list.html    # Каталог товаров
│   │   ├── product_detail.html  # Карточка товара
│   │   ├── product_form.html    # Форма товара
│   │   ├── price_update.html    # Обновление цены
│   │   ├── supply_list.html     # Список поставок
│   │   └── supply_form.html     # Форма поставки
│   │
│   ├── 📂 sales/
│   │   ├── sale_list.html       # История продаж
│   │   ├── sale_form.html       # Форма продажи
│   │   └── sale_detail.html     # Детали продажи
│   │
│   ├── 📂 inventory/
│   │   ├── write_off_list.html  # Список списаний
│   │   ├── write_off_form.html  # Форма списания
│   │   ├── inventory_list.html  # Список инвентаризаций
│   │   └── inventory_form.html  # Форма инвентаризации
│   │
│   ├── 📂 chat/
│   │   └── chat.html            # Чат сотрудников
│   │
│   └── 📂 reports/
│       └── dashboard.html        # Отчеты и графики
│
├── 📂 static/                     # Статические файлы (будут CDN в prod)
│   ├── 📂 css/                   # (используется CDN Bootstrap)
│   ├── 📂 js/                    # (используется CDN jQuery, Chart.js)
│   └── 📂 images/                # (опционально)
│
├── 📂 media/                      # Загруженные файлы
│   ├── 📂 products/              # Изображения товаров
│   ├── 📂 avatars/               # Аватары пользователей
│   └── 📂 chat_images/           # Изображения из чата
│
├── 📂 staticfiles/                # Собранные статические файлы (prod)
│
├── 📂 venv/                       # Виртуальное окружение (не в git)
│
├── 📄 manage.py                   # Django management скрипт
├── 📄 requirements.txt            # Python зависимости
├── 📄 db.sqlite3                  # База данных SQLite (не в git)
│
├── 📄 .gitignore                  # Игнорируемые файлы Git
│
├── 📄 README.md                   # Основное описание проекта
├── 📄 QUICKSTART.md               # Быстрый старт
├── 📄 FEATURES.md                 # Описание функций
├── 📄 DEPLOYMENT.md               # Руководство по развертыванию
├── 📄 PROJECT_STRUCTURE.md        # Этот файл
│
├── 📄 create_test_data.py         # Скрипт создания тестовых данных
│
├── 📄 start.bat                   # Запуск сервера (Windows)
├── 📄 start.sh                    # Запуск сервера (Linux/Mac)
├── 📄 install.bat                 # Полная установка (Windows)
└── 📄 setup_test_data.bat         # Создание тестовых данных (Windows)
```

## Описание ключевых файлов

### Конфигурационные файлы

#### `grocery_store/settings.py`
Основные настройки Django:
- Установленные приложения
- Middleware
- Настройки базы данных
- Настройки статических и медиа файлов
- Настройки Django Channels
- Языковые настройки (русский)

#### `grocery_store/urls.py`
Главные URL-маршруты:
```python
/                    → редирект на /products/
/admin/              → админ-панель Django
/accounts/           → авторизация и профиль
/products/           → товары и поставки
/sales/              → продажи
/inventory/          → списания и инвентаризация
/chat/               → чат
/reports/            → отчеты
```

#### `grocery_store/asgi.py`
Конфигурация ASGI для WebSocket:
- HTTP маршруты → Django
- WebSocket маршруты → Channels

### Модели данных

#### `accounts/models.py`
```python
CustomUser
  - username, email, password (Django стандарт)
  - role (director/manager/cashier)
  - avatar (ImageField)
  - phone
  - методы: can_manage_products(), can_manage_sales(), can_view_reports()
```

#### `products/models.py`
```python
Category
  - name
  - icon (Font Awesome класс)
  - description

Product
  - name, description
  - category (ForeignKey)
  - image (ImageField)
  - price, quantity, unit
  - expiry_date
  - свойства: is_low_stock, is_expired

PriceHistory
  - product (ForeignKey)
  - old_price, new_price
  - changed_at, changed_by

Supply
  - product (ForeignKey)
  - quantity, price_per_unit, total_cost
  - supplier
  - supply_date, created_by
```

#### `sales/models.py`
```python
Sale
  - product (ForeignKey)
  - quantity, price_per_unit, total_amount
  - sale_date
  - cashier (ForeignKey)
  - автоматически: уменьшает quantity товара
```

#### `inventory/models.py`
```python
WriteOff
  - product (ForeignKey)
  - quantity
  - reason (expired/damaged/quality/other)
  - reason_detail
  - write_off_date, created_by
  - автоматически: уменьшает quantity товара

Inventory
  - product (ForeignKey)
  - expected_quantity, actual_quantity
  - difference (автоматически)
  - inventory_date, conducted_by
  - автоматически: обновляет quantity товара
```

#### `chat/models.py`
```python
ChatMessage
  - sender (ForeignKey to CustomUser)
  - message (текст)
  - image (опционально)
  - timestamp
  - is_read
```

### Views (представления)

#### `products/views.py`
- `dashboard()` - главная страница со статистикой
- `product_list()` - каталог с фильтрами
- `product_detail()` - карточка товара
- `product_create()` - добавление товара
- `product_update()` - редактирование товара
- `supply_list()` - список поставок
- `supply_create()` - регистрация поставки
- `price_update()` - изменение цены

#### `sales/views.py`
- `sale_list()` - история продаж
- `sale_create()` - регистрация продажи
- `sale_detail()` - детали продажи

#### `inventory/views.py`
- `write_off_list()` - список списаний
- `write_off_create()` - списание товара
- `inventory_list()` - список инвентаризаций
- `inventory_create()` - проведение инвентаризации

#### `chat/views.py`
- `chat_view()` - отображение чата
- `get_messages()` - API получения сообщений

#### `reports/views.py`
- `reports_dashboard()` - страница отчетов
- `profit_chart_data()` - API данных графика прибыли
- `top_products_data()` - API данных топ товаров
- `statistics_data()` - API общей статистики

### WebSocket

#### `chat/consumers.py`
```python
ChatConsumer
  - connect() - подключение клиента
  - disconnect() - отключение клиента
  - receive() - получение сообщения
  - chat_message() - отправка сообщения
  - save_message() - сохранение в БД
```

### Шаблоны

Все шаблоны наследуются от `base.html`:
- Единый дизайн
- Навигационное меню
- Отображение сообщений
- Подключение CSS/JS библиотек

### Формы

Формы используют:
- Bootstrap 5 классы для стилей
- Django Crispy Forms для автоматического рендеринга
- Валидация на стороне сервера
- CSRF защита

### Права доступа

Проверка прав в views через методы модели CustomUser:
```python
if not request.user.can_manage_products():
    messages.error(request, 'Нет прав')
    return redirect('products:dashboard')
```

Проверка в шаблонах:
```django
{% if user.can_view_reports %}
    <a href="{% url 'reports:dashboard' %}">Отчеты</a>
{% endif %}
```

## База данных

### Связи между моделями

```
CustomUser (1) ←→ (N) Sale [cashier]
CustomUser (1) ←→ (N) Supply [created_by]
CustomUser (1) ←→ (N) WriteOff [created_by]
CustomUser (1) ←→ (N) Inventory [conducted_by]
CustomUser (1) ←→ (N) PriceHistory [changed_by]
CustomUser (1) ←→ (N) ChatMessage [sender]

Category (1) ←→ (N) Product

Product (1) ←→ (N) Sale
Product (1) ←→ (N) Supply
Product (1) ←→ (N) WriteOff
Product (1) ←→ (N) Inventory
Product (1) ←→ (N) PriceHistory
```

## Технологический стек

### Backend
- **Django 4.2** - веб-фреймворк
- **Django Channels** - WebSocket поддержка
- **Pillow** - обработка изображений
- **Crispy Forms** - красивые формы

### Frontend
- **Bootstrap 5** - CSS фреймворк
- **jQuery** - JavaScript библиотека
- **Chart.js** - графики
- **Font Awesome** - иконки
- **Animate.css** - анимации

### База данных
- **SQLite** - для разработки
- **PostgreSQL** - для продакшн

### Real-time
- **Redis** - для Channels (продакшн)
- **In-Memory** - для разработки

## Файловая система

### Загружаемые файлы

```
media/
  products/          # Изображения товаров
    ├── product1.jpg
    ├── product2.png
    └── ...
  
  avatars/           # Аватары пользователей
    ├── user1.jpg
    ├── user2.png
    └── ...
  
  chat_images/       # Изображения из чата
    ├── image1.jpg
    └── ...
```

### Статические файлы (разработка)

Используются CDN:
- Bootstrap CSS/JS
- jQuery
- Chart.js
- Font Awesome
- Animate.css

### Статические файлы (продакшн)

```
staticfiles/        # Собранные collectstatic
  admin/           # Django admin статика
  css/             # Кастомные стили
  js/              # Кастомные скрипты
```

## API Endpoints

### Chat API
- `GET /chat/api/messages/` - получить сообщения
- `WS /ws/chat/` - WebSocket соединение

### Reports API
- `GET /reports/api/profit-chart/?period=week` - данные графика прибыли
- `GET /reports/api/top-products/?period=month` - топ товары
- `GET /reports/api/statistics/` - общая статистика

## Команды управления

```bash
# Стандартные Django команды
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# Кастомные команды
python manage.py setup_initial_data    # Создать категории
python manage.py shell < create_test_data.py  # Тестовые данные
```

---

**Структура проекта разработана для легкой навигации и расширения! 📁**
