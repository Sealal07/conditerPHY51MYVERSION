from django.urls import path # Импорт функции для определения путей
from . import views # Импорт наших представлений (контроллеров)

app_name = 'catalog' # Пространство имен для URL (используется как catalog:home)

urlpatterns = [
    path('', views.home_view, name='home'), # Главная страница приложения
    path('categories/', views.category_list_view, name='category_list'), # Все категории
    path('categories/<slug:slug>/', views.category_detail_view, name='category_detail'), # Конкретная категория
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'), # Карточка товара
    path('promotions/', views.promotions_view, name='promotions'), # Страница акций
]