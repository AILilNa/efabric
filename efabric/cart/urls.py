from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_all, name='cart_all'),  # Displays the entire cart
    path('add/', views.cart_add, name='cart_add'),  # Adds a product to the cart
    path('update/', views.cart_update, name='cart_update'),  # Updates the quantity of a product in the cart
    path('delete/', views.cart_delete, name='cart_delete'),  # Removes a product from the cart
]
