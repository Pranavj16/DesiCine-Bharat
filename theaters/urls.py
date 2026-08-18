from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TheaterViewSet, ShowtimeViewSet

router = DefaultRouter()
router.register(r'theaters', TheaterViewSet, basename='theater-api')
router.register(r'showtimes', ShowtimeViewSet, basename='showtime-api')

urlpatterns = [
    path('api/', include(router.urls)),
]
