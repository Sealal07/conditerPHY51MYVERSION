import uuid  # Импорт для работы с уникальными идентификаторами (хотя здесь не используется явно)
from django.db import models  # Импорт базового класса моделей Django
from django.utils.text import slugify  # Импорт функции для создания URL-безопасных строк (слагов)
from decimal import Decimal  # Импорт для точных математических вычислений с деньгами

class Category(models.Model):  # Модель категории товаров
    name = models.CharField('Название', max_length=200, unique=True)  # Название категории, должно быть уникальным
    slug = models.SlugField('Слаг', max_length=200, unique=True, blank=True)  # Человекочитаемый URL, может быть пустым в админке
    description = models.TextField('Описание', blank=True)  # Необязательное текстовое описание
    is_active = models.BooleanField('Активна', default=True)  # Флаг, отображать ли категорию на сайте

    class Meta:  # Метаданные модели
        verbose_name = 'Категория'  # Название в единственном числе для админки
        verbose_name_plural = 'Категории'  # Название во множественном числе
        ordering = ['name']  # Сортировка по умолчанию по имени

    def save(self, *args, **kwargs):  # Переопределение метода сохранения
        if not self.slug:  # Если слаг не заполнен вручную
            self.slug = slugify(self.name)  # Генерируем его из названия
        super().save(*args, **kwargs)  # Вызываем стандартный метод сохранения

    def __str__(self):  # Строковое представление объекта
        return self.name  # Возвращает название категории

    def get_absolute_url(self):  # Метод для получения ссылки на страницу категории
        from django.urls import reverse  # Импорт функции reverse для генерации URL
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})  # Возвращает путь по имени маршрута


class Product(models.Model):  # Модель товара
    name = models.CharField('Название', max_length=300)  # Название товара
    slug = models.SlugField('Слаг', max_length=300, unique=True, blank=True)  # Уникальный URL товара
    category = models.ForeignKey(  # Связь "многие к одному" с категорией
        Category, on_delete=models.CASCADE, related_name='products',  # При удалении категории удаляются товары
        verbose_name='Категория'
    )
    description = models.TextField('Описание', blank=True)  # Описание товара
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)  # Цена (макс. 10 цифр, 2 после запятой)
    discount_percent = models.PositiveSmallIntegerField('Скидка (%)', default=0)  # Процент скидки (0-100)
    is_active = models.BooleanField('Активен', default=True)  # Видимость товара на сайте
    is_popular = models.BooleanField('Популярный', default=False)  # Ручная метка популярного товара
    created_at = models.DateTimeField('Создан', auto_now_add=True)  # Дата создания (ставится автоматически)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)  # Дата изменения (обновляется автоматически)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']  # Сортировка: сначала новые товары

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    @property  # Вычисляемое свойство: цена со скидкой
    def discount_price(self):
        if self.discount_percent > 0:  # Если есть скидка
            # Формула: Цена * (1 - Скидка/100)
            return self.price * (Decimal('1') - Decimal(self.discount_percent) / Decimal('100'))
        return self.price  # Если скидки нет, возвращаем обычную цену

    @property  # Проверка наличия скидки (True/False)
    def has_discount(self):
        return self.discount_percent > 0

    def total_ordered(self):  # Метод для подсчета общего количества проданных единиц
        """Количество заказов с этим товаром"""
        from orders.models import OrderItem  # Импорт модели позиций заказа (из другого приложения)
        return OrderItem.objects.filter(product=self).aggregate(
            total=models.Sum('quantity')  # Суммируем поле quantity
        )['total'] or 0  # Если заказов нет, возвращаем 0


class ProductImage(models.Model):  # Модель для нескольких изображений одного товара
    product = models.ForeignKey(  # Связь с товаром
        Product, on_delete=models.CASCADE, related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField('Изображение', upload_to='products/%Y/%m/%d/')  # Файл картинки с разбивкой по датам
    is_main = models.BooleanField('Главное', default=False)  # Флаг основного изображения для превью
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self):
        return f"Изображение: {self.product.name}"