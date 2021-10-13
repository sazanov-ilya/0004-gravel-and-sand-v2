import json

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
# from app_first__gravel_and_sand.models import Products, Orders
# from app_first__gravel_and_sand.serializers import ProductsSerializer
from ..models import Products, Orders
from ..serializers import ProductsSerializer


class ProductsApiTestCase(APITestCase):
    # запускается каждый раз при старте каждого из тестов
    def setUp(self):
        # создаем пользователя
        self.user = User.objects.create(username='test_username')
        # создаем тестовый набор
        self.product_1 = Products.objects.create(product_name='Test product 1',
                                                 product_unit='unit 1',
                                                 product_price='3000',
                                                 product_description='product 1 description')
        self.product_2 = Products.objects.create(product_name='Test product 2',
                                                 product_unit='unit 2',
                                                 product_price='4000',
                                                 product_description='product 2 description')
        self.product_3 = Products.objects.create(product_name='Test product 3',
                                                 product_unit='unit 1',
                                                 product_price='5000',
                                                 product_description='product 3 description, product 1')
        self.product_4 = Products.objects.create(product_name='Aest product 4',
                                                 product_unit='unit 1',
                                                 product_price='4000',
                                                 product_description='product 4 description')

    def test_get_products_list(self):
        # динамическая ссылка на СПИСОК по url из urls.py
        url = reverse('get_all_products-list')
        #url = 'http://127.0.0.1:8000/get_all_products/?format=json'
        #print(url)
        #print(response)
        #print(response.data)
        response = self.client.get(url)
        serializer_data = ProductsSerializer([self.product_1, self.product_2, self.product_3, self.product_4],
                                             many=True).data
        # проверяем ответ
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # проверяем данные
        self.assertEqual(serializer_data, response.data)

    def test_search_products_list(self):
        url = reverse('get_all_products-list')
        response = self.client.get(url, data={'search': 'product 1'})
        serializer_data = ProductsSerializer([self.product_1, self.product_3], many=True).data
        # проверяем ответ
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # проверяем данные
        self.assertEqual(serializer_data, response.data)

    def test_filter_products_list(self):
        url = reverse('get_all_products-list')
        response = self.client.get(url, data={'product_price': '4000'})
        serializer_data = ProductsSerializer([self.product_2, self.product_4], many=True).data
        # проверяем ответ
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # проверяем данные
        self.assertEqual(serializer_data, response.data)

    def test_ordering_products_list(self):
        url = reverse('get_all_products-list')
        response = self.client.get(url, data={'ordering': 'product_name'})
        serializer_data = ProductsSerializer([self.product_4, self.product_1, self.product_2, self.product_3],
                                             many=True).data
        # проверяем ответ
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # проверяем данные
        self.assertEqual(serializer_data, response.data)

    def test_create_products_list(self):
        # проверяем число записей до создания
        self.assertEqual(4, Products.objects.all().count())

        # создаем новую запись
        url = reverse('get_all_products-list')
        data = {
            'product_name': 'test_create_products_list',
            'product_unit': 'тонна',
            'product_price': '3000.00',
            'product_description': 'тест создания нового продукта'
        }
        json_data = json.dumps(data)
        # авторизация
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        # проверяем ответ
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # можно добавить проверку, что новая записи была создана с переданными значениями полей

        # проверяем число записей после создания
        self.assertEqual(5, Products.objects.all().count())

    def test_update_products_list(self):
        # добавляем в ссылку id записи для обновления
        url = reverse('get_all_products-detail', args=(self.product_1.product_id,))
        data = {
            'product_name': self.product_1.product_name,
            'product_unit': self.product_1.product_unit,
            'product_price': '3500.00',
            'product_description': self.product_1.product_description
        }
        json_data = json.dumps(data)
        # авторизация
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        # проверяем ответ
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class OrdersApiTestCase(APITestCase):
    # запускается каждый раз при старте каждого из тестов
    def setUp(self):
        # создаем пользователя
        self.user = User.objects.create(username='test_username')

        print('UserCount')
        print(User.objects.all().count())
        print('ALL')
        print(User.objects.all())
        print('User.id')
        print(self.user.id)
        print('END')


        # создаем тестовый набор
        self.orders_1 = Orders.objects.create(user_id=self.user.id,
                                              order_date=timezone.now(),
                                              order_name='order 1 test',
                                              order_phone='phone 1 test',
                                              product_id=1,
                                              order_count=2,
                                              area_id=1,
                                              order_address='address 1 test',
                                              order_date_delivery='2021-07-27',
                                              order_time_delivery='19:09:24',
                                              order_description='description 1 test',
                                              order_cost=500,
                                              status_id=2)


    #def test_get_products_list(self):
    #    # динамическая ссылка на СПИСОК по url из urls.py
    #    url = reverse('get_all_products-list')
    #    #url = 'http://127.0.0.1:8000/get_all_products/?format=json'
    #    #print(url)
    #    #print(response)
    #    #print(response.data)
    #    response = self.client.get(url)
    #    serializer_data = ProductsSerializer([self.product_1, self.product_2, self.product_3, self.product_4],
    #                                         many=True).data
    #    # проверяем ответ
    #    self.assertEqual(status.HTTP_200_OK, response.status_code)
    #    # проверяем данные
    #    self.assertEqual(serializer_data, response.data)

    def test_create_order(self):
        # проверяем число записей до создания
        self.assertEqual(1, Orders.objects.all().count())

        # создаем новую запись
        url = reverse('save_new_order-list')
        data = {
            'user_id': self.user.id,
            'order_date': timezone.now(),
            'order_name': 'order 2 test',
            'order_phone': 'phone 2 test',
            'product_id': 1,
            'order_count': 2,
            'area_id': 1,
            'order_address': 'address 2 test',
            'order_date_delivery': '2021-07-27',
            'order_time_delivery': '19:09:24',
            'order_description': 'description 2 test',
            'order_cost': 500,
            'status_id': 2
        }
        json_data = json.dumps(data)
        # авторизация
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        # проверяем ответ
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # можно добавить проверку, что новая запись была создана с переданными значениями полей

        # проверяем число записей после создания
        self.assertEqual(2, Orders.objects.all().count())



