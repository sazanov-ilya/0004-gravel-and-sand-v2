from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    """ Класс формы регистрации пользователя """
    # прописываем все поля формы
    # уточнить как прописать объекты bootstrap
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control '}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    """ Класс формы авторизации пользователя """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control '}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))