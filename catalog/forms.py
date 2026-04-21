from django import forms


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label='Excel файл', help_text='Файл с листами: category, products')


class ProductSearchForm(forms.Form):
    q = forms.CharField(label='Поиск', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Поиск товаров...', 'class': 'w-full border rounded px-3 py-2'}
    ))