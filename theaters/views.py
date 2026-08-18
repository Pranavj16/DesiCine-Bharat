from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Theater, Screen, Seat, Showtime
from .serializers import TheaterSerializer, ShowtimeListSerializer, ShowtimeDetailSerializer

# ==================== DRF VIEWSETS ====================

class TheaterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        city = self.request.query_params.get('city')
        brand = self.request.query_params.get('brand')
        if city:
            qs = qs.filter(city__iexact=city)
        if brand:
            qs = qs.filter(brand__icontains=brand)
        return qs


class ShowtimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Showtime.objects.filter(is_active=True)
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ShowtimeDetailSerializer
        return ShowtimeListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        movie_id = self.request.query_params.get('movie')
        city = self.request.query_params.get('city')
        date = self.request.query_params.get('date')

        if movie_id:
            qs = qs.filter(movie_id=movie_id)
        if city:
            qs = qs.filter(screen__theater__city__iexact=city)
        if date:
            qs = qs.filter(show_date=date)
        return qs

    @action(detail=True, methods=['get'])
    def seat_layout(self, request, pk=None):
        showtime = self.get_object()
        serializer = ShowtimeDetailSerializer(showtime)
        return Response(serializer.data)
