from app_order.models import OrderStatus

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Продукты', 'url_name': 'products'},
    {'title': 'Мои заказы', 'url_name': 'orders'},
    {'title': 'Новый заказ', 'url_name': 'new_order'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
 ]


class OrderContext:
    def get_order_context(self, **kwargs):
        # Получаем переданный контекст
        context = kwargs

        # Добавляем общий контекст
        # statuses = OrderStatus.objects.all()  # пользовательский тег
        # context['statuses'] = statuses
        # context['menu'] = menu  # пользовательский тег

        if 'status_selected' not in context:
            context['status_selected'] = 0

        return context  # Возвращаем весь контекст
