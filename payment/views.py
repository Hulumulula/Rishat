import json
import stripe

from django.http import JsonResponse
from django.views import generic, View
from django.conf import settings

from .models import *


stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemsListView(generic.ListView):
    model = Item
    template_name = 'payment/item-list.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Список товаров"
        })
        return context

    def get_queryset(self):
        return Item.objects.all()


class ItemInfoView(generic.DetailView):
    model = Item
    template_name = 'payment/item-info.html'
    context_object_name = 'item'
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        item = Item.objects.get(id=self.kwargs.get('id'))
        context.update({
            "title": "Товар",
            "item": item,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class StripePaymentIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(
                email=req_json.get("email"),
            )
            item = Item.objects.get(id=self.kwargs.get("id"))
            intent = stripe.PaymentIntent.create(
                amount=int(item.price * 100),
                currency=item.currency,
                customer=customer["id"],
                metadata={
                    "item_id": item.id
                }
            )
            return JsonResponse({
                "clientSecret": intent["client_secret"]
            })
        except Exception as e:
            return JsonResponse({"error": str(e)})
