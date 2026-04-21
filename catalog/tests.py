from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product
from decimal import Decimal

class CatalogTest(TestCase):
    def setUp(self):
        """Настройка начальных данных для тестов"""
        self.client = Client()
        self.category = Category.objects.create(
            name="Торты",
            slug="torty"
        )
        self.product = Product.objects.create(
            name="Медовик",
            category=self.category,
            price=Decimal('1000.00'),
            discount_percent=10,
            is_active=True
        )

    def test_category_creation(self):
        """Проверка корректности создания категории"""
        self.assertEqual(self.category.name, "Торты")
        self.assertEqual(str(self.category), "Торты")

    def test_discount_price_calculation(self):
        """Проверка вычисляемого свойства цены со скидкой"""
        # 1000 - 10% = 900
        self.assertEqual(self.product.discount_price, Decimal('900.00'))

    def test_homepage_status_code(self):
        """Проверка доступности главной страницы"""
        response = self.client.get(reverse('catalog:home'))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_view(self):
        """Проверка страницы конкретной категории"""
        url = reverse('catalog:category_detail', kwargs={'slug': self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Медовик") # Проверяем, что товар отобразился