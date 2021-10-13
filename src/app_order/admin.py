# Register your models here.
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Products, Areas, OrderStatus, Orders, ProductUnit


@admin.register(ProductUnit)
class ProductsAdmin(ModelAdmin):
    """ Настройки отображения в адимнке """
    list_display = ('unit_id', 'unit_name')
    list_display_links = ('unit_id', 'unit_name')  # Ссылка для переходя на элемент
    search_fields = ('unit_name',)  # Поиск по полям


@admin.register(Products)
class ProductsAdmin(ModelAdmin):
    """ Настройки отображения в адимнке """
    list_display = ('product_id', 'product_name', 'product_unit', 'product_price', 'product_description')
    list_display_links = ('product_id', 'product_name')  # Ссылка для переходя на элемент
    search_fields = ('product_name', 'product_description')  # Поиск по полям
    prepopulated_fields = {'slug': ('product_name',)}  # автозаполнение слага в админке


@admin.register(Areas)
class AreasAdmin(ModelAdmin):
    """ Настройки отображения в адимнке """
    list_display = ('area_id', 'area_name', 'area_price', 'area_description')
    list_display_links = ('area_id', 'area_name')  # Ссылка для переходя на элемент
    search_fields = ('area_name', 'area_description')  # Поиск по полям
    prepopulated_fields = {'slug': ('area_name',)}  # автозаполнение слага в админке


@admin.register(OrderStatus)
class OrderStatusAdmin(ModelAdmin):
    """ Настройки отображения в адимнке """
    list_display = ('status_id', 'status_name')
    list_display_links = ('status_id', 'status_name')  # Ссылка для переходя на элемент
    search_fields = ('status_name', )  # Поиск по полям
    prepopulated_fields = {'slug': ('status_name',)}  # автозаполнение слага в админке


@admin.register(Orders)
class OrdersAdmin(ModelAdmin):
    """ Настройки отображения в адимнке """
    list_display = ('order_id', 'user_id', 'order_date', 'order_name', 'order_phone',
                    'product_id', 'order_address')
    list_display_links = ('order_id', 'user_id')
    search_fields = ('order_id', 'user_id', 'area_id')




#admin.site.register(Areas)
#admin.site.register(Orders)
