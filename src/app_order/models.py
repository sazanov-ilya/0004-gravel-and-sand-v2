import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from django.utils.timezone import now


class ProductUnit (models.Model):
    """ Класс модели ед. измерения продуктов """
    unit_id = models.AutoField('ID', primary_key=True)
    unit_name = models.CharField('Наименование единицы измерения', max_length=200, db_index=True)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
        # ordering = ['unit_id', 'unit_name']

    def __str__(self):
        # return f'unit_id: {self.unit_id}, unit_name: {self.unit_name}'
        return self.unit_name


class Products(models.Model):
    """ Класс модели продуктов """
    product_id = models.AutoField('ID', primary_key=True)
    product_date_create = models.DateTimeField('Дата создания', auto_now_add=True)
    product_date_update = models.DateTimeField('Дата обновления', auto_now=True)
    product_name = models.CharField('Наименование продукта', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True, db_index=True)
    product_photo = models.ImageField('Фото', upload_to='product_photos/%Y/%m/%d/', null=True, blank=True)
    product_unit = models.ForeignKey('ProductUnit', db_column="unit_id", default=1, on_delete=models.PROTECT)
    product_price = models.DecimalField('Цена за ед.', max_digits=10, decimal_places=2)
    product_description = models.TextField('Описание продукта')
    product_is_published = models.BooleanField('Публикация', default=False)
    product_date_published = models.DateTimeField('Дата публикации', null=True, blank=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        # ordering = ['product_id']

    # изменить Дату публикации, когда значение product_is_published равно True
    def __init__(self, *args, **kwargs):
        super(Products, self).__init__(*args, **kwargs)
        self._product_is_published = self.product_is_published

    def save(self, *args, **kwargs):
        if not self._product_is_published and self.product_is_published:
            self.pub_date = timezone.now()
        super(Products, self).save(*args, **kwargs)
    # изменить Дату публикации, когда значение product_is_published равно True

    def __str__(self):
        # return f'product_id: {self.product_id}, product_name: {self.product_name}'
        return self.product_name

    def get_absolute_url(self):
        """ Процедура возвращает абсолюбный маршрут на конкрктную запись, котрый можно использовать в шаблоне """
        # return reverse('orders_by_status', kwargs={'status_id': self.status_id})
        return reverse('product', kwargs={'product_slug': self.slug})


class Areas(models.Model):
    """ Класс модели районов """
    area_id = models.AutoField('ID', primary_key=True)
    area_name = models.CharField('Наименование района', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True, db_index=True)
    area_price = models.DecimalField('Стоимость доставки', default=0, max_digits=10, decimal_places=2, blank=True)
    area_description = models.TextField('Описание района')

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'
        # ordering = ['area_id', 'area_name']

    def __str__(self):
        # return f'area_id {self.area_id}, area_name: {self.area_name}'
        return self.area_name


class OrderStatus(models.Model):
    """ Класс модели статусов заказов """
    status_id = models.AutoField('ID', primary_key=True)
    status_name = models.CharField('Наименование статуса', max_length=200, db_index=True)
    slug = models.SlugField('Slug', max_length=200, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'
        # ordering = ['status_id', 'status_name']

    def __str__(self):
        # return f'status_id: {self.status_id}, status_name: {self.status_name}'
        return self.status_name

    def get_absolute_url(self):
        """ Процедура возвращает абсолюбный маршрут на конкрктную запись, котрый можно использовать в шаблоне """
        # return reverse('orders_by_status', kwargs={'status_id': self.status_id})
        return reverse('orders_by_status', kwargs={'status_slug': self.slug})


class Orders(models.Model):
    """ Таблица заказов
     Доступно обновление только статуса """
    order_id = models.AutoField('ID', primary_key=True)
    user = models.ForeignKey(User, db_column="id", on_delete=models.CASCADE)
    order_date = models.DateTimeField('Дата заказа', auto_now_add=True)
    order_timezone = models.CharField('Timezone', max_length=6)
    order_name = models.CharField('Имя заказчика', max_length=200)
    order_phone = models.CharField('Телефон заказчика', max_length=200)
    product = models.ForeignKey(Products, db_column="product_id", on_delete=models.CASCADE)
    order_count = models.IntegerField('Количество')
    area = models.ForeignKey(Areas, db_column="area_id", on_delete=models.CASCADE)
    order_address = models.CharField('Адрес доставки', max_length=500)
    order_date_delivery = models.DateField('Дата доставки')
    order_time_delivery = models.TimeField('Время доставки')
    order_description = models.TextField('Описание заказа', null=True, blank=True)
    order_cost = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
    # Не даст удалить статус, пока есть заказы по нему - on_delete=models.PROTECT
    status = models.ForeignKey('OrderStatus', db_column="status_id", default=2, on_delete=models.PROTECT)
    status_date = models.DateTimeField('Дата статуса', default=timezone.now())

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        # ordering = ['order_id', 'order_name']

    # обновление даты смены статуса
    def __init__(self, *args, **kwargs):
        super(Orders, self).__init__(*args, **kwargs)
        self._status = self.status

    def save(self, *args, **kwargs):
        if self._status != self.status:
            self.status_date = timezone.now()
        super(Orders, self).save(*args, **kwargs)
    # конец - обновление даты смены статуса

    def __str__(self):
        # return f'order_id: {self.order_id}, order_name: {self.order_name}'
        return str(self.order_id)

    def get_absolute_url(self):
        """ Процедура возвращает абсолюбный маршрут на конкрктную запись, котрый можно использовать в шаблоне """
        return reverse('order', kwargs={'order_id': self.order_id})

    def is_overdue_order(self):
        """ Проверка на просроченный заказ
        Если через 1 час после создания, заявка все еще в статуса Новый или Не определено
        """
        return self.status_id in (1, 2) and (self.order_date >= (timezone.now() - datetime.timedelta(hours=1)))
