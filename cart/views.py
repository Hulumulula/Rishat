from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from payment.models import *
from .cart import Cart
from .forms import CartAddItemForm


@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    form = CartAddItemForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=item,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])

    return redirect('payment:items')


def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('payment:items')
