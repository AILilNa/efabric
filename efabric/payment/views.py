from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ShippingForm, BillingForm
from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart


def payment_success(request):
    """
    Renders the payment success page.
    """
    return render(request, 'payment/payment_success.html', {})


def order(request):
    """
    Handles the order placement process, including displaying the cart,
    capturing shipping details, and redirecting to billing.
    """
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    total_price = cart.get_total_price()

    if request.user.is_authenticated:
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        shipping_form = ShippingForm(request.POST or None)

    if request.method == 'POST':
        if shipping_form.is_valid():
            # Save shipping form data to session
            request.session['shipping'] = shipping_form.cleaned_data
            return redirect('billing')
        else:
            messages.error(request, "Please correct the errors in the form.")

    return render(request, 'payment/order.html', {
        "cart_products": cart_products,
        "quantities": quantities,
        "total_price": total_price,
        "shipping_form": shipping_form
    })


def billing(request):
    """
    Handles the billing process, including displaying the cart,
    capturing billing details, and redirecting to process the order.
    """
    if 'shipping' not in request.session:
        messages.error(request, "Shipping information is missing.")
        return redirect('order')

    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    total_price = cart.get_total_price()

    billing_form = BillingForm(request.POST or None)

    if request.method == 'POST' and billing_form.is_valid():
        billing_data = billing_form.cleaned_data
        request.session['billing'] = billing_data
        return redirect('process_order')

    return render(request, 'payment/billing.html', {
        "cart_products": cart_products,
        "quantities": quantities,
        "total_price": total_price,
        "shipping": request.session.get('shipping'),
        "billing_form": billing_form,
    })


def process_order(request):
    """
    Processes the order, including creating order and order items,
    saving them to the database, and clearing the cart.
    """
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quantities()
        total_price = cart.get_total_price()
        billing_form = BillingForm(request.POST or None)
        shipping = request.session.get('shipping')
        full_name = shipping['shipping_full_name']
        email = shipping['shipping_email']
        shipping_address = (f"{shipping['shipping_address']}\n{shipping['shipping_city']}\n"
                            f"{shipping['shipping_zipcode']}\n{shipping['shipping_country']}\n")
        amount_paid = total_price

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email,
                                 shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            order_id = create_order.pk
            for product in cart_products:
                product_id = product.id

                if product.is_sale:
                    product_price = product.price_sale
                else:
                    product_price = product.price

                for key, value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id,
                                                      product_id=product_id,
                                                      user=user,
                                                      quantity=value,
                                                      price=product_price)
                        create_order_item.save()
                        return redirect('payment_success')

            messages.success(request, "Order successfully created")
            return redirect('home')

        else:
            create_order = Order(full_name=full_name, email=email,
                                 shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            order_id = create_order.pk
            for product in cart_products:
                product_id = product.id

                if product.is_sale:
                    product_price = product.price_sale
                else:
                    product_price = product.price

                for key, value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id,
                                                      product_id=product_id,
                                                      quantity=value,
                                                      price=product_price)
                        create_order_item.save()
                        return redirect('payment_success')

    else:
        messages.success(request, "Please login")
        return redirect('home')
