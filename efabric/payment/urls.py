from django.urls import path
from . import views

urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),  # Displays payment success
    path('order', views.order, name='order'),  # Displays order
    path('billing', views.billing, name='billing'),  # Displays billing
    path('process_order', views.process_order, name='process_order'),  # Displays process order

]
