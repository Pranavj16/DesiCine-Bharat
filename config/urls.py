from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
    path('', include('theaters.urls')),
    path('', include('bookings.urls')),
    path('', include('payments.urls')),
    path('', include('accounts.urls')),
    path('dashboard/', include('admin_dashboard.urls')),
]