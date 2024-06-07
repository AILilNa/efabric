from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    old_cart = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Category(models.Model):
    """Represents product categories."""
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='uploads/category/', default=0)  # Consider using a default image path

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Customer(models.Model):
    """Represents customer information."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    """Represents product information."""
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    is_sale = models.BooleanField(default=False)
    price_sale = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    """Represents customer orders."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)
