from django.test import TestCase
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from .views import cart_add, cart_update, cart_delete


class CartViewsTestCase(TestCase):
    def setUp(self):
        # Initialize the RequestFactory
        self.factory = RequestFactory()

    def test_cart_add(self):
        # Test case for adding a product to the cart
        url = reverse('cart_add')  # Get the URL for the cart_add view
        request = self.factory.post(url, {'product_id': 1, 'product_qty': 2})  # Create a POST request
        middleware = SessionMiddleware(lambda request: None)  # Create a session middleware
        middleware.process_request(request)  # Process the request with the session middleware
        request.session.save()  # Save the session
        response = cart_add(request)  # Call the cart_add view
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_cart_update(self):
        # Test case for updating the quantity of a product in the cart
        url = reverse('cart_update')  # Get the URL for the cart_update view
        request = self.factory.post(url, {'product_id': 1, 'product_qty': 3})  # Create a POST request
        middleware = SessionMiddleware(lambda request: None)  # Create a session middleware
        middleware.process_request(request)  # Process the request with the session middleware
        request.session.save()  # Save the session
        response = cart_update(request)  # Call the cart_update view
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)

    def test_cart_delete(self):
        # Test case for deleting a product from the cart
        url = reverse('cart_delete')  # Get the URL for the cart_delete view
        request = self.factory.post(url, {'product_id': 1})  # Create a POST request
        middleware = SessionMiddleware(lambda request: None)  # Create a session middleware
        middleware.process_request(request)  # Process the request with the session middleware
        request.session.save()  # Save the session
        response = cart_delete(request)  # Call the cart_delete view
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)
