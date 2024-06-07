from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .views import order, billing, process_order


class PaymentViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    # Test for accessing the order view
    def test_order_view(self):
        # Generate the URL for the order view
        url = reverse('order')
        # Create a GET request to the URL
        request = self.factory.get(url)
        # Call the order view with the GET request
        response = order(request)
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Assert that the order.html template is used
        self.assertTemplateUsed(response, 'payment/order.html')

    # Test for accessing the order view with an authenticated user
    def test_order_view_post_authenticated(self):
        # Generate the URL for the order view
        url = reverse('order')
        # Create a user
        user = User.objects.create_user(username='testuser', password='12345')
        # Create a POST request to the URL
        request = self.factory.post(url)
        # Set the user for the request
        request.user = user
        # Call the order view with the POST request
        response = order(request)
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Assert that the order.html template is used
        self.assertTemplateUsed(response, 'payment/order.html')

    # Test for accessing the billing view
    def test_billing_view(self):
        # Generate the URL for the billing view
        url = reverse('billing')
        # Create a GET request to the URL
        request = self.factory.get(url)
        # Call the billing view with the GET request
        response = billing(request)
        # Assert that the response status code is 302 (redirects if shipping info is missing)
        self.assertEqual(response.status_code, 302)

    # Test for accessing the billing view with a POST request
    def test_billing_view_post(self):
        # Generate the URL for the billing view
        url = reverse('billing')
        # Create a POST request to the URL
        request = self.factory.post(url)
        # Set the shipping session data for the request
        request.session['shipping'] = {'shipping_full_name': 'John Doe', 'shipping_email': 'john@example.com',
                                       'shipping_address': '123 Main St', 'shipping_city': 'New York',
                                       'shipping_zipcode': '10001', 'shipping_country': 'USA'}
        # Call the billing view with the POST request
        response = billing(request)
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Assert that the billing.html template is used
        self.assertTemplateUsed(response, 'payment/billing.html')

    # Test for processing the order with an authenticated user
    def test_process_order_view_authenticated(self):
        # Generate the URL for the process_order view
        url = reverse('process_order')
        # Create a user
        user = User.objects.create_user(username='testuser', password='12345')
        # Create a POST request to the URL
        request = self.factory.post(url)
        # Set the user for the request
        request.user = user
        # Set the shipping session data for the request
        request.session['shipping'] = {'shipping_full_name': 'John Doe', 'shipping_email': 'john@example.com',
                                       'shipping_address': '123 Main St', 'shipping_city': 'New York',
                                       'shipping_zipcode': '10001', 'shipping_country': 'USA'}
        # Call the process_order view with the POST request
        response = process_order(request)
        # Assert that the response status code is 302 (redirects to payment success)
        self.assertEqual(response.status_code, 302)

    # Test for processing the order without an authenticated user
    def test_process_order_view_unauthenticated(self):
        # Generate the URL for the process_order view
        url = reverse('process_order')
        # Create a POST request to the URL
        request = self.factory.post(url)
        # Set the shipping session data for the request
        request.session['shipping'] = {'shipping_full_name': 'John Doe', 'shipping_email': 'john@example.com',
                                       'shipping_address': '123 Main St', 'shipping_city': 'New York',
                                       'shipping_zipcode': '10001', 'shipping_country': 'USA'}
        # Call the process_order view with the POST request
        response = process_order(request)
        # Assert that the response
