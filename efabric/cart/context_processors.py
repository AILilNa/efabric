from .cart import Cart


def cart(request):
    """
    Creates a Cart object and adds it to the context dictionary.
    """
    cart_obj = Cart(request)  # Initialize a Cart object using the request object
    cart_context = {'cart': cart_obj}  # Create a context dictionary with the cart object
    return cart_context  # Return the context dictionary
