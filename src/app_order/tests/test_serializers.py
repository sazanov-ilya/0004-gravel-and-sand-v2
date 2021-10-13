from django.test import TestCase
from app_first__gravel_and_sand.models import Products
from app_first__gravel_and_sand.serializers import ProductsSerializer


class ProductsSerializerTestCase(TestCase):
    def test_products_serializer(self):
        product_1 = Products.objects.create(product_name='Песок', product_unit='тонна', product_price='3000',
                                            product_description='Песок как песок')
        product_2 = Products.objects.create(product_name='Щебень', product_unit='тонна', product_price='4000',
                                            product_description='Щебень обычный')
        data = ProductsSerializer([product_1, product_2], many=True).data
        expected_data = [
            {
                'product_id': product_1.product_id,
                'product_name': 'Песок',
                'product_unit': 'тонна',
                'product_price': '3000.00',
                'product_description': 'Песок как песок'
            },
            {
                'product_id': product_2.product_id,
                'product_name': 'Щебень',
                'product_unit': 'тонна',
                'product_price': '4000.00',
                'product_description': 'Щебень обычный'
            }
        ]
        self.assertEqual(expected_data, data)

