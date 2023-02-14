from django.views import generic

from .models import *
from .utils import *


class ItemsListView(DataMixin, generic.ListView):
    model = Item
    template_name = 'payment/item-list.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список товаров")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Item.objects.all()


class StripePaymentIntentView(DataMixin, generic.View):
    model = Item


class ItemInfoView(DataMixin, generic.DetailView):
    model = Item
    template_name = 'payment/item-info.html'
    context_object_name = 'item'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Товар")
        return dict(list(context.items()) + list(c_def.items()))