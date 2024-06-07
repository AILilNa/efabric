from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from store.models import Product


class ShippingAddress(models.Model):
    """
    Model to store shipping address details.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)  # Full name of the recipient
    shipping_email = models.CharField(max_length=255)  # Email of the recipient
    shipping_address = models.CharField(max_length=255)  # Address line
    shipping_city = models.CharField(max_length=255)  # City
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)  # Zipcode (optional)
    shipping_country = models.CharField(max_length=255)  # Country

    class Meta:
        verbose_name_plural = 'Shipping Addresses'  # Plural name for admin panel

    def __str__(self):
        return f'Shipping addresses - {str(self.id)}'  # String representation of the shipping address


def create_shipping(sender, instance, created, **kwargs):
    """
    Signal to create a default shipping address for a user when a new user is created.
    """
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()


# Connect the create_shipping function to the User model's post_save signal
post_save.connect(create_shipping, sender=User)


class Order(models.Model):
    """
    Model to store order details.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # The user who placed the order
    full_name = models.CharField(max_length=255)  # Full name of the person who placed the order
    email = models.EmailField(max_length=255)  # Email of the person who placed the order
    shipping_address = models.TextField(max_length=10000)  # Shipping address for the order
    amount_paid = models.DecimalField(max_digits=15, decimal_places=0)  # Total amount paid for the order
    date_order = models.DateTimeField(auto_now_add=True)  # Date and time when the order was placed

    def __str__(self):
        return f'Order - {str(self.id)}'  # String representation of the order


class OrderItem(models.Model):
    """
    Model to store details of each item in an order.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # The user who placed the order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)  # The order this item belongs to
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)  # The product being ordered
    quantity = models.PositiveBigIntegerField(default=1)  # Quantity of the product ordered
    price = models.DecimalField(max_digits=15, decimal_places=0)  # Price of the product

    def __str__(self):
        return f'Order Item - {str(self.id)}'  # String representation of the order item
