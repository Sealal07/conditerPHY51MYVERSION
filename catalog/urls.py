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