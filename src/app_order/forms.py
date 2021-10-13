from django import forms
from django.core.exceptions import ValidationError

from app_order.models import ProductUnit, Products, Orders, Areas


# !!!Актуальный, испольлзуется с классе views.py - AddProduct
class AddProductForm(forms.ModelForm):
    """ Класс формы нового продукта СВЯЗАННЫЙ с моделью """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_unit'].empty_label = 'Ед. измерения не выбрана'

    class Meta:
        model = Products
        # fields = '__all__'
        fields = ['product_name', 'slug', 'product_unit', 'product_price',
                  'product_description', 'product_photo', 'product_is_published']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'product_description': forms.Textarea(attrs={'cols': 60, 'rows': 7})
        }

    def clean_product_name(self):
        """ Пользовательский валидатор
        начинается с clean_... """
        product_name = self.cleaned_data['product_name']
        if len(product_name) > 10:
            raise ValidationError('Длина превышает 10 символов')
        return product_name


class AddOrderForm(forms.ModelForm):
    """ Класс формы нового заказа СВЯЗАННЫЙ с моделью """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].empty_label = 'Продукт не выбран'
        self.fields['area'].empty_label = 'Район не выбран'

    class Meta:
        model = Orders
        # fields = '__all__'
        fields = ['order_name', 'order_phone', 'product', 'order_count', 'area', 'order_cost',
                  'order_address', 'order_date_delivery', 'order_time_delivery', 'order_timezone',
                  'order_description']
        widgets = {
            'order_name': forms.TextInput(attrs={'id': 'input_name', 'required': True,
                                                 'class': 'form-control',
                                                 'placeholder': 'ваше имя',
                                                 'aria-label': 'Sizing example input',
                                                 'aria-describedby': 'inputGroup-sizing-sm'}),
            'order_phone': forms.TextInput(attrs={'id': 'input_phone', 'required': True,
                                                  'class': 'form-control phone_mask',
                                                  'data-mask': '000-000-0000',
                                                  'aria-label': 'Sizing example input',
                                                  'aria-describedby': 'inputGroup-sizing-sm',
                                                  'pattern': '[\+]\d{1}[\(]\d{3}[\)\ ]\d{3}[\-]\d{4}'}),
            'product': forms.Select(attrs={'id': 'select_product', 'required': True,
                                           'class': 'form-select form-select-sm',
                                           'aria-label': '.form-select-sm example'}),
            'order_count': forms.NumberInput(attrs={'id': 'input_count_unit', 'required': True,
                                                    'min': 1, 'max': 100,
                                                    'class': 'form-control',
                                                    'aria-label': 'Sizing example input',
                                                    'aria-describedby': 'inputGroup-sizing-sm'}),
            'area': forms.Select(attrs={'id': 'select_area', 'required': True,
                                        'class': 'form-select form-select-sm',
                                        'aria-label': '.form-select-sm example'}),
            'order_cost': forms.NumberInput(attrs={'id': 'input_all_cost', 'required': True,
                                                   'min': 1,
                                                   'class': 'form-control',
                                                   'aria-label': 'Disabled input example',
                                                   'aria-describedby': 'inputGroup-sizing-sm',
                                                   'readonly': 'readonly'}),
            'order_address': forms.Textarea(attrs={'id': 'input_address', 'required': True,
                                                   'class': 'form-control',
                                                   'rows': 2}),
            'order_date_delivery': forms.DateInput(attrs={'id': 'input_date_delivery', 'required': True,
                                                          'type': 'date',
                                                          'class': 'form-control'}),
            'order_time_delivery': forms.TimeInput(attrs={'id': 'input_time_delivery', 'required': True,
                                                          'type': 'time',
                                                          'class': 'form-control'}),
            'order_timezone': forms.TextInput(attrs={'id': 'input_timezone', 'required': True,
                                                     'class': 'form-control',
                                                     'aria-label': 'Disabled input example',
                                                     'aria-describedby': 'inputGroup-sizing-sm',
                                                     'readonly': 'readonly'}),
            'order_description': forms.Textarea(attrs={'id': 'input_description',
                                                       'class': 'form-control',
                                                       'rows': 5})
        }

    def clean_order_count(self):
        """ Пользовательский валидатор для order_count
        !начинается с clean_... """
        order_count = self.cleaned_data['order_count']
        if (order_count < 1) or (order_count > 1000):
            raise ValidationError('Количество от 1 до 1000')
        return order_count

    def clean_order_cost(self):
        """ Пользовательский валидатор для order_cost """
        order_cost = self.cleaned_data['order_cost']
        if order_cost < 1:
            raise ValidationError('Некорректный рассчет общей стоимости, повторно заполните форму')
        return order_cost
