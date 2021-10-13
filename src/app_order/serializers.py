from rest_framework.serializers import ModelSerializer

#from app_first__gravel_and_sand.models import Products, Areas, Orders
from .models import Products, Areas, Orders


class ProductsSerializer(ModelSerializer):
    """ Для данных по товарам """
    class Meta:
        model = Products
        fields = '__all__'
        # fields = ('product_id', 'product_name')


class ProductsSerializerInfo(ModelSerializer):
    """ Для списка на форме """
    class Meta:
        model = Products
        fields = ('product_id', 'product_name', 'product_unit', 'product_price')


class AreasSerializer(ModelSerializer):
    """ Для данных по районам """
    class Meta:
        model = Areas
        fields = '__all__'


class OrdersSerializer(ModelSerializer):
    """ Для данных по заказам """
    class Meta:
        model = Orders
        fields = '__all__'


class OrdersSerializerInfo(ModelSerializer):
    """ Для списка на форме """
    class Meta:
        model = Products
        fields = ('order_id', 'user_id', 'order_date', 'order_name', 'order_phone',
                  'product_id', 'order_count', 'area_id')
