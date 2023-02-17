from django.urls import path

from .views import *


urlpatterns = [
    path('buy/<int:id>', StripePaymentIntentView.as_view(), name='create-payment-intent'),
    path('item/<int:id>', ItemInfoView.as_view(), name='item'),
    path('items/', ItemsListView.as_view(), name='items'),
    path('orders/order-create/', order_create, name='order_create'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout')
]
