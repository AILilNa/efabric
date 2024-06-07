from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .views import (home, search, category_all, about, login_user, logout_user,
                    register_user, update_user, update_password, update_information, forecast)
from .models import Product, Category


class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    # Test for the home view
    def test_home_view(self):
        url = reverse('home')
        request = self.factory.get(url)
        response = home(request)
        self.assertEqual(response.status_code, 200)

    # Test for the search view
    def test_search_view(self):
        url = reverse('search')
        request = self.factory.post(url, {'searched': 'test'})
        response = search(request)
        self.assertEqual(response.status_code, 200)

    # Test for the product view
    def test_product_view(self):
        product = Product.objects.create(name='Test Product', description='Test Description', price=10)
        url = reverse('product', args=[product.id])
        request = self.factory.get(url)
        response = product(request, product.id)
        self.assertEqual(response.status_code, 200)

    # Test for the category view
    def test_category_view(self):
        category = Category.objects.create(name='Test Category')
        url = reverse('category', args=[category.name])
        request = self.factory.get(url)
        response = category(request, category.name)
        self.assertEqual(response.status_code, 200)

    # Test for the category_all view
    def test_category_all_view(self):
        url = reverse('category_all')
        request = self.factory.get(url)
        response = category_all(request)
        self.assertEqual(response.status_code, 200)

    # Test for the about view
    def test_about_view(self):
        url = reverse('about')
        request = self.factory.get(url)
        response = about(request)
        self.assertEqual(response.status_code, 200)

    # Test for the login_user view
    def test_login_user_view(self):
        url = reverse('login')
        request = self.factory.get(url)
        response = login_user(request)
        self.assertEqual(response.status_code, 200)

    # Test for the logout_user view
    def test_logout_user_view(self):
        url = reverse('logout')
        request = self.factory.get(url)
        response = logout_user(request)
        self.assertEqual(response.status_code, 302)

    # Test for the register_user view
    def test_register_user_view(self):
        url = reverse('register')
        request = self.factory.get(url)
        response = register_user(request)
        self.assertEqual(response.status_code, 200)

    # Test for the update_user view
    def test_update_user_view(self):
        user = User.objects.create_user(username='testuser', password='12345')
        url = reverse('update_user')
        request = self.factory.get(url)
        request.user = user
        response = update_user(request)
        self.assertEqual(response.status_code, 200)

    # Test for the update_password view
    def test_update_password_view(self):
        user = User.objects.create_user(username='testuser', password='12345')
        url = reverse('update_password')
        request = self.factory.get(url)
        request.user = user
        response = update_password(request)
        self.assertEqual(response.status_code, 200)

    # Test for the update_information view
    def test_update_information_view(self):
        user = User.objects.create_user(username='testuser', password='12345')
        url = reverse('update_information')
        request = self.factory.get(url)
        request.user = user
        response = update_information(request)
        self.assertEqual(response.status_code, 200)

    # Test for the forecast view
    def test_forecast_view(self):
        url = reverse('forecast')
        request = self.factory.get(url)
        response = forecast(request)
        self.assertEqual(response.status_code, 200)
