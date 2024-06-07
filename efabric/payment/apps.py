from django.apps import AppConfig


class PaymentConfig(AppConfig):
    # Set the default field type for auto-generated primary keys
    default_auto_field = 'django.db.models.BigAutoField'
    # Specify the name of the application
    name = 'payment'
