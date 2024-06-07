from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .cart import Cart
from store.models import Product


def cart_all(request):
    """
    Displays the entire cart contents to the user.
    """
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    total_price = cart.get_total_price()
    context = {"cart_products": cart_products, "quantities": quantities, "total_price": total_price}
    return render(request, 'cart_all.html', context)


def cart_add(request):
    """
    Handles adding a product to the cart and returns a JSON response.
    """
    cart = Cart(request)
    if request.method == 'POST':  # Check for POST request
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_quantity = len(cart)
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Product successfully added to cart")
        return response


def cart_update(request):
    """
    Handles updating the quantity of a product in the cart and returns a JSON response.
    """
    cart = Cart(request)
    if request.method == 'POST':  # Check for POST request
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty': product_qty})
        messages.success(request, "Product quantity successfully updated")
        return response


def cart_delete(request):
    """
    Handles deleting a product from the cart and returns a JSON response.
    """
    cart = Cart(request)
    if request.method == 'POST':  # Check for POST request
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request, "Product successfully removed from cart")
        return response
