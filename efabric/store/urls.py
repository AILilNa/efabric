from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('about/', views.about, name='about'),  # About page
    path('login/', views.login_user, name='login'),  # Login page
    path('logout/', views.logout_user, name='logout'),  # Logout path
    path('register/', views.register_user, name='register'),  # Registration path
    path('product/<int:pk>/', views.product, name='product'),  # Product detail page with dynamic ID
    path('category_all/', views.category_all, name='category_all'),  # All categories page
    path('category/<slug:category_name>/', views.category, name='category'),  # Category detail page with slug
    path('search/', views.search, name='search'),  # Search functionality
    path('update_user', views.update_user, name='update_user'),  # Update user profile
    path('update_password', views.update_password, name='update_password'),  # Update user password
    path('update_information', views.update_information, name='update_information'),  # Update user information
    path('forcast/', views.forecast, name='forcast'),  # Forecast page (consider naming convention)
]
