import json
from cart.cart import Cart
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from pandas import Timestamp
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from .forecast import predict_sales, train_sarima_model, data
from .forms import RegistrationForm, UpdateUserForm, UpdatePasswordForm, UserInfoForm
from .models import Product, Category, Profile


def home(request):
    """Renders the homepage with all products."""
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def search(request):
    """Handles product search functionality."""
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "Nothing found")
        return render(request, "search.html", {'searched': searched})
    else:
        return render(request, "search.html", {})


def product(request, pk):
    """Renders the product detail page for a specific product."""
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'products': product})


def category(request, category_name):
    """Renders the category detail page for a specific category."""
    try:
        category_obj = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category_obj)
        return render(request, 'category.html', {'products': products, 'category': category_obj})
    except Category.DoesNotExist:
        messages.error(request, "Invalid category")
        return redirect('home')


def category_all(request):
    """Renders the page displaying all available categories."""
    categories = Category.objects.all()
    return render(request, 'category_all.html', {'categories': categories})


def about(request):
    """Renders the about us page."""
    return render(request, 'about.html', {})


def login_user(request):
    """Handles user login requests."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login successful
            login(request, user)
            current_user = Profile.objects.get(user_id=request.user.id)
            saved_cart = current_user.old_cart

            if saved_cart:
                # Convert the saved cart from JSON to a dictionary
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)

                # Add items from the saved cart to the current cart
                for key, value in converted_cart.items():
                    cart.add_db(product=key, quantity=value)

            messages.success(request, "You successfully logged in")
            return redirect('home')
        else:
            # Login failed
            messages.error(request, "Invalid email or password")
            return redirect('login')

    # Render the login form
    return render(request, 'login.html', {})


def logout_user(request):
    """Logs out the current user."""
    logout(request)
    messages.success(request, "You successfully logged out")
    return redirect('home')


def register_user(request):
    """Handles user registration requests."""
    form = RegistrationForm()

    if request.method == 'POST':
        # Create a new form instance with POST data
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Form data is valid, save the new user
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You successfully registered")
            return redirect('update_information')

        else:
            # Form data is invalid, display error messages
            messages.error(request, "Error registering user")
            return redirect('register')

    # Render the registration form
    return render(request, 'register.html', {'form': form})


def update_user(request):
    """Handles user profile updates."""
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User profile successfully updated")
            return redirect('home')

        return render(request, "update_user.html", {'user_form': user_form})

    else:
        messages.success(request, "Please login")
        return redirect('home')


def update_password(request):
    """Handles password updates for authenticated users."""
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = UpdatePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Password successfully updated")
                login(request, current_user)
                return redirect('update_user')

            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})

    else:
        messages.success(request, "Please login")
        return redirect('home')


def update_information(request):
    """Handles updates to user information and shipping address."""
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = ShippingAddress(user=request.user)

        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if request.method == 'POST':
            if form.is_valid() and shipping_form.is_valid():
                form.save()
                shipping_form.save()
                messages.success(request, "Your information successfully updated")
                return redirect('home')
            else:
                messages.error(request, "Please correct the errors below.")

        return render(request, "update_information.html", {
            'form': form,
            'shipping_form': shipping_form
        })
    else:
        messages.error(request, "Please login")
        return redirect('home')


def forecast(request):
    """Handles sales forecast generation based on user input."""
    categories = Category.objects.all()  # Get all available categories
    predicted_sales_count = None
    plot_uri = None
    error_message = None

    if request.method == 'POST':
        category_input = request.POST.get('category')  # Get the selected category
        selected_date = request.POST.get('date')  # Get the selected date

        # Check if a date is provided
        if not selected_date:
            error_message = "Please select a date."
            return render(request, 'forecast.html', {'categories': categories,
                                                     'error_message': error_message})

        future_date = Timestamp(datetime(2024, 6, 22))

        try:
            if category_input.lower() == 'all':
                unique_categories = data['category'].unique()
                for category in unique_categories:
                    category_data = data[data['category'] == category]
                    model_fit, test_data = train_sarima_model(category_data)
                    if model_fit is not None:
                        predicted_sales, plot_uri, error_message = (
                            predict_sales(model_fit, test_data, category, future_date))  # Predict sales for the future date
                        if not error_message:
                            return render(request, 'forecast.html', {'categories': categories,
                                                                     'predicted_sales_count': predicted_sales,
                                                                     'plot_uri': plot_uri})
                        else:
                            return render(request, 'forecast.html', {'categories': categories,
                                                                     'error_message': error_message})
            else:
                category_data = data[data['category'] == category_input]
                if category_data.empty:
                    error_message = f"Category '{category_input}' not found in data."
                else:
                    model_fit, test_data = train_sarima_model(category_data)
                    if model_fit is not None:
                        predicted_sales, plot_uri, error_message = (
                            predict_sales(model_fit, test_data, category_input, future_date))  # Predict sales for the future date
                        if not error_message:
                            return render(request, 'forecast.html', {'categories': categories,
                                                                     'predicted_sales_count': predicted_sales,
                                                                     'plot_uri': plot_uri})
                        else:
                            return render(request, 'forecast.html', {'categories': categories,
                                                                     'error_message': error_message})

        except Exception as e:
            error_message = f"An error occurred: {e}"  # Handle any exceptions

    return render(request, 'forecast.html', {
        'categories': categories,
        'predicted_sales_count': predicted_sales_count,
        'plot_uri': plot_uri,
        'error_message': error_message
    })
