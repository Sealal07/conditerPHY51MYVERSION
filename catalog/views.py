from django.shortcuts import render, get_object_or_404  # Отрисовка шаблонов и получение объекта или 404
from django.db.models import Sum, Count  # Агрегатные функции БД
from .models import Category, Product  # Наши модели
from .forms import ProductSearchForm  # Форма поиска

def home_view(request):  # Главная страница
    form = ProductSearchForm(request.GET or None) # Инициализация формы поиска данными из URL

    # Популярные товары — берем топ-5, сортируя по сумме заказанных единиц
    popular_products = Product.objects.filter(
        is_active=True
    ).annotate(
        total_ordered=Sum('orderitem__quantity') # Считаем сумму через связь в OrderItem
    ).order_by('-total_ordered')[:5]

    # Если продаж мало и товаров < 5, добавляем в список просто последние новинки
    if popular_products.count() < 5:
        extra = Product.objects.filter(is_active=True).exclude(
            id__in=[p.id for p in popular_products] # Исключаем те, что уже есть в топе
        ).order_by('-created_at')[:5 - popular_products.count()]
        from itertools import chain # Утилита для объединения списков
        popular_products = list(chain(popular_products, extra)) # Склеиваем популярные и новые

    # Акции: товары со скидкой больше 0
    promotions = Product.objects.filter(
        is_active=True,
        discount_percent__gt=0
    ).order_by('-discount_percent') # Сортировка: самая большая скидка первой

    # Список всех активных категорий для навигации
    categories = Category.objects.filter(is_active=True)

    return render(request, 'catalog/home.html', { # Передаем данные в шаблон
        'form': form,
        'popular_products': popular_products,
        'promotions': promotions,
        'categories': categories,
        'breadcrumbs': [ # Хлебные крошки
            {'title': 'Главная', 'url': '/'},
        ],
    })


def category_list_view(request): # Страница со списком всех категорий
    categories = Category.objects.filter(is_active=True)
    return render(request, 'catalog/category_list.html', {
        'categories': categories,
        'breadcrumbs': [
            {'title': 'Главная', 'url': '/'},
            {'title': 'Категории', 'url': ''},
        ],
    })


def category_detail_view(request, slug): # Страница конкретной категории (список товаров в ней)
    category = get_object_or_404(Category, slug=slug, is_active=True) # Ищем категорию или ошибку 404
    products = category.products.filter(is_active=True) # Получаем все товары этой категории
    form = ProductSearchForm(request.GET or None)

    if form.is_valid() and form.cleaned_data.get('q'): # Если в поиске что-то ввели
        q = form.cleaned_data['q']
        products = products.filter(name__icontains=q) # Фильтруем товары по названию (без учета регистра)

    return render(request, 'catalog/product_list.html', {
        'category': category,
        'products': products,
        'form': form,
        'breadcrumbs': [
            {'title': 'Главная', 'url': '/'},
            {'title': 'Категории', 'url': '/catalog/categories/'},
            {'title': category.name, 'url': ''},
        ],
    })


def product_detail_view(request, slug): # Страница одного товара
    product = get_object_or_404(Product, slug=slug, is_active=True)
    # Похожие товары: из той же категории, исключая текущий, лимит 4 шт.
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related,
        'breadcrumbs': [
            {'title': 'Главная', 'url': '/'},
            {'title': 'Категории', 'url': '/catalog/categories/'},
            {'title': product.category.name, 'url': product.category.get_absolute_url()},
            {'title': product.name, 'url': ''},
        ],
    })


def promotions_view(request): # Страница всех акций
    promotions = Product.objects.filter(
        is_active=True, discount_percent__gt=0
    ).order_by('-discount_percent')
    return render(request, 'catalog/promotions.html', {
        'promotions': promotions,
        'breadcrumbs': [
            {'title': 'Главная', 'url': '/'},
            {'title': 'Акции', 'url': ''},
        ],
    })