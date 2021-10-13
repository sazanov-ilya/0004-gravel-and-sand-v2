from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import CreateView

# from django.contrib.auth.models import User
from app_users.forms import RegisterUserForm, LoginUserForm


class RegisterUser (CreateView):
    """ Класс формы регистрации пользователя """
    # form_class = UserCreationForm  # базовая форма django для регистрации
    form_class = RegisterUserForm  # своя форма из forms.py
    template_name = 'user/user/base_register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """ После успешной регистрации сразу авторизуем """
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


class LoginUser (LoginView):
    """ Класс формы автризации пользователя """
    # form_class = AuthenticationForm  # базовая форма django для авторизации
    form_class = LoginUserForm  # своя форма из forms.py
    template_name = 'user/user/base_login.html'
    success_url = reverse_lazy('login')  # Перенаправление при успешной авторизации

    def get_success_url(self):
        """ Перенаправление при успешной авторизации """
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
