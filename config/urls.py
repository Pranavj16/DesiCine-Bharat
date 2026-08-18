import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.views.static import serve
from django.conf import settings

# Determine primary static document root
if hasattr(settings, 'STATIC_ROOT') and os.path.exists(settings.STATIC_ROOT):
    document_root = settings.STATIC_ROOT
else:
    document_root = settings.STATICFILES_DIRS[0]

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
    path('', include('theaters.urls')),
    path('', include('bookings.urls')),
    path('', include('payments.urls')),
    path('', include('accounts.urls')),
    path('dashboard/', include('admin_dashboard.urls')),
    # Direct static file serving fallback for serverless cloud environments (Vercel)
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': document_root}),
]