from decimal import Decimal  # Импортируем Decimal для точных денежных расчетов
from catalog.models import Product  # Импортируем модель Product из приложения catalog
from decimal import Decimal  # Повторный импорт Decimal (можно удалить, так как уже импортирован выше)

class Cart:  # Определяем класс Cart для управления корзиной покупок
    def __init__(self, request):  # Конструктор класса, принимает request объект
        self.session = request.session  # Сохраняем сессию пользователя в атрибут объекта
        cart = self.session.get('cart')  # Пытаемся получить корзину из сессии по ключу 'cart'
        if not cart:  # Если корзины нет в сессии (None или пустая)
            cart = self.session['cart'] = {}  # Создаем пустой словарь для корзины и сохраняем в сессию
        self.cart = cart  # Сохраняем словарь корзины в атрибут объекта

    def add(self, product, quantity=1, update_quantity=False):  # Метод добавления товара в корзину
        product_id = str(product.id)  # Преобразуем ID товара в строку (для использования в качестве ключа)
        if product_id not in self.cart:  # Проверяем, есть ли уже такой товар в корзине
            self.cart[product_id] = {  # Если нет — создаем запись о товаре
                'quantity': 0,  # Начальное количество товара
                'price': str(product.price),  # Сохраняем цену как строку (для сериализации)
                'discount_percent': product.discount_percent,  # Сохраняем процент скидки
            }
        if update_quantity:  # Если передан флаг обновления количества
            self.cart[product_id]['quantity'] = quantity  # Устанавливаем точное количество товара
        else:  # Если флаг не передан
            self.cart[product_id]['quantity'] += quantity  # Добавляем количество к существующему
        self.save()  # Сохраняем изменения в сессии

    def remove(self, product):  # Метод удаления товара из корзины
        product_id = str(product.id)  # Преобразуем ID товара в строку
        if product_id in self.cart:  # Проверяем, есть ли товар в корзине
            del self.cart[product_id]  # Удаляем товар из словаря корзины
            self.save()  # Сохраняем изменения в сессии

    def save(self):  # Метод для сохранения изменений корзины в сессию
        self.session.modified = True  # Устанавливаем флаг изменения сессии (Django сохранит ее)

    def __iter__(self):  # Магический метод для итерации по корзине (например, в цикле for)
        product_ids = self.cart.keys()  # Получаем все ID товаров из корзины
        products = Product.objects.filter(id__in=product_ids)  # Получаем объекты товаров из БД по ID
        cart = self.cart.copy()  # Создаем копию словаря корзины (чтобы не изменять оригинал)
        for product in products:  # Перебираем все товары, полученные из БД
            cart[str(product.id)]['product'] = product  # Добавляем объект товара в данные корзины
        for item in cart.values():  # Перебираем все элементы корзины
            item['price'] = Decimal(item['price'])  # Преобразуем цену из строки в Decimal
            if item['discount_percent'] > 0:  # Проверяем, есть ли скидка на товар
                item['discount_price'] = item['price'] * (1 - item['discount_percent'] / 100)  # Рассчитываем цену со скидкой
            else:  # Если скидки нет
                item['discount_price'] = item['price']  # Цена со скидкой равна обычной цене
            item['total_price'] = item['discount_price'] * item['quantity']  # Рассчитываем общую стоимость для данного товара
            yield item  # Возвращаем элемент (делаем класс итерируемым)

    def __len__(self):  # Магический метод для получения длины корзины (количества уникальных товаров)
        return sum(item['quantity'] for item in self.cart.values())  # Возвращаем сумму всех количеств товаров

    def get_total_price(self):  # Метод для получения общей стоимости всех товаров в корзине
        return sum(  # Суммируем стоимости всех товаров
            Decimal(item['price']) * (Decimal('1') - Decimal(item['discount_percent']) / Decimal('100')) * item['quantity']
            # Формула: цена * (1 - скидка/100) * количество
            for item in self.cart.values()  # Перебираем все товары в корзине
        )

    def clear(self):  # Метод для полной очистки корзины
        del self.session['cart']  # Удаляем ключ 'cart' из сессии
        self.save()  # Сохраняем изменения (фактически удаляем корзину)
