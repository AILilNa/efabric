from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL for site management
    path('', include('store.urls')),  # Include URLs from the 'store' app
    path('cart/', include('cart.urls')),  # Include URLs from the 'cart' app
    path('payment/', include('payment.urls')),  # Include URLs from the 'payment' app

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve static media files
