"""gravel_and_sand URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from .views import ProductsViewSet, AreasViewSet, OrdersViewSet, \
    ShowProductsView, ShowProductView, AddProductView, \
    ShowOrdersAllView, ShowOrdersByStatusView, ShowOrderView, AddOrderView, about, archive

router = SimpleRouter()

router.register(r'get_products', ProductsViewSet, basename='get_products')
router.register(r'get_areas', AreasViewSet, basename='get_areas')
router.register(r'get_orders', OrdersViewSet, basename='get_orders')

urlpatterns = [
    # path('admin/', admin.site.urls),
    # url('', include('social_django.urls', namespace='social')),
    # path('auth/', auth, name='auth/'),

    path('', about, name='about'),

    # Список всех продуктов
    # http://127.0.0.1:8000/orders/products/
    path('products/', ShowProductsView.as_view(), name='products'),  # класс

    # Данные по продукту
    # http://127.0.0.1:8000/orders/product/pesok/
    path('product/<slug:product_slug>/', ShowProductView.as_view(), name='product'),  # класс и slug

    # Новый продукт
    # http://127.0.0.1:8000/orders/new_product/
    path('new_product/', AddProductView.as_view(), name='new_product'),  # класс

    # Список всех заказов
    # http://127.0.0.1:8000/orders/orders/
    path('orders/', ShowOrdersAllView.as_view(), name='orders'),  # класс

    # Список заказов по статусу
    # http://127.0.0.1:8000/orders/orders/novyj/
    path('orders/<slug:status_slug>/', ShowOrdersByStatusView.as_view(), name='orders_by_status'),  # класс и slug

    # Данные по заказу
    # http://127.0.0.1:8000/orders/order/4/
    path('order/<int:order_id>/', ShowOrderView.as_view(), name='order'),  # класс

    # Новый заказ
    # http://127.0.0.1:8000/orders/new_order_form/
    path('new_order_form/', AddOrderView.as_view(), name='new_order_form'),  # класс

    # пример шаблона ссылки п датой
    # http://127.0.0.1:8000/orders/archive/2020/
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive, name='archive'),
]

urlpatterns += router.urls








