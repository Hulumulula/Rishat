from django.urls import path

from . import views


urlpatterns = [
    path('add/<int:item_id>', views.cart_add, name='cart_add'),
    path('remove/<int:item_id>', views.cart_remove, name='cart_remove'),
]
