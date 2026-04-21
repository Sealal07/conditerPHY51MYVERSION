# Django проект — Магазин кондитерских изделий

Ниже — полная структура проекта со всеми файлами. Каждый файл представлен в отдельном блоке.

## 1. Структура проекта

```
confectionery_shop/
├── manage.py
├── requirements.txt
├── .env.example
├── confectionery_shop/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/accounts/
│       ├── login.html
│       ├── register.html
│       └── profile.html
├── catalog/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   ├── context_processors.py
│   ├── import_excel.py
│   └── templates/catalog/
│       ├── home.html
│       ├── category_list.html
│       ├── product_detail.html
│       ├── product_list.html
│       └── promotions.html
├── cart/
│   ├── __init__.py
│   ├── cart.py
│   ├── views.py
│   ├── urls.py
│   ├── context_processors.py
│   └── templates/cart/
│       └── cart_detail.html
├── orders/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/orders/
│       └── order_create.html
├── templates/
│   ├── base.html
│   └── partials/
│       └── breadcrumbs.html
└── static/
    └── css/
        └── style.css
```

---

## 2. requirements.txt

```txt
crispy-tailwind==1.0.3
Django>=5.0,<5.1[settings.py](config%2Fsettings.py)
psycopg2-binary>=2.9,<3.0
python-decouple>=3.8
openpyxl>=3.1,<4.0
Pillow>=10.0,<11.0
django-crispy-forms>=2.1,<3.0
pytils
```

---

## 3. .env.example

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=confectionery_shop
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 4. confectionery_shop/settings.py

```python
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-key-change-in-production')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_tailwind',
    'accounts',
    'catalog',
    'cart',
    'orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'confectionery_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'catalog.context_processors.categories_context',
                'cart.context_processors.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'confectionery_shop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='confectionery_shop'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='postgres'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'accounts:login'
LOGOUT_REDIRECT_URL = '/'
```

---

## 5. confectionery_shop/urls.py

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('catalog.urls', namespace='catalog_home')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 6. accounts/models.py

```python
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    address = models.TextField('Адрес доставки', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name() or self.username
```

---

## 7. accounts/views.py

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.phone = request.POST.get('phone', '')
        request.user.address = request.POST.get('address', '')
        request.user.save()
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html')
```

---

## 8. accounts/forms.py

```python
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',
                  'password1', 'password2', 'phone')
```

---

## 9. accounts/urls.py

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
```

---

## 10. accounts/templates/accounts/login.html

```html
{% extends "base.html" %}
{% load crispy_forms_tags %}

{% block content %}
<div class="max-w-md mx-auto mt-10 bg-white p-8 rounded-lg shadow">
    <h2 class="text-2xl font-bold mb-6 text-center">Вход</h2>
    <form method="post">
        {% csrf_token %}
        <input type="hidden" name="username" id="id_username" class="w-full border rounded px-3 py-2 mb-3" placeholder="Логин">
        <input type="password" name="password" id="id_password" class="w-full border rounded px-3 py-2 mb-3" placeholder="Пароль">
        <button type="submit" class="w-full bg-pink-600 text-white py-2 rounded hover:bg-pink-700 transition">Войти</button>
    </form>
    <p class="mt-4 text-center text-gray-600">
        Нет аккаунта? <a href="{% url 'accounts:register' %}" class="text-pink-600 hover:underline">Зарегистрироваться</a>
    </p>
</div>
{% endblock %}
```

---

## 11. accounts/templates/accounts/register.html

```html
{% extends "base.html" %}
{% load crispy_forms_tags %}

{% block content %}
<div class="max-w-md mx-auto mt-10 bg-white p-8 rounded-lg shadow">
    <h2 class="text-2xl font-bold mb-6 text-center">Регистрация</h2>
    <form method="post">
        {% csrf_token %}
        {% for field in form %}
        <div class="mb-3">
            <label class="block text-sm font-medium text-gray-700">{{ field.label }}</label>
            {{ field }}
            {% if field.errors %}
                <p class="text-red-500 text-xs mt-1">{{ field.errors.0 }}</p>
            {% endif %}
        </div>
        {% endfor %}
        <button type="submit" class="w-full bg-pink-600 text-white py-2 rounded hover:bg-pink-700 transition">Зарегистрироваться</button>
    </form>
    <p class="mt-4 text-center text-gray-600">
        Уже есть аккаунт? <a href="{% url 'accounts:login' %}" class="text-pink-600 hover:underline">Войти</a>
    </p>
</div>
{% endblock %}
```

---

## 12. accounts/templates/accounts/profile.html

```html
{% extends "base.html" %}
{% block content %}
<div class="max-w-2xl mx-auto mt-10 bg-white p-8 rounded-lg shadow">
    <h2 class="text-2xl font-bold mb-6">Профиль</h2>
    <form method="post">
        {% csrf_token %}
        <div class="grid grid-cols-2 gap-4">
            <div>
                <label class="block text-sm font-medium text-gray-700">Имя</label>
                <input type="text" name="first_name" value="{{ user.first_name }}" class="w-full border rounded px-3 py-2">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Фамилия</label>
                <input type="text" name="last_name" value="{{ user.last_name }}" class="w-full border rounded px-3 py-2">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Email</label>
                <input type="email" name="email" value="{{ user.email }}" class="w-full border rounded px-3 py-2">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Телефон</label>
                <input type="text" name="phone" value="{{ user.phone|default:'' }}" class="w-full border rounded px-3 py-2">
            </div>
        </div>
        <div class="mt-4">
            <label class="block text-sm font-medium text-gray-700">Адрес доставки</label>
            <textarea name="address" class="w-full border rounded px-3 py-2" rows="3">{{ user.address|default:'' }}</textarea>
        </div>
        <button type="submit" class="mt-4 bg-pink-600 text-white px-6 py-2 rounded hover:bg-pink-700 transition">Сохранить</button>
    </form>
</div>
{% endblock %}
```

---

## 13. catalog/models.py

```python
import uuid
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    slug = models.SlugField('Слаг', max_length=200, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField('Название', max_length=300)
    slug = models.SlugField('Слаг', max_length=300, unique=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products',
        verbose_name='Категория'
    )
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    discount_percent = models.PositiveSmallIntegerField('Скидка (%)', default=0)
    is_active = models.BooleanField('Активен', default=True)
    is_popular = models.BooleanField('Популярный', default=False)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    @property
    def discount_price(self):
        if self.discount_percent > 0:
            return self.price * (1 - self.discount_percent / 100)
        return self.price

    @property
    def has_discount(self):
        return self.discount_percent > 0

    def total_ordered(self):
        """Количество заказов с этим товаром"""
        from orders.models import OrderItem
        return OrderItem.objects.filter(product=self).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField('Изображение', upload_to='products/%Y/%m/%d/')
    is_main = models.BooleanField('Главное', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self):
        return f"Изображение: {self.product.name}"
```

---

## 14. catalog/admin.py

```python
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage
from .forms import ExcelImportForm


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return ''
    image_preview.short_description = 'Превью'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    search_fields = ('name',)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'is_main')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return ''
    image_preview.short_description = 'Превью'


admin.site.register(ProductImage, ProductImageAdmin)


class ProductImageMultiInline(admin.StackedInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'is_main')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_percent',
                    'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'discount_percent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageMultiInline]
    list_editable = ('price', 'discount_percent', 'is_active')

    change_list_template = 'admin/catalog/product/change_list_import.html'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel_view), name='catalog_product_import_excel'),
        ]
        return custom_urls + urls

    def import_excel_view(self, request):
        from .import_excel import import_from_excel
        if request.method == 'POST':
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = request.FILES['excel_file']
                result = import_from_excel(excel_file)
                self.message_user(request, result)
                return redirect('..')
        else:
            form = ExcelImportForm()
        from django.shortcuts import render
        return render(request, 'admin/catalog/product/import_excel.html', {
            'form': form,
            'title': 'Импорт товаров из Excel',
        })
```

---

## 15. catalog/forms.py

```python
from django import forms


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label='Excel файл', help_text='Файл с листами: category, products')


class ProductSearchForm(forms.Form):
    q = forms.CharField(label='Поиск', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Поиск товаров...', 'class': 'w-full border rounded px-3 py-2'}
    ))
```

---

## 16. catalog/import_excel.py

```python
import openpyxl
from django.db import IntegrityError
from .models import Category, Product


def import_from_excel(excel_file):
    """
    Импорт категорий и товаров из Excel файла.
    Листы: 'category', 'products'
    """
    wb = openpyxl.load_workbook(excel_file)
    categories_created = 0
    products_created = 0
    errors = []

    # --- Импорт категорий ---
    if 'category' in wb.sheetnames:
        ws = wb['category']
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not row or not row[0]:
                continue
            try:
                name = str(row[0]).strip()
                description = str(row[1]).strip() if len(row) > 1 and row[1] else ''
                is_active = True
                if len(row) > 2:
                    val = str(row[2]).strip().lower()
                    is_active = val not in ('0', 'false', 'нет', 'no')

                cat, created = Category.objects.get_or_create(
                    name=name,
                    defaults={'description': description, 'is_active': is_active}
                )
                if created:
                    categories_created += 1
            except IntegrityError as e:
                errors.append(f"Строка {row_idx} (category): {e}")

    # --- Импорт товаров ---
    if 'products' in wb.sheetnames:
        ws = wb['products']
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not row or not row[0]:
                continue
            try:
                name = str(row[0]).strip()
                category_name = str(row[1]).strip() if len(row) > 1 else ''
                description = str(row[2]).strip() if len(row) > 2 and row[2] else ''
                price = float(row[3]) if len(row) > 3 and row[3] else 0
                discount = int(row[4]) if len(row) > 4 and row[4] else 0
                is_active = True
                if len(row) > 5:
                    val = str(row[5]).strip().lower()
                    is_active = val not in ('0', 'false', 'нет', 'no')

                try:
                    category = Category.objects.get(name=category_name)
                except Category.DoesNotExist:
                    errors.append(f"Строка {row_idx} (products): категория '{category_name}' не найдена")
                    continue

                product, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        'category': category,
                        'description': description,
                        'price': price,
                        'discount_percent': discount,
                        'is_active': is_active,
                    }
                )
                if created:
                    products_created += 1
                else:
                    product.price = price
                    product.discount_percent = discount
                    product.save()

            except (ValueError, IntegrityError) as e:
                errors.append(f"Строка {row_idx} (products): {e}")

    msg = f"Импорт завершён. Категорий создано: {categories_created}, Товаров создано: {products_created}."
    if errors:
        msg += f" Ошибки: {'; '.join(errors)}"
    return msg
```

---

## 17. catalog/views.py

```python
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
```

---

## 18. catalog/urls.py

```python
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('categories/', views.category_list_view, name='category_list'),
    path('categories/<slug:slug>/', views.category_detail_view, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('promotions/', views.promotions_view, name='promotions'),
]
```

---

## 19. catalog/context_processors.py

```python
from .models import Category


def categories_context(request):
    return {
        'nav_categories': Category.objects.filter(is_active=True),
    }
```

---

## 20. cart/cart.py

```python
from decimal import Decimal
from catalog.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'discount_percent': product.discount_percent,
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            if item['discount_percent'] > 0:
                item['discount_price'] = item['price'] * (1 - item['discount_percent'] / 100)
            else:
                item['discount_price'] = item['price']
            item['total_price'] = item['discount_price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * (1 - item['discount_percent'] / 100) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        del self.session['cart']
        self.save()
```

---

## 21. cart/views.py

```python
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity=quantity)
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')
```

---

## 22. cart/urls.py

```python
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('clear/', views.cart_clear, name='cart_clear'),
]
```

---

## 23. cart/context_processors.py

```python
from .cart import Cart


def cart_context(request):
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_total_items': len(cart),
    }
```

---

## 24. orders/models.py

```python
from django.db import models
from django.conf import settings
from catalog.models import Product
from decimal import Decimal


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders',
        verbose_name='Пользователь'
    )
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    address = models.TextField('Адрес')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)
    total_price = models.DecimalField('Итого', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} — {self.get_full_name()}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_total(self):
        self.total_price = sum(item.get_total_cost() for item in self.items.all())
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='orderitem',
        verbose_name='Товар'
    )
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_cost(self):
        return self.price * self.quantity
```

---

## 25. orders/admin.py

```python
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name',
                    'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at', 'total_price')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.update_total()
        super().save_model(request, obj, form, change)
```

---

## 26. orders/views.py

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.cart import Cart
from decimal import Decimal


@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name', request.user.first_name),
            last_name=request.POST.get('last_name', request.user.last_name),
            email=request.POST.get('email', request.user.email),
            phone=request.POST.get('phone', request.user.phone or ''),
            address=request.POST.get('address', request.user.address or ''),
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['discount_price'],
                quantity=item['quantity'],
            )
        order.update_total()
        cart.clear()
        return redirect('orders:order_success')

    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'breadcrumbs': [
            {'title': 'Главная', 'url': '/'},
            {'title': 'Корзина', 'url': '/cart/'},
            {'title': 'Оформление заказа', 'url': ''},
        ],
    })


@login_required
def order_success(request):
    return render(request, 'orders/order_create.html', {
        'success': True,
        'breadcrumbs': [
            {'title': 'Главная', 'url': '/'},
            {'title': 'Заказ оформлен', 'url': ''},
        ],
    })
```

---

## 27. orders/urls.py

```python
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('success/', views.order_success, name='order_success'),
]
```

---

## 28. templates/base.html

```html
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Сладкий Мир — Кондитерская{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@3.4.0/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/@fontsource/inter@5.0.0/index.min.css" rel="stylesheet">
    <link href="{% static 'css/style.css' %}" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body class="font-sans bg-gray-50 text-gray-800">

    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
            <a href="/" class="text-2xl font-bold text-pink-600 hover:text-pink-700">🧁 Сладкий Мир</a>

            <nav class="hidden md:flex items-center gap-6">
                <a href="/" class="hover:text-pink-600 transition">Главная</a>
                <a href="{% url 'catalog:category_list' %}" class="hover:text-pink-600 transition">Каталог</a>
                <a href="{% url 'catalog:promotions' %}" class="hover:text-pink-600 transition text-red-500 font-semibold">Акции</a>
            </nav>

            <div class="flex items-center gap-4">
                <a href="{% url 'cart:cart_detail' %}" class="relative hover:text-pink-600 transition">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/>
                    </svg>
                    {% if cart_total_items > 0 %}
                        <span class="absolute -top-2 -right-2 bg-pink-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">{{ cart_total_items }}</span>
                    {% endif %}
                </a>
                {% if user.is_authenticated %}
                    <div class="relative group">
                        <button class="hover:text-pink-600 transition flex items-center gap-1">
                            <span>{{ user.first_name|default:user.username }}</span>
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                            </svg>
                        </button>
                        <div class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 hidden group-hover:block border">
                            <a href="{% url 'accounts:profile' %}" class="block px-4 py-2 hover:bg-pink-50">Профиль</a>
                            <a href="{% url 'accounts:logout' %}" class="block px-4 py-2 hover:bg-pink-50 text-red-500">Выйти</a>
                        </div>
                    </div>
                {% else %}
                    <a href="{% url 'accounts:login' %}" class="hover:text-pink-600 transition">Войти</a>
                {% endif %}
            </div>
        </div>

        <!-- Mobile nav -->
        <div class="md:hidden border-t px-4 py-2 flex gap-4 text-sm overflow-x-auto">
            <a href="/" class="whitespace-nowrap hover:text-pink-600">Главная</a>
            <a href="{% url 'catalog:category_list' %}" class="whitespace-nowrap hover:text-pink-600">Каталог</a>
            <a href="{% url 'catalog:promotions' %}" class="whitespace-nowrap text-red-500">Акции</a>
        </div>
    </header>

    <!-- Breadcrumbs -->
    {% if breadcrumbs %}
    <nav class="bg-white border-b">
        <div class="max-w-7xl mx-auto px-4 py-2">
            <ol class="flex items-center gap-2 text-sm text-gray-500">
                {% for crumb in breadcrumbs %}
                    {% if not forloop.last %}
                        <li><a href="{{ crumb.url }}" class="hover:text-pink-600 transition">{{ crumb.title }}</a></li>
                        <li>/</li>
                    {% else %}
                        <li class="text-gray-800 font-medium">{{ crumb.title }}</li>
                    {% endif %}
                {% endfor %}
            </ol>
        </div>
    </nav>
    {% endif %}

    <!-- Messages -->
    {% if messages %}
    <div class="max-w-7xl mx-auto px-4 mt-4">
        {% for message in messages %}
            <div class="p-4 rounded-lg mb-2 {% if message.tags == 'error' %}bg-red-100 text-red-700{% elif message.tags == 'success' %}bg-green-100 text-green-700{% else %}bg-blue-100 text-blue-700{% endif %}">
                {{ message }}
            </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-8 min-h-screen">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-gray-300 py-8 mt-12">
        <div class="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
                <h3 class="text-white font-bold text-lg mb-2">🧁 Сладкий Мир</h3>
                <p class="text-sm">Лучшие кондитерские изделия с доставкой на дом.</p>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-2">Навигация</h4>
                <ul class="space-y-1 text-sm">
                    <li><a href="/" class="hover:text-pink-400">Главная</a></li>
                    <li><a href="{% url 'catalog:category_list' %}" class="hover:text-pink-400">Каталог</a></li>
                    <li><a href="{% url 'catalog:promotions' %}" class="hover:text-pink-400">Акции</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-2">Контакты</h4>
                <p class="text-sm">Телефон: +7 (999) 123-45-67</p>
                <p class="text-sm">Email: info@sweetworld.ru</p>
            </div>
        </div>
        <div class="max-w-7xl mx-auto px-4 mt-6 pt-4 border-t border-gray-700 text-center text-sm">
            &copy; {% now "Y" %} Сладкий Мир. Все права защищены.
        </div>
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## 29. templates/partials/breadcrumbs.html

(уже встроен в base.html, но можно использовать отдельно)

---

## 30. catalog/templates/catalog/home.html

```html
{% extends "base.html" %}
{% block title %}Сладкий Мир — Главная{% endblock %}

{% block content %}

<!-- Hero Section -->
<section class="bg-gradient-to-r from-pink-500 to-purple-600 rounded-2xl p-8 md:p-12 mb-10 text-white">
    <h1 class="text-3xl md:text-5xl font-bold mb-4">Свежие кондитерские изделия</h1>
    <p class="text-lg md:text-xl mb-6 opacity-90">Торты, пирожные, печенье и многое другое — с любовью к каждой детали</p>
    <a href="{% url 'catalog:category_list' %}" class="inline-block bg-white text-pink-600 px-6 py-3 rounded-lg font-semibold hover:bg-pink-50 transition">Перейти в каталог</a>
</section>

<!-- Popular Products -->
<section class="mb-10">
    <h2 class="text-2xl font-bold mb-6 flex items-center gap-2">
        <span class="text-yellow-500">⭐</span> Популярные товары
    </h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
        {% for product in popular_products %}
            <div class="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden group">
                <div class="relative h-48 bg-gray-100 overflow-hidden">
                    {% if product.images.first %}
                        <img src="{{ product.images.first.image.url }}" alt="{{ product.name }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                    {% else %}
                        <div class="flex items-center justify-center h-full text-gray-400 text-4xl">🍰</div>
                    {% endif %}
                    {% if product.has_discount %}
                        <span class="absolute top-2 left-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">-{{ product.discount_percent }}%</span>
                    {% endif %}
                </div>
                <div class="p-4">
                    <h3 class="font-semibold text-sm mb-1 truncate">{{ product.name }}</h3>
                    <p class="text-xs text-gray-500 mb-2">{{ product.category.name }}</p>
                    <div class="flex items-center justify-between">
                        <div>
                            {% if product.has_discount %}
                                <span class="text-gray-400 line-through text-xs">{{ product.price }} ₽</span>
                                <span class="text-pink-600 font-bold ml-1">{{ product.discount_price|floatformat:0 }} ₽</span>
                            {% else %}
                                <span class="text-pink-600 font-bold">{{ product.price }} ₽</span>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        {% empty %}
            <p class="text-gray-500 col-span-full">Пока нет популярных товаров</p>
        {% endfor %}
    </div>
</section>

<!-- Promotions -->
{% if promotions %}
<section class="mb-10">
    <h2 class="text-2xl font-bold mb-6 flex items-center gap-2">
        <span class="text-red-500">🔥</span> Акции
    </h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {% for product in promotions %}
            <a href="{{ product.get_absolute_url }}" class="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden group">
                <div class="relative h-48 bg-gray-100 overflow-hidden">
                    {% if product.images.first %}
                        <img src="{{ product.images.first.image.url }}" alt="{{ product.name }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                    {% else %}
                        <div class="flex items-center justify-center h-full text-gray-400 text-4xl">🎂</div>
                    {% endif %}
                    <span class="absolute top-2 left-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">-{{ product.discount_percent }}%</span>
                </div>
                <div class="p-4">
                    <h3 class="font-semibold mb-1 truncate">{{ product.name }}</h3>
                    <p class="text-gray-400 line-through text-sm">{{ product.price }} ₽</p>
                    <p class="text-pink-600 font-bold text-lg">{{ product.discount_price|floatformat:0 }} ₽</p>
                </div>
            </a>
        {% endfor %}
    </div>
</section>
{% endif %}

<!-- Categories -->
<section class="mb-10">
    <h2 class="text-2xl font-bold mb-6">Категории</h2>
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        {% for cat in categories %}
            <a href="{{ cat.get_absolute_url }}" class="bg-white rounded-xl shadow p-6 text-center hover:bg-pink-50 transition hover:shadow-md">
                <div class="text-4xl mb-2">
                    {% if 'торт' in cat.name|lower %}🎂{% elif 'печень' in cat.name|lower %}🍪{% elif 'конфет' in cat.name|lower %}🍬{% elif 'пирожн' in cat.name|lower %}🧁{% elif 'шоколад' in cat.name|lower %}🍫{% else %}🍰{% endif %}
                </div>
                <h3 class="font-semibold">{{ cat.name }}</h3>
                <p class="text-xs text-gray-500 mt-1">{{ cat.products.filter.is_active.count }} товаров</p>
            </a>
        {% endfor %}
    </div>
</section>

{% endblock %}
```

---

## 31. catalog/templates/catalog/category_list.html

```html
{% extends "base.html" %}
{% block content %}
<h1 class="text-3xl font-bold mb-8">Категории</h1>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    {% for cat in categories %}
        <a href="{{ cat.get_absolute_url }}" class="bg-white rounded-xl shadow p-6 hover:shadow-lg transition flex items-center gap-4">
            <div class="text-4xl">
                {% if 'торт' in cat.name|lower %}🎂{% elif 'печень' in cat.name|lower %}🍪{% elif 'конфет' in cat.name|lower %}🍬{% elif 'пирожн' in cat.name|lower %}🧁{% elif 'шоколад' in cat.name|lower %}🍫{% else %}🍰{% endif %}
            </div>
            <div>
                <h3 class="font-bold text-lg">{{ cat.name }}</h3>
                <p class="text-gray-500 text-sm">{{ cat.description|truncatechars:80 }}</p>
                <p class="text-pink-600 text-sm mt-1">{{ cat.products.filter.is_active.count }} товаров</p>
            </div>
        </a>
    {% empty %}
        <p class="text-gray-500 col-span-full">Категории пока не добавлены</p>
    {% endfor %}
</div>
{% endblock %}
```

---

## 32. catalog/templates/catalog/product_list.html

```html
{% extends "base.html" %}
{% block content %}
<h1 class="text-3xl font-bold mb-2">{{ category.name }}</h1>
<p class="text-gray-500 mb-6">{{ category.description }}</p>

<!-- Search -->
<form method="get" class="mb-6 max-w-md">
    <div class="flex gap-2">
        <input type="text" name="q" value="{{ form.q.value|default:'' }}" placeholder="Поиск в категории..." class="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-pink-400">
        <button type="submit" class="bg-pink-600 text-white px-4 py-2 rounded-lg hover:bg-pink-700 transition">Найти</button>
    </div>
</form>

<!-- Products Grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    {% for product in products %}
        <a href="{{ product.get_absolute_url }}" class="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden group">
            <div class="relative h-56 bg-gray-100 overflow-hidden">
                {% if product.images.first %}
                    <img src="{{ product.images.first.image.url }}" alt="{{ product.name }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                {% else %}
                    <div class="flex items-center justify-center h-full text-gray-400 text-5xl">🍰</div>
                {% endif %}
                {% if product.has_discount %}
                    <span class="absolute top-3 left-3 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">-{{ product.discount_percent }}%</span>
                {% endif %}
            </div>
            <div class="p-4">
                <h3 class="font-semibold mb-1 truncate">{{ product.name }}</h3>
                <p class="text-sm text-gray-500 mb-3">{{ product.description|truncatechars:60 }}</p>
                <div class="flex items-center justify-between">
                    <div>
                        {% if product.has_discount %}
                            <span class="text-gray-400 line-through text-sm">{{ product.price }} ₽</span>
                            <span class="text-pink-600 font-bold text-lg ml-1">{{ product.discount_price|floatformat:0 }} ₽</span>
                        {% else %}
                            <span class="text-pink-600 font-bold text-lg">{{ product.price }} ₽</span>
                        {% endif %}
                    </div>
                </div>
            </div>
        </a>
    {% empty %}
        <p class="text-gray-500 col-span-full text-center py-8">В этой категории пока нет товаров</p>
    {% endfor %}
</div>
{% endblock %}
```

---

## 33. catalog/templates/catalog/product_detail.html

```html
{% extends "base.html" %}
{% block content %}
<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
    <!-- Gallery -->
    <div>
        {% if product.images.exists %}
            <div class="bg-gray-100 rounded-2xl overflow-hidden mb-4 h-96" id="main-image-container">
                <img id="main-image" src="{{ product.images.first.image.url }}" alt="{{ product.name }}" class="w-full h-full object-cover">
            </div>
            {% if product.images.count > 1 %}
                <div class="flex gap-2 overflow-x-auto py-2">
                    {% for img in product.images.all %}
                        <button onclick="document.getElementById('main-image').src='{{ img.image.url }}'"
                                class="flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 {% if forloop.first %}border-pink-500{% else %}border-transparent{% endif %} hover:border-pink-400 transition">
                            <img src="{{ img.image.url }}" alt="Фото {{ forloop.counter }}" class="w-full h-full object-cover">
                        </button>
                    {% endfor %}
                </div>
            {% endif %}
        {% else %}
            <div class="bg-gray-100 rounded-2xl h-96 flex items-center justify-center text-gray-400 text-6xl">🍰</div>
        {% endif %}
    </div>

    <!-- Product Info -->
    <div>
        <span class="text-sm text-pink-600 font-medium">{{ product.category.name }}</span>
        <h1 class="text-3xl font-bold mt-1 mb-4">{{ product.name }}</h1>

        {% if product.has_discount %}
            <div class="flex items-center gap-3 mb-4">
                <span class="text-gray-400 line-through text-xl">{{ product.price }} ₽</span>
                <span class="text-3xl font-bold text-pink-600">{{ product.discount_price|floatformat:0 }} ₽</span>
                <span class="bg-red-500 text-white text-sm font-bold px-2 py-1 rounded">-{{ product.discount_percent }}%</span>
            </div>
        {% else %}
            <p class="text-3xl font-bold text-pink-600 mb-4">{{ product.price }} ₽</p>
        {% endif %}

        <p class="text-gray-600 mb-6 leading-relaxed">{{ product.description|linebreaks }}</p>

        <!-- Add to Cart -->
        <form method="post" action="{% url 'cart:cart_add' product.id %}" class="flex items-center gap-4">
            {% csrf_token %}
            <div class="flex items-center border rounded-lg">
                <button type="button" onclick="changeQty(-1)" class="px-3 py-2 hover:bg-gray-100 rounded-l-lg">−</button>
                <input type="number" name="quantity" id="qty-input" value="1" min="1" class="w-12 text-center border-x py-2 focus:outline-none">
                <button type="button" onclick="changeQty(1)" class="px-3 py-2 hover:bg-gray-100 rounded-r-lg">+</button>
            </div>
            <button type="submit" class="bg-pink-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-pink-700 transition flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/></svg>
                В корзину
            </button>
        </form>
    </div>
</div>

<!-- Related Products -->
{% if related_products %}
<section>
    <h2 class="text-2xl font-bold mb-6">Похожие товары</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {% for p in related_products %}
            <a href="{{ p.get_absolute_url }}" class="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden group">
                <div class="relative h-48 bg-gray-100 overflow-hidden">
                    {% if p.images.first %}
                        <img src="{{ p.images.first.image.url }}" alt="{{ p.name }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                    {% else %}
                        <div class="flex items-center justify-center h-full text-gray-400 text-4xl">🍰</div>
                    {% endif %}
                </div>
                <div class="p-4">
                    <h3 class="font-semibold text-sm mb-1 truncate">{{ p.name }}</h3>
                    <p class="text-pink-600 font-bold">{{ p.price }} ₽</p>
                </div>
            </a>
        {% endfor %}
    </div>
</section>
{% endif %}

<script>
function changeQty(delta) {
    const input = document.getElementById('qty-input');
    let val = parseInt(input.value) || 1;
    val = Math.max(1, val + delta);
    input.value = val;
}
</script>
{% endblock %}
```

---

## 34. catalog/templates/catalog/promotions.html

```html
{% extends "base.html" %}
{% block content %}
<h1 class="text-3xl font-bold mb-2 text-red-500">🔥 Акции и скидки</h1>
<p class="text-gray-500 mb-8">Специальные предложения на кондитерские изделия</p>

{% if promotions %}
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    {% for product in promotions %}
        <a href="{{ product.get_absolute_url }}" class="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden group relative">
            <div class="absolute top-3 right-3 bg-red-500 text-white text-sm font-bold w-12 h-12 rounded-full flex items-center justify-center z-10 shadow">
                -{{ product.discount_percent }}%
            </div>
            <div class="relative h-56 bg-gray-100 overflow-hidden">
                {% if product.images.first %}
                    <img src="{{ product.images.first.image.url }}" alt="{{ product.name }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                {% else %}
                    <div class="flex items-center justify-center h-full text-gray-400 text-5xl">🎂</div>
                {% endif %}
            </div>
            <div class="p-4">
                <h3 class="font-semibold mb-1">{{ product.name }}</h3>
                <p class="text-sm text-gray-500 mb-2">{{ product.category.name }}</p>
                <div class="flex items-center gap-2">
                    <span class="text-gray-400 line-through">{{ product.price }} ₽</span>
                    <span class="text-pink-600 font-bold text-xl">{{ product.discount_price|floatformat:0 }} ₽</span>
                </div>
                <p class="text-green-600 text-sm mt-1">Экономия: {{ product.price|add:product.discount_price|floatformat:0 }} ₽</p>
            </div>
        </a>
    {% endfor %}
</div>
{% else %}
<p class="text-gray-500 text-center py-12">Сейчас нет активных акций. Загляните позже!</p>
{% endif %}
{% endblock %}
```

---

## 35. cart/templates/cart/cart_detail.html

```html
{% extends "base.html" %}
{% block content %}
<h1 class="text-3xl font-bold mb-8">Корзина</h1>

{% if cart|length == 0 %}
    <div class="text-center py-16">
        <div class="text-6xl mb-4">🛒</div>
        <p class="text-gray-500 text-lg mb-4">Ваша корзина пуста</p>
        <a href="{% url 'catalog:category_list' %}" class="inline-block bg-pink-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-pink-700 transition">Перейти в каталог</a>
    </div>
{% else %}
    <div class="bg-white rounded-xl shadow overflow-hidden">
        <table class="w-full">
            <thead class="bg-gray-50">
                <tr>
                    <th class="text-left px-6 py-3 text-sm font-semibold text-gray-600">Товар</th>
                    <th class="px-6 py-3 text-sm font-semibold text-gray-600">Цена</th>
                    <th class="px-6 py-3 text-sm font-semibold text-gray-600">Кол-во</th>
                    <th class="px-6 py-3 text-sm font-semibold text-gray-600">Итого</th>
                    <th class="px-6 py-3 text-sm font-semibold text-gray-600"></th>
                </tr>
            </thead>
            <tbody class="divide-y">
                {% for item in cart %}
                    <tr class="hover:bg-gray-50">
                        <td class="px-6 py-4">
                            <div class="flex items-center gap-4">
                                {% if item.product.images.first %}
                                    <img src="{{ item.product.images.first.image.url }}" alt="{{ item.product.name }}" class="w-16 h-16 object-cover rounded-lg">
                                {% endif %}
                                <div>
                                    <a href="{{ item.product.get_absolute_url }}" class="font-semibold hover:text-pink-600">{{ item.product.name }}</a>
                                    {% if item.product.has_discount %}
                                        <span class="text-red-500 text-xs">Скидка {{ item.product.discount_percent }}%</span>
                                    {% endif %}
                                </div>
                            </div>
                        </td>
                        <td class="px-6 py-4 text-center">
                            {% if item.product.has_discount %}
                                <span class="text-gray-400 line-through text-sm">{{ item.price }} ₽</span><br>
                                <span class="text-pink-600 font-semibold">{{ item.discount_price|floatformat:0 }} ₽</span>
                            {% else %}
                                <span class="font-semibold">{{ item.price }} ₽</span>
                            {% endif %}
                        </td>
                        <td class="px-6 py-4 text-center">{{ item.quantity }}</td>
                        <td class="px-6 py-4 text-center font-bold">{{ item.total_price|floatformat:0 }} ₽</td>
                        <td class="px-6 py-4 text-center">
                            <a href="{% url 'cart:cart_remove' item.product.id %}" class="text-red-500 hover:text-red-700 transition">✕</a>
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="mt-8 flex flex-col sm:flex-row items-center justify-between bg-white rounded-xl shadow p-6 gap-4">
        <div>
            <p class="text-gray-500">Итого ({{ cart|length }} товаров):</p>
            <p class="text-3xl font-bold text-pink-600">{{ cart.get_total_price|floatformat:0 }} ₽</p>
        </div>
        <div class="flex gap-3">
            <a href="{% url 'cart:cart_clear' %}" class="border border-gray-300 px-6 py-3 rounded-lg hover:bg-gray-50 transition">Очистить</a>
            {% if user.is_authenticated %}
                <a href="{% url 'orders:order_create' %}" class="bg-pink-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-pink-700 transition">Оформить заказ</a>
            {% else %}
                <a href="{% url 'accounts:login' %}?next={% url 'orders:order_create' %}" class="bg-pink-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-pink-700 transition">Войти для оформления</a>
            {% endif %}
        </div>
    </div>
{% endif %}
{% endblock %}
```

---

## 36. orders/templates/orders/order_create.html

```html
{% extends "base.html" %}
{% block content %}

{% if success %}
    <div class="max-w-lg mx-auto text-center py-16">
        <div class="text-6xl mb-4">✅</div>
        <h1 class="text-3xl font-bold mb-4">Заказ оформлен!</h1>
        <p class="text-gray-500 mb-6">Спасибо за покупку! Мы свяжемся с вами для подтверждения.</p>
        <a href="/" class="inline-block bg-pink-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-pink-700 transition">Вернуться на главную</a>
    </div>
{% else %}
    <h1 class="text-3xl font-bold mb-8">Оформление заказа</h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Order Form -->
        <div class="lg:col-span-2 bg-white rounded-xl shadow p-6">
            <h2 class="text-xl font-bold mb-6">Данные получателя</h2>
            <form method="post">
                {% csrf_token %}
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Имя *</label>
                        <input type="text" name="first_name" value="{{ user.first_name }}" required class="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-pink-400 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Фамилия *</label>
                        <input type="text" name="last_name" value="{{ user.last_name }}" required class="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-pink-400 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Email *</label>
                        <input type="email" name="email" value="{{ user.email }}" required class="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-pink-400 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Телефон *</label>
                        <input type="tel" name="phone" value="{{ user.phone|default:'' }}" required class="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-pink-400 focus:outline-none">
                    </div>
                </div>
                <div class="mt-4">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Адрес доставки *</label>
                    <textarea name="address" required class="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-pink-400 focus:outline-none" rows="3">{{ user.address|default:'' }}</textarea>
                </div>
                <button type="submit" class="mt-6 w-full bg-pink-600 text-white py-3 rounded-lg font-semibold hover:bg-pink-700 transition text-lg">Подтвердить заказ</button>
            </form>
        </div>

        <!-- Order Summary -->
        <div class="bg-white rounded-xl shadow p-6 h-fit">
            <h2 class="text-xl font-bold mb-4">Ваш заказ</h2>
            <div class="divide-y mb-4">
                {% for item in cart %}
                    <div class="py-3 flex justify-between items-center">
                        <div>
                            <p class="font-medium text-sm">{{ item.product.name }}</p>
                            <p class="text-gray-500 text-xs">{{ item.quantity }} × {{ item.discount_price|floatformat:0 }} ₽</p>
                        </div>
                        <span class="font-semibold">{{ item.total_price|floatformat:0 }} ₽</span>
                    </div>
                {% endfor %}
            </div>
            <div class="border-t pt-4 flex justify-between items-center">
                <span class="text-lg font-bold">Итого:</span>
                <span class="text-2xl font-bold text-pink-600">{{ cart.get_total_price|floatformat:0 }} ₽</span>
            </div>
        </div>
    </div>
{% endif %}
{% endblock %}
```

---

## 37. catalog/templates/admin/catalog/product/change_list_import.html

```html
{% extends "admin/change_list.html" %}

{% block object-tools-items %}
    <li>
        <a href="{% url 'admin:catalog_product_import_excel' %}" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition">
            📥 Импорт из Excel
        </a>
    </li>
    {{ block.super }}
{% endblock %}
```

---

## 38. catalog/templates/admin/catalog/product/import_excel.html

```html
{% extends "admin/base_site.html" %}
{% load i18n admin_urls %}

{% block content %}
<div class="max-w-lg mx-auto bg-white p-8 rounded-lg shadow">
    <h2 class="text-xl font-bold mb-4">Импорт товаров из Excel</h2>
    <p class="text-gray-600 text-sm mb-6">
        Файл должен содержать два листа:<br>
        <strong>category</strong> — колонки: название, описание, активна (да/нет)<br>
        <strong>products</strong> — колонки: название, категория, описание, цена, скидка(%), активен (да/нет)
    </p>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <div class="mb-4">
            {{ form.as_p }}
        </div>
        <button type="submit" class="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 transition">
            Загрузить
        </button>
    </form>
    <p class="mt-4"><a href="{% url 'admin:catalog_product_changelist' %}" class="text-blue-600 hover:underline">← Назад к товарам</a></p>
</div>
{% endblock %}
```

---

## 39. static/css/style.css

```css
/* Custom styles for Sweet World Confectionery Shop */

body {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

/* Smooth scroll */
html {
    scroll-behavior: smooth;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #f1f1f1;
}
::-webkit-scrollbar-thumb {
    background: #e91e63;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #c2185b;
}

/* Gallery image transitions */
#main-image {
    transition: opacity 0.3s ease;
}

/* Hover effects */
.group:hover .group-hover\:scale-105 {
    transform: scale(1.05);
}

/* Badge pulse animation */
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

/* Focus styles */
input:focus, textarea:focus, select:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.3);
}

/* Breadcrumb hover */
nav ol li a:hover {
    color: #db2777;
}

/* Table row hover */
tbody tr:hover {
    background-color: #fdf2f8;
}
```

---

## 40. manage.py

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confectionery_shop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

---

## 41. confectionery_shop/wsgi.py

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confectionery_shop.settings')
application = get_wsgi_application()
```

---

## 42. confectionery_shop/asgi.py

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confectionery_shop.settings')
application = get_asgi_application()
```

---

## 43. confectionery_shop/__init__.py

```python
```

---

## 44. accounts/__init__.py

```python
```

---

## 45. catalog/__init__.py

```python
```

---

## 46. cart/__init__.py

```python
```

---

## 47. orders/__init__.py

```python
```

---

## Инструкция по запуску

```bash
# 1. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Создать .env файл
cp .env.example .env
# Отредактировать .env с реальными данными PostgreSQL

# 4. Применить настройки AUTH_USER_MODEL в settings.py
# Добавить в settings.py:
# AUTH_USER_MODEL = 'accounts.CustomUser'

# 5. Создать миграции и применить
python manage.py makemigrations
python manage.py migrate

# 6. Создать суперпользователя
python manage.py createsuperuser

# 7. Запустить сервер
python manage.py runserver
```

---

## Пример Excel-файла для импорта

**Лист `category`:**

| name        | description      | is_active |
|-------------|------------------|-----------|
| Торты       | Праздничные торты | да        |
| Печенье     | Разное печенье    | да        |
| Конфеты     | Шоколадные конфеты| да        |
| Пирожные    | Нежные пирожные   | да        |

**Лист `products`:**

| name              | category | description         | price  | discount_percent | is_active |
|-------------------|----------|---------------------|--------|------------------|-----------|
| Торт Наполеон     | Торты    | Классический торт   | 1200.00| 15               | да        |
| Торт Медовик      | Торты    | Медовый торт        | 900.00 | 0                | да        |
| Печенье Овсяное   | Печенье  | Овсяное печенье     | 250.00 | 10               | да        |
| Конфеты Ассорти   | Конфеты  | Набор конфет        | 500.00 | 20               | да        |
| Пирожное Эклер    | Пирожные | Заварное пирожное   | 150.00 | 0                | да        |