from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    ProfileAPIView,
    login_view,
    signup_view,
    logout_view,
    user_account
)

urlpatterns = [
    # DRF Auth APIs
    path('api/auth/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/auth/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/auth/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('api/auth/profile/', ProfileAPIView.as_view(), name='api_profile'),

    # Template Pages
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('account/', user_account, name='user_account'),
]