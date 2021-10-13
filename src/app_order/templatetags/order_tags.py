"""
Пользовательские теги
Для исключения дублирования кода
"""

from django import template
from django.db.models import Count

from app_order.models import OrderStatus

register = template.Library()


# простой тег
# передает параметр для использования в шаблоне
# базовый вариант без параметров
# @register.simple_tag(name='get_statuses')
# def get_statuses():
#    """ Список всех статусов заказа """
#    return OrderStatus.objects.order_by('status_id')

# простой тег
# с передачей параметра
@register.simple_tag(name='get_statuses')
def get_statuses(filter=None):
    if not filter:
        return OrderStatus.objects.order_by('status_id')
    else:
        return OrderStatus.objects.filter(status_id=filter)

# включающий тег
# передает шаблон-фрагмент страницы для использования в основном шаблоне
# базовый вариант без параметров
# @register.inclusion_tag('order/order/list_statuses.html')
# def show_statuses():
#    statuses = OrderStatus.objects.order_by('status_id')
#    return {'statuses': statuses}


# включающий тег
# с передачей параметра
@register.inclusion_tag('order/order_tags/list_statuses.html')
def show_statuses(user, sort=None, status_selected=0):
    if not sort:
        # statuses = OrderStatus.objects.all()
        # statuses = OrderStatus.objects.annotate(count=Count('orders'))
        statuses = OrderStatus.objects.filter(orders__user=user).annotate(count=Count('orders'))
    else:
        # statuses = OrderStatus.objects.order_by(sort)
        # statuses = OrderStatus.objects.annotate(count=Count('orders')).order_by(sort)
        statuses = OrderStatus.objects.filter(orders__user=user).annotate(count=Count('orders')).order_by(sort)

    return {'statuses': statuses, 'status_selected': status_selected}

# ===
# - Вам нужно передать пользователя в свой тег включения.
# @register.inclusion_tag('Kappa/sidebar.html')
# def get_game_list(user):
#     return {'game_list': Game.objects.all(),  'user': user}
#
# Затем в вашем шаблоне вызовите тег с
# {% get_game_list user %}
#
# - Кроме того, вы можете установить takes_context=True в теге включения,
# чтобы получить доступ к пользователю из контекста шаблона.
# @register.inclusion_tag('Kappa/sidebar.html', takes_context=True)
# def get_game_list(context):
#     return {'game_list': Game.objects.all(),  'user': context['user']}
#
# В этом случае вам больше не нужно передавать пользователя в тег шаблона.
# {% get_game_list %}
# ===


@register.inclusion_tag('order/order_tags/list_menu.html')
def show_menu(user, item_selected=0):
    menu = [
        {'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Продукты', 'url_name': 'products'},
        {'title': 'Добавить продукт', 'url_name': 'new_product'},  # еще редирект в new_product_x.html
        {'title': 'Мои заказы', 'url_name': 'orders'},
        {'title': 'Новый заказ', 'url_name': 'new_order_form'},  # еще редирект в new_order_form.html
        {'title': 'Обратная связь', 'url_name': 'contact'},
    ]

    # # Проверка авторизации и корректировка списка меню
    # user_menu = menu.copy()
    # if not user.is_authenticated:
    #     user_menu.pop(1)  # Удаляем "Продукты"

    return {'user': user, 'menu': menu, 'item_selected': item_selected}




