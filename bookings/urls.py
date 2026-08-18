from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SnackItemViewSet, BookingViewSet, seat_selection, checkout, payment_success

router = DefaultRouter()
router.register(r'snacks', SnackItemViewSet, basename='snack-api')
router.register(r'bookings', BookingViewSet, basename='booking-api')

urlpatterns = [
    # DRF API
    path('api/', include(router.urls)),

    # Template Pages
    path('seat-selection/', seat_selection, name='seat_selection'),
    path('seat-selection/<int:showtime_id>/', seat_selection, name='seat_selection_by_showtime'),
    path('checkout/', checkout, name='checkout'),
    path('payment-success/', payment_success, name='payment_success'),
]