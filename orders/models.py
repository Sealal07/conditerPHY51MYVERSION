from django.db import models  # Импорт базового модуля для создания моделей Django
from django.conf import settings  # Импорт настроек проекта для доступа к модели пользователя
from catalog.models import Product  # Импорт модели товара из приложения каталога
from decimal import Decimal  # Импорт типа Decimal для точных финансовых вычислений


class Order(models.Model):  # Определение модели основного заказа
    STATUS_CHOICES = [  # Список доступных статусов заказа для выбора
        ('pending', 'Ожидает'),  # Статус: заказ только что создан
        ('processing', 'В обработке'),  # Статус: заказ собирается или проверяется
        ('shipped', 'Отправлен'),  # Статус: заказ передан в службу доставки
        ('delivered', 'Доставлен'),  # Статус: клиент получил заказ
        ('cancelled', 'Отменён'),  # Статус: заказ был аннулирован
    ]

    user = models.ForeignKey(  # Связь с пользователем (многие заказы к одному юзеру)
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,  # При удалении юзера заказ остается (null)
        null=True, blank=True, related_name='orders',  # Поле может быть пустым, доступ через user.orders
        verbose_name='Пользователь'  # Читаемое название поля в админке
    )
    first_name = models.CharField('Имя', max_length=100)  # Текстовое поле для имени покупателя
    last_name = models.CharField('Фамилия', max_length=100)  # Текстовое поле для фамилии покупателя
    email = models.EmailField('Email')  # Поле для адреса электронной почты с валидацией
    phone = models.CharField('Телефон', max_length=20)  # Поле для контактного номера телефона
    address = models.TextField('Адрес')  # Большое текстовое поле для адреса доставки
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')  # Статус с выбором
    created_at = models.DateTimeField('Создан', auto_now_add=True)  # Дата создания, ставится один раз автоматически
    updated_at = models.DateTimeField('Обновлён', auto_now=True)  # Дата обновления, меняется при каждом сохранении
    total_price = models.DecimalField('Итого', max_digits=10, decimal_places=2, default=0)  # Итоговая сумма заказа

    class Meta:  # Конфигурация отображения модели
        verbose_name = 'Заказ'  # Название модели в единственном числе
        verbose_name_plural = 'Заказы'  # Название модели во множественном числе
        ordering = ['-created_at']  # Сортировка списка: сначала самые новые заказы

    def __str__(self):  # Метод для строкового представления объекта
        return f"Заказ #{self.id} — {self.get_full_name()}"  # Возвращает номер и имя клиента

    def get_full_name(self):  # Метод для объединения имени и фамилии
        return f"{self.first_name} {self.last_name}"  # Возвращает строку с полным именем

    def update_total(self):  # Метод для пересчета общей стоимости заказа
        self.total_price = sum(item.get_total_cost() for item in self.items.all())  # Суммирует стоимость всех позиций
        self.save()  # Сохраняет обновленную сумму в базу данных


class OrderItem(models.Model):  # Определение модели отдельной позиции в заказе
    order = models.ForeignKey(  # Связь с моделью заказа (многие позиции к одному заказу)
        Order, on_delete=models.CASCADE, related_name='items',  # При удалении заказа удаляются и его позиции
        verbose_name='Заказ'  # Название связи в интерфейсе
    )
    product = models.ForeignKey(  # Связь с конкретным товаром
        Product, on_delete=models.CASCADE, related_name='orderitem',  # Ссылка на товар из каталога
        verbose_name='Товар'  # Название поля товара
    )
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)  # Цена товара на момент покупки
    quantity = models.PositiveIntegerField('Количество', default=1)  # Количество единиц товара

    class Meta:  # Конфигурация отображения позиции заказа
        verbose_name = 'Позиция заказа'  # Понятное имя в единственном числе
        verbose_name_plural = 'Позиции заказов'  # Понятное имя во множественном числе

    def __str__(self):  # Строковое описание позиции
        return f"{self.product.name} x {self.quantity}"  # Возвращает "Название товара x кол-во"

    def get_total_cost(self):  # Метод для расчета стоимости конкретной позиции
        return self.price * self.quantity  # Умножает цену за единицу на количество