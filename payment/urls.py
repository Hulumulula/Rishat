from django.urls import path

urlpatterns = [
    path('buy/<int:id>', StripePaymentIntentView.as_view(), name='buy'),
    path('item/<int:id>', ItemInfoView.as_view(), name='item'),
    path('items/', ItemsListView.as_view(), name='items'),

]
