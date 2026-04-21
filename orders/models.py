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