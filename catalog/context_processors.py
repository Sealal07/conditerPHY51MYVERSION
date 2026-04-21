from .models import Category # Импорт модели категорий

def categories_context(request):
    """
    Позволяет переменной 'nav_categories' быть доступной в любом шаблоне (например, в меню).
    """
    return {
        # Возвращаем только активные категории для навигации
        'nav_categories': Category.objects.filter(is_active=True),
    }