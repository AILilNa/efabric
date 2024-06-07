from store.models import Product, Profile


class Cart:
    def __init__(self, request):
        # Initialize the cart with the session and request objects
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        # If no cart is found in the session, create an empty cart
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add_db(self, product, quantity):
        # Add product to the cart using the product ID as the key
        product_id = str(product)
        product_qty = str(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)

        # Mark the session as modified to ensure the cart is saved
        self.session.modified = True

        # If the user is authenticated, update the user's old cart in their profile
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        # Add product to the cart using the product ID as the key
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)

        # Mark the session as modified to ensure the cart is saved
        self.session.modified = True

        # If the user is authenticated, update the user's old cart in their profile
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user_id=self.request.user.id)
            cartt = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=str(cartt))

    def get_total_price(self):
        # Calculate the total price of items in the cart
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.price_sale * value
                    else:
                        total += product.price * value

        return total

    def __len__(self):
        # Return the number of items in the cart
        return len(self.cart)

    def get_products(self):
        # Retrieve the products in the cart based on their IDs
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantities(self):
        # Return the quantities of items in the cart
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        # Update the quantity of a specific product in the cart
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart
        ourcart[product_id] = product_qty

        # Mark the session as modified to ensure the cart is saved
        self.session.modified = True

        # If the user is authenticated, update the user's old cart in their profile
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=str(carty))

        cloth = self.cart
        return cloth

    def delete(self, product):
        # Remove a product from the cart
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        # Mark the session as modified to ensure the cart is saved
        self.session.modified = True

        # If the user is authenticated, update the user's old cart in their profile
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user_id=self.request.user.id)
            cartt = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=str(cartt))
