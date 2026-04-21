from django.shortcuts import render, redirect  # Функции для отображения страниц и перенаправлений
from django.contrib import admin  # Модуль админки Django
from django.utils.safestring import mark_safe  # Функция для вставки "сырого" HTML (для картинок)
from .models import Category, Product, ProductImage  # Импорт моделей
from .forms import ExcelImportForm  # Форма для загрузки файла Excel


class ProductImageInline(admin.TabularInline):  # Возможность добавлять картинки прямо в карточке товара
    model = ProductImage  # Какая модель используется
    extra = 1  # Количество пустых полей для новых картинок
    fields = ('image', 'is_main', 'image_preview')  # Поля, которые будут видны
    readonly_fields = ('image_preview',)  # Поле превью нельзя редактировать вручную

    def image_preview(self, obj):  # Метод для генерации HTML-кода картинки
        if obj.image:  # Если файл загружен
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')  # Возвращаем тег img
        return ''  # Иначе пусто
    image_preview.short_description = 'Превью'  # Заголовок колонки в админке


@admin.register(Category)  # Регистрация модели Категория
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')  # Столбцы в списке категорий
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение слага при вводе имени
    list_filter = ('is_active',)  # Фильтр справа по активности
    search_fields = ('name',)  # Поиск по имени


class ProductImageAdmin(admin.ModelAdmin):  # Отдельное управление изображениями
    list_display = ('product', 'image_preview', 'is_main')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return ''
    image_preview.short_description = 'Превью'


admin.site.register(ProductImage, ProductImageAdmin)  # Регистрация админки картинок


class ProductImageMultiInline(admin.StackedInline):  # Альтернативный вид отображения вложенных картинок
    model = ProductImage
    extra = 3  # Сразу 3 пустых поля
    fields = ('image', 'is_main')


@admin.register(Product)  # Регистрация модели Товар
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_percent',
                    'is_active', 'created_at')  # Поля в списке товаров
    list_filter = ('category', 'is_active', 'discount_percent')  # Фильтры
    search_fields = ('name', 'description')  # Где искать товар
    prepopulated_fields = {'slug': ('name',)}  # Генерация слага
    inlines = [ProductImageMultiInline]  # Подключаем вложенные картинки
    list_editable = ('price', 'discount_percent', 'is_active')  # Можно менять прямо в списке

    # Указываем свой шаблон для списка товаров (чтобы добавить кнопку импорта)
    change_list_template = 'admin/catalog/product/change_list_import.html'

    def get_urls(self):  # Добавление кастомных URL в админку
        from django.urls import path
        urls = super().get_urls()  # Получаем стандартные URL
        custom_urls = [  # Добавляем наш путь для импорта
            path('import-excel/', self.admin_site.admin_view(self.import_excel_view), name='catalog_product_import_excel'),
        ]
        return custom_urls + urls  # Наш путь идет первым

    def import_excel_view(self, request):  # Логика страницы импорта
        from .import_excel import import_from_excel  # Ленивый импорт функции обработки
        if request.method == 'POST':  # Если форму отправили
            form = ExcelImportForm(request.POST, request.FILES)  # Загружаем данные в форму
            if form.is_valid():  # Если файл корректный
                excel_file = request.FILES['excel_file']  # Получаем сам файл
                result = import_from_excel(excel_file)  # Запускаем функцию обработки из import_excel.py
                self.message_user(request, result)  # Выводим сообщение пользователю
                return redirect('..')  # Возвращаемся в список товаров
        else:
            form = ExcelImportForm()  # Если просто зашли на страницу — пустая форма
        return render(request, 'admin/catalog/product/import_excel.html', {  # Рендерим шаблон
            'form': form,
            'title': 'Импорт товаров из Excel',
        })