from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count
from .models import Category, Product
from .forms import ProductSearchForm


def home_view(request):
    form = ProductSearchForm(request.GET or None)

    # Популярные товары — топ-5 по количеству заказов
    popular_products = Product.objects.filter(
        is_active=True
    ).annotate(
        total_ordered=Sum('orderitem__quantity')
    ).order_by('-total_ordered')[:5]

    # Если товаров меньше 5, дополняем просто последними
    if popular_products.count() < 5:
        extra = Product.objects.filter(is_active=True).exclude(
            id__in=[p.id for p in popular_products]
        ).order_by('-created_at')[:5 - popular_products.count()]
        from django.db.models import QuerySet
        from itertools import chain
        popular_products = list(chain(popular_products, extra))

    # Акции
    promotions = Product.objects.filter(
        is_active=True,
        discount_percent__gt=0
    ).order_by('-discount_percent')

    # Все категории для навигации
    categories = Category.objects.filter(is_active=True)

    return render(request, 'catalog/home.html', {
        'form': form,
        'popular_products': popular_products,
        'promotions': promotions,
        'categories': categories,
        'breadcrumbs': [
            {'title': 'Главная', 'url': '/'},
        ],
    })


def category_list_view(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'catalog/category_list.html', {
        'categories': categories,
        'breadcrumbs': [
            {'title': 'Главная', 'url': '/'},
            {'title': 'Категории', 'url': ''},
        ],
    })


def category_detail_view(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = category.products.filter(is_active=True)
    form = ProductSearchForm(request.GET or None)

    if form.is_valid() and form.cleaned_data.get('q'):
        q = form.cleaned_data['q']
        products = products.filter(name__icontains=q)

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


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
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


def promotions_view(request):
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