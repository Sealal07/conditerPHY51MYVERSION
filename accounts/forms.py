from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # Добавляем телефон, так как его нет в стандартной форме
    phone = forms.CharField(label='Телефон', max_length=20, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Указываем только те поля, которые должны быть видимы,
        # КРОМЕ паролей (они добавятся автоматически от UserCreationForm)
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')