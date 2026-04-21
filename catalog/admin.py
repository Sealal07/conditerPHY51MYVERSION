from django.shortcuts import render, redirect
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage
from .forms import ExcelImportForm


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return ''
    image_preview.short_description = 'Превью'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    search_fields = ('name',)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'is_main')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return ''
    image_preview.short_description = 'Превью'


admin.site.register(ProductImage, ProductImageAdmin)


class ProductImageMultiInline(admin.StackedInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'is_main')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_percent',
                    'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'discount_percent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageMultiInline]
    list_editable = ('price', 'discount_percent', 'is_active')

    change_list_template = 'admin/catalog/product/change_list_import.html'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel_view), name='catalog_product_import_excel'),
        ]
        return custom_urls + urls

    def import_excel_view(self, request):
        from .import_excel import import_from_excel
        if request.method == 'POST':
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = request.FILES['excel_file']
                result = import_from_excel(excel_file)
                self.message_user(request, result)
                return redirect('..')
        else:
            form = ExcelImportForm()
        return render(request, 'admin/catalog/product/import_excel.html', {
            'form': form,
            'title': 'Импорт товаров из Excel',
        })