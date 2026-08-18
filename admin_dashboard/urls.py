from django.urls import path
from .views import dashboard, DashboardAnalyticsAPIView

urlpatterns = [
    # DRF Analytics API
    path('api/analytics/', DashboardAnalyticsAPIView.as_view(), name='api_dashboard_analytics'),

    # Template Page
    path('', dashboard, name='dashboard'),
]