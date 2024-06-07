from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category, Customer, Product, Order, Profile

# Registering models with the admin site
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


# Inline editing of Profile model within User admin
class ProfileInline(admin.StackedInline):
    model = Profile


# Customizing User admin to include Profile inline
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]


# Unregistering default User admin and registering custom User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
