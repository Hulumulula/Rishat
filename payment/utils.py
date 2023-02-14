from .models import *

menu = [
    {'title': "Оплата", 'url_name': 'pay'},
    {'title': "Товар", 'url_name': 'item'},
    {'title': "Список товаров", 'url_name': 'list-item'},
]


class DataMixin:
    paginate_by = 10

    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        context['menu'] = user_menu

        return context
