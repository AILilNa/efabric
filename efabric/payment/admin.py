from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

# Register the ShippingAddress model with the Django admin site
admin.site.register(ShippingAddress)

# Register the Order model with the Django admin site
admin.site.register(Order)

# Register the OrderItem model with the Django admin site
admin.site.register(OrderItem)
