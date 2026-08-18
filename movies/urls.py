from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, home, movie_details

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie-api')

urlpatterns = [
    # DRF API
    path('api/', include(router.urls)),

    # Template Pages
    path('', home, name='home'),
    path('movie-details/', movie_details, name='movie_details'),
    path('movie/<int:movie_id>/', movie_details, name='movie_detail_by_id'),
]