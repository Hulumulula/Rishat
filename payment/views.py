import json
import stripe
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic, View
from django.conf import settings

from cart.cart import Cart
from cart.forms import CartAddItemForm
from .forms import *
from .models import *


stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemsListView(generic.ListView):
    model = Item
    template_name = 'payment/item-list.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddItemForm()
        context.update({
            "title": "Список товаров",
            'cart_product_form': cart_product_form,
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
        item = get_object_or_404(Item, id=self.kwargs.get('id'))
        cart_product_form = CartAddItemForm()
        context.update({
            "title": "Товар",
            "item": item,
            'cart_product_form': cart_product_form,
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


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         item=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'payment/order-created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'payment/order-create.html',
                  {'cart': cart, 'form': form})


class RegisterUser(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'payment/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'title': 'Регистрация',
            }
        )
        return context

    def form_valid(self, form):
        user = form.save()
        old_session = self.request.session
        login(self.request, user)
        self.request.session = old_session
        return redirect('payment:items')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'payment/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'title': 'Авторизация',
            }
        )
        return context

    def get_success_url(self):
        return reverse_lazy('payment:items')


def logout_user(request):
    logout(request)
    return redirect('payment:items')


def page_not_found(request, exception):
    return render(request, 'payment/404.html')
