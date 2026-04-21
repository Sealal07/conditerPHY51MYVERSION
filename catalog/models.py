import uuid
from django.db import models
from django.utils.text import slugify
from decimal import Decimal

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
            # Приводим проценты к типу Decimal перед расчетом
            return self.price * (Decimal('1') - Decimal(self.discount_percent) / Decimal('100'))
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