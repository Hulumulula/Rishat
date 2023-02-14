from django.views import generic

from .models import *


class ItemsListView(generic.ListView):
    model = Item
    template_name = 'payment/item-list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.all()


class StripePaymentIntentView(generic.View):
    pass


class ItemInfoView(generic.DetailView):
    model = Item
    template_name = 'payment/item-info.html'
    context_object_name = 'item'

