from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import WriteOff, Inventory
from .forms import WriteOffForm, InventoryForm
from products.models import Category, Product
from accounts.models import CustomUser

@login_required
def write_off_list(request):
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для просмотра списаний.')
        return redirect('products:dashboard')
    
    write_offs = WriteOff.objects.all()
    return render(request, 'inventory/write_off_list.html', {'write_offs': write_offs})

@login_required
def write_off_create(request):
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для создания списаний.')
        return redirect('products:dashboard')
    
    categories = Category.objects.all().order_by('name')
    products = Product.objects.select_related('category').all().order_by('name')
    
    if request.method == 'POST':
        form = WriteOffForm(request.POST)
        if form.is_valid():
            write_off = form.save(commit=False)
            write_off.created_by = request.user
            
            # Проверяем наличие товара на складе
            if write_off.product.quantity < write_off.quantity:
                messages.error(request, f'Недостаточно товара на складе! Доступно: {write_off.product.quantity} {write_off.product.unit}')
                return render(request, 'inventory/write_off_form.html', {
                    'form': form,
                    'categories': categories,
                    'products': products
                })
            
            write_off.save()
            messages.success(request, 'Списание успешно зарегистрировано!')
            return redirect('inventory:write_off_list')
    else:
        form = WriteOffForm()
    
    return render(request, 'inventory/write_off_form.html', {
        'form': form,
        'categories': categories,
        'products': products
    })

@login_required
def inventory_list(request):
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для просмотра инвентаризаций.')
        return redirect('products:dashboard')
    
    from django.db.models import Count, Sum, Min, Max
    from collections import defaultdict
    
    # Группируем инвентаризации только по session_id
    inventory_sessions = Inventory.objects.values('session_id').annotate(
        products_count=Count('id'),
        total_expected=Sum('expected_quantity'),
        total_actual=Sum('actual_quantity'),
        total_difference=Sum('difference'),
        first_date=Min('inventory_date')
    ).order_by('-first_date')
    
    # Получаем категории и проводившего для каждой сессии
    sessions_data = []
    for session in inventory_sessions:
        items = Inventory.objects.filter(session_id=session['session_id']).select_related('product__category', 'conducted_by')
        categories = set(item.product.category.name for item in items)
        session['categories'] = ', '.join(sorted(categories))
        # Берем проводившего из первой записи
        first_item = items.first()
        session['conducted_by__first_name'] = first_item.conducted_by.first_name if first_item and first_item.conducted_by else ''
        session['conducted_by__last_name'] = first_item.conducted_by.last_name if first_item and first_item.conducted_by else ''
        sessions_data.append(session)
    
    return render(request, 'inventory/inventory_list.html', {'inventory_sessions': sessions_data})

@login_required
def inventory_create(request):
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для создания инвентаризаций.')
        return redirect('products:dashboard')
    
    categories = Category.objects.all().order_by('name')
    products = Product.objects.select_related('category').all().order_by('name')
    
    if request.method == 'POST':
        try:
            import json
            # Получаем данные из формы
            items_data = json.loads(request.POST.get('items_data', '[]'))
            
            if not items_data:
                messages.error(request, 'Добавьте хотя бы один товар для инвентаризации!')
                return render(request, 'inventory/inventory_form.html', {
                    'categories': categories,
                    'products': products
                })
            
            # Используем дату как session_id - все инвентаризации в один день объединяются
            from datetime import date
            session_id = date.today().strftime('%Y-%m-%d')
            
            # Создаем записи инвентаризации для каждого товара
            inventory_count = 0
            for item in items_data:
                product = Product.objects.get(id=item['product_id'])
                Inventory.objects.create(
                    session_id=session_id,
                    product=product,
                    expected_quantity=float(item['expected_quantity']),
                    actual_quantity=float(item['actual_quantity']),
                    conducted_by=request.user
                )
                inventory_count += 1
            
            messages.success(request, f'Инвентаризация успешно проведена! Проверено товаров: {inventory_count}')
            return redirect('inventory:inventory_list')
            
        except Exception as e:
            messages.error(request, f'Ошибка при проведении инвентаризации: {str(e)}')
            return render(request, 'inventory/inventory_form.html', {
                'categories': categories,
                'products': products
            })
    else:
        return render(request, 'inventory/inventory_form.html', {
            'categories': categories,
            'products': products
        })


@login_required
def print_inventory_report(request, session_id):
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для просмотра отчетов.')
        return redirect('products:dashboard')
    
    # Получаем все записи инвентаризации для данной сессии
    inventory_items = Inventory.objects.filter(session_id=session_id).select_related('product__category', 'conducted_by')
    
    if not inventory_items.exists():
        messages.error(request, 'Инвентаризация не найдена.')
        return redirect('inventory:inventory_list')
    
    # Группируем товары по категориям
    from collections import defaultdict
    categories_data = defaultdict(list)
    
    first_item = inventory_items.first()
    
    for item in inventory_items:
        categories_data[item.product.category.name].append({
            'product': item.product.name,
            'unit': item.product.unit,
            'expected': item.expected_quantity,
            'actual': item.actual_quantity,
            'difference': item.difference
        })
    
    # Рассчитываем итоги
    total_expected = sum(item.expected_quantity for item in inventory_items)
    total_actual = sum(item.actual_quantity for item in inventory_items)
    total_difference = sum(item.difference for item in inventory_items)
    
    context = {
        'session_id': session_id,
        'inventory_date': first_item.inventory_date,
        'conducted_by': first_item.conducted_by,
        'categories_data': dict(categories_data),
        'total_items': inventory_items.count(),
        'total_expected': total_expected,
        'total_actual': total_actual,
        'total_difference': total_difference,
    }
    
    return render(request, 'inventory/inventory_report.html', context)


@login_required
def send_inventory_email(request, session_id):
    """Отправляет детальный отчет об инвентаризации на email заведующего"""
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для отправки отчетов.')
        return redirect('products:dashboard')
    
    # Получаем все записи инвентаризации для данной сессии
    inventory_items = Inventory.objects.filter(session_id=session_id).select_related('product__category', 'conducted_by')
    
    if not inventory_items.exists():
        messages.error(request, 'Инвентаризация не найдена.')
        return redirect('inventory:inventory_list')
    
    # Получаем email заведующих и директоров
    managers = CustomUser.objects.filter(role='manager')
    directors = CustomUser.objects.filter(role='director')
    recipients = list(managers.values_list('email', flat=True)) + list(directors.values_list('email', flat=True))
    recipients = [email for email in recipients if email]
    
    if not recipients:
        messages.error(request, 'Не найдены email адреса заведующих для отправки.')
        return redirect('inventory:inventory_list')
    
    # Подготовка данных
    from collections import defaultdict
    categories_data = defaultdict(list)
    first_item = inventory_items.first()
    
    for item in inventory_items:
        categories_data[item.product.category.name].append({
            'product': item.product.name,
            'unit': item.product.unit,
            'expected': item.expected_quantity,
            'actual': item.actual_quantity,
            'difference': item.difference
        })
    
    # Рассчитываем итоги
    total_expected = sum(item.expected_quantity for item in inventory_items)
    total_actual = sum(item.actual_quantity for item in inventory_items)
    total_difference = sum(item.difference for item in inventory_items)
    
    # Формируем текст письма
    conductor_name = f"{first_item.conducted_by.first_name} {first_item.conducted_by.last_name}" if first_item.conducted_by else "Неизвестно"
    
    message_body = f'''
ОТЧЕТ ОБ ИНВЕНТАРИЗАЦИИ
{'='*60}

Дата проведения: {first_item.inventory_date.strftime('%d.%m.%Y %H:%M')}
Проводил инвентаризацию: {conductor_name}
Должность: {first_item.conducted_by.get_role_display() if first_item.conducted_by else 'N/A'}
Всего проверено товаров: {inventory_items.count()}

{'='*60}
ДЕТАЛЬНАЯ ИНФОРМАЦИЯ ПО КАТЕГОРИЯМ
{'='*60}

'''
    
    for category_name, items in sorted(categories_data.items()):
        message_body += f"\n📦 КАТЕГОРИЯ: {category_name}\n"
        message_body += "-" * 60 + "\n"
        
        for item in items:
            status_icon = "✅" if item['difference'] == 0 else ("⬆️" if item['difference'] > 0 else "⬇️")
            message_body += f"{status_icon} {item['product']}\n"
            message_body += f"   Ожидалось: {item['expected']} {item['unit']}\n"
            message_body += f"   Фактически: {item['actual']} {item['unit']}\n"
            message_body += f"   Разница: {item['difference']:+.2f} {item['unit']}\n\n"
    
    message_body += "=" * 60 + "\n"
    message_body += "ИТОГОВЫЕ ПОКАЗАТЕЛИ\n"
    message_body += "=" * 60 + "\n"
    message_body += f"Общее ожидаемое количество: {total_expected:.2f}\n"
    message_body += f"Общее фактическое количество: {total_actual:.2f}\n"
    message_body += f"Общая разница: {total_difference:+.2f}\n\n"
    
    if total_difference == 0:
        message_body += "✅ Инвентаризация прошла без расхождений!\n"
    elif total_difference > 0:
        message_body += f"⚠️ Обнаружен излишек: +{total_difference:.2f} единиц\n"
    else:
        message_body += f"⚠️ Обнаружена недостача: {total_difference:.2f} единиц\n"
    
    message_body += "\n" + "=" * 60 + "\n"
    message_body += "Система управления продуктовым магазином 'На Просторной'\n"
    message_body += "Это автоматически созданное сообщение, не отвечайте на него.\n"
    
    # Отправка email
    try:
        send_mail(
            subject=f'📋 Отчет об инвентаризации от {first_item.inventory_date.strftime("%d.%m.%Y")}',
            message=message_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        messages.success(request, f'Отчет успешно отправлен на {len(recipients)} адрес(а/ов)!')
    except Exception as e:
        messages.error(request, f'Ошибка при отправке email: {str(e)}')
    
    return redirect('inventory:inventory_list')
