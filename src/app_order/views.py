from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator  # AddProductView, только для админа

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, ListView, DetailView, CreateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import User

from .models import Products, Areas, Orders, OrderStatus
from .forms import AddOrderForm, AddProductForm
from .serializers import ProductsSerializer, AreasSerializer, OrdersSerializer
from .utils import OrderContext


class ProductsViewSet(ModelViewSet):
    """ Для списков продуктов """
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Все только для авторизованных пользователей
    # permission_classes = [IsAuthenticated]
    # Получать могут все, менять только авторизованные
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_fields = ['product_id']
    search_fields = ['product_name', 'product_price', 'product_description']
    ordering_fields = ['product_price', 'product_name']
    http_method_names = ['get', ]


class AreasViewSet(ModelViewSet):
    """ Для списков районов """
    queryset = Areas.objects.all()
    serializer_class = AreasSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Все только для авторизованных пользователей
    # permission_classes = [IsAuthenticated]
    # Получать могут все, менять только авторизованные
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_fields = ['area_id']
    search_fields = ['area_name', 'area_price', 'area_description']
    ordering_fields = ['area_price', 'area_name']
    http_method_names = ['get', ]


class OrdersViewSet(ModelViewSet):
    """ Для списков заказов (реализовать добавление нового заказа тут через post)"""
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Все только для авторизованных пользователей
    # permission_classes = [IsAuthenticated]
    # Получать могут все, менять только авторизованные
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_fields = ['order_id']
    search_fields = ['order_date', 'order_name', 'order_phone']
    ordering_fields = ['order_id', 'order_date']
    http_method_names = ['get', ]

    def perform_create(self, serializer):
        """ Переопределяем метод, добавляем дополнительные поля, которых нет с формы """
        serializer.validated_data['user_id'] = self.request.user
        serializer.save()


# def home(request):
#    """ Домашняя страница (вызов через клмк по логотипу)"""
#    return HttpResponse('home')


def page_not_found(request, exception):
    """ Страница не найдена (возвращаем с кодом 404) """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def home(request):
    """ Домашняя страница (вызов через клмк по логотипу)
    Можно использовать как общую старницу для всего сайта"""
    # test = OrderStatus.objects.annotate(total=Count('orders')).filter(total__gt=0)
    # # Products.objects.values('unit_id').annotate(Count('product_id'))
    # print(test)

    return redirect('about')


def about(request):
    """ Страница о сайте
     Можно использовать как главную страницу приложения"""
    context = {}
    # return render(request, 'order/order/about.html', context={'menu': menu})
    return render(request, 'order/order/about.html', context=context)


class ShowProductsView(ListView):
    # ListView - базовый класс для отображения списков
    """ Класс для формы списка всех продуктов """
    paginate_by = 3  # Количество записей на странице - перенести в миксины
    model = Products  # Выбирает все записи и пытается отобразить списком
    template_name = 'order/order/products.html'  # По умолчанию <имя приложения>/<имя модели>_list.html
    context_object_name = 'products'  # Именованный массив для шаблона (по умолчанию object_list)
    extra_context = {'title': 'Список продуктов'}  # Только статический контекст

    # def get_context_data(self, *, object_list=None, **kwargs):
    #    """ Добавляем статический и динамический контекст """
    #    ! Общмй код для нескольких view выносим в миксины, файл -> utils.py
    #    !!! сейчас через пользовательский тег """
    #    # получаем текущий контент
    #    context = super().get_context_data(**kwargs)
    #    context['menu'] = menu
    #    context['title'] = 'Список продуктов'
    #    context['status_selected'] = 0
    #    return context  # и возвращаем контекст

    def get_queryset(self):
        """ Фильтр на списко данных """
        # Избавляемся от дублирующих запросов
        # .select_related('product_unit')
        # - подгрузка данных связанной модели по внешнему ключу один ко многим (ForeignKey)
        # .prefetch_related('product_unit')
        # - подгрузка данных связанной модели по внешнему ключу многие ко многим ()
        return Products.objects.select_related('product_unit').filter(product_is_published=True).order_by('product_name')


class ShowProductView(DetailView):
    # DetailView - базовый класс для отображения одной записи
    """ Класс формы для страницы вывода данных по продукту """
    model = Products
    template_name = 'order/order/product.html'
    # pk_url_kwarg = "order_id"  # для pk
    slug_url_kwarg = 'product_slug'  # для слага
    # query_pk_and_slug = True
    context_object_name = 'product'  # имя переменной для шаблона


@method_decorator(staff_member_required, name='dispatch')
class AddProductView(CreateView):
    # CreateView - базовый класс для добавления новой записи (работает с формами, в не моделями)
    """ Класс формы для страницы добавление нового продукта """
    form_class = AddProductForm
    template_name = 'order/order/new_product.html'
    # success_url = reverse_lazy('home')  # или по умолчанию get_absolute_url из модели

    # def get_context_data(self, *, object_list=None, **kwargs):
    #    """ Добавляем статический и динамический контекст """
    #    !!! сейчас через пользовательский тег """
    #    # получаем текущий контент
    #    context = super().get_context_data(**kwargs)
    #    # добавляем свой контент, например, список меню
    #    context['menu'] = menu
    #    context['title'] = 'Новый продукт'
    #    return context  # и возвращаем контекст


# ДАЛЕЕ - заказы
class ShowOrdersAllView(LoginRequiredMixin, OrderContext, ListView):
    # ListView - базовый класс для отображения списков
    # OrderContext - миксины для заказов
    """ Класс для формы списка всех заказов """
    model = Orders  # Mодель по которой выводим данные
    template_name = 'order/order/orders.html'  # По умолчанию <имя приложения>/<имя модели>_list.html
    context_object_name = 'orders'  # Именованный массив для шаблона (по умолчанию object_list)
    login_url = 'login'  # Или в settings.py
    # extra_context = {'title': 'Все заказы'}  # можно передавать только статический контекст

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Добавляем статический и динамический контекст """
        context = super().get_context_data(**kwargs)  # Получаем текущий контент как словарь
        # context['menu'] = menu  # Пользовательский тег
        # context['status_selected'] = 0  # По умолчанию 0

        # ! Общмй код для нескольких view выносим в миксины, файл -> utils.py
        mixin = self.get_order_context(title='Все заказы')  # Вызываем и передаем начальный контекст

        return dict(list(context.items()) + list(mixin.items()))  # Объединяем словари

    def get_queryset(self):
        """ Фильтр на список данных """
        # добавить провкрку на авторизованного пользователя
        # и для суперадминов все заказы по всем (также добавить список пользователей)


        print('ShowOrdersAllView', self.request.user.id)

        return Orders.objects.select_related('product', 'status').filter(
            user=self.request.user).order_by('order_id')

        # return Orders.objects.select_related('product', 'status').filter(
        #     status__slug=self.kwargs['status_slug']).order_by('order_id')


class ShowOrdersByStatusView(LoginRequiredMixin, OrderContext, ListView):
    # ListView - базовый класс для отображения списков
    # OrderContext - миксины для заказов
    """ Класс для формы списка всех заказов по выбранному статусу """
    model = Orders  # Модель данных
    template_name = 'order/order/orders.html'  # По умолчанию <имя приложения>/<имя модели>_list.html
    context_object_name = 'orders'  # Именованный массив для шаблона (по умолчанию object_list)
    login_url = 'login'  # Или в settings.py
    allow_empty = False  # Если данных нет, то исключение 404

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Добавляем статический и динамический контекст """
        context = super().get_context_data(**kwargs)  # Получаем текущий контент как словарь
        # context['title'] = 'Заказы в статусе: ' + str(context['orders'][0].status)
        # context['menu'] = menu  # Пользовательский тег
        # context['status_selected'] = context['orders'][0].status_id  #  Передаем в миксин

        # ! Общий код для нескольких view выносим в миксины, файл -> utils.py
        mixin = self.get_order_context(title='Заказы в статусе: ' + str(context['orders'][0].status),
                                       status_selected=context['orders'][0].status_id)

        # Избавляемся от отложенных дублирующих запросов
        # status = OrderStatus.objects.get(slug=self.kwargs['status_slug'])
        # mixin = self.get_order_context(title='Заказы в статусе: ' + str(status.status_name),
        #                                status_selected=status.status_id)

        return dict(list(context.items()) + list(mixin.items()))  # Объединяем словари

    def get_queryset(self):
        """ Фильтр на список данных """
        # Добавить провкрку на авторизованного пользователя
        # и для суперадминов все заказы по всем (также добавить список пользователей)
        # status__slug - проверка по полю слаг slug связанной модели OrderStatus через ключ status

        # print(self.request.user.id)

        return Orders.objects.select_related('product', 'status').filter(
            user=self.request.user, status__slug=self.kwargs['status_slug']).order_by('order_id')


class ShowOrderView(LoginRequiredMixin, OrderContext, DetailView):
    # DetailView - базовый класс для отображения одной записи
    # OrderContext - миксины для заказов
    """ Класс для формы с данными по заказу """
    model = Orders
    template_name = 'order/order/order.html'
    pk_url_kwarg = "order_id"  # Для pk
    # slug_url_kwarg = 'slug'  # Для слага
    # query_pk_and_slug = True
    context_object_name = 'order'  # Имя переменной для шаблона
    login_url = 'login'  # Или в settings.py

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Добавляем статический и динамический контекст """
        # Получаем текущий контент как словарь
        context = super().get_context_data(**kwargs)
        # Добавляем параметры в контекст
        # context['title'] = 'Заказы в статусе: ' + str(context['orders'][0].status)
        # context['menu'] = menu  # Пользовательский тег
        # context['status_selected'] = context['orders'][0].status_id  #  Передаем в миксин

        # ! Общий код для нескольких view выносим в миксины, файл -> utils.py
        mixin = self.get_order_context(title='Данные по заказу № : ' + str(context['order'].order_id))

        # Возвращаем контекст
        return dict(list(context.items()) + list(mixin.items()))  # Объединяем словари


class AddOrderView(LoginRequiredMixin, CreateView):
    # CreateView - базовый класс для добавления новой записи (работает с формами, в не моделями)
    # LoginRequiredMixin - базовый миксин для проверки авторизации
    """ Класс для формы добавлеия нового заказа """
    form_class = AddOrderForm
    template_name = 'order/order/new_order_form.html'
    extra_context = {'title': 'Новый заказ'}  # Только статический контекст
    # success_url = reverse_lazy('home')  # Или по умолчанию get_absolute_url из модели
    login_url = 'login'  # Или в settings.py

    def form_valid(self, form):
        """ Переопределяем метод, добавляем пользователя """
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


def archive(request, year):
    """ Архив по годам - пример маски в запросе """
    if int(year) > 2020:
        raise Http404()
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")
