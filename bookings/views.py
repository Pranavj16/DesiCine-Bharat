from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SnackItem, Booking, BookedSeat
from .serializers import SnackItemSerializer, BookingDetailSerializer, BookingCreateSerializer
from theaters.models import Showtime
from movies.models import Movie
from movies.recommendation_engine import BollywoodRecommendationEngine

# ==================== DRF VIEWSETS ====================

class SnackItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SnackItem.objects.filter(is_available=True)
    serializer_class = SnackItemSerializer
    permission_classes = [permissions.AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Booking.objects.all()
            return Booking.objects.filter(user=user)
        return Booking.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = BookingCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        response_serializer = BookingDetailSerializer(booking)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def my_tickets(self, request):
        user = request.user
        if user.is_authenticated:
            bookings = Booking.objects.filter(user=user).order_by('-created_at')
        else:
            bookings = Booking.objects.all().order_by('-created_at')[:5]
        serializer = BookingDetailSerializer(bookings, many=True)
        return Response(serializer.data)


# ==================== TEMPLATE VIEWS ====================

def seat_selection(request, showtime_id=None):
    if showtime_id:
        showtime = get_object_or_404(Showtime, id=showtime_id)
    else:
        showtime = Showtime.objects.first()

    # Smart Recommendation Engine in Booking: Suggest similar blockbusters
    recommended_movies = []
    if showtime and showtime.movie:
        recommended_movies = BollywoodRecommendationEngine.get_booking_recommendations(showtime.movie.id, top_n=3)

    return render(request, "seat_selection.html", {
        'showtime': showtime,
        'recommended_movies': recommended_movies
    })


def checkout(request):
    showtime_id = request.GET.get('showtime_id')
    showtime = Showtime.objects.filter(id=showtime_id).first() if showtime_id else Showtime.objects.first()
    snacks = SnackItem.objects.filter(is_available=True)
    return render(request, "checkout.html", {
        'showtime': showtime,
        'snacks': snacks
    })


def payment_success(request):
    booking_id = request.GET.get('booking_id')
    if booking_id:
        booking = Booking.objects.filter(booking_id=booking_id).first()
    else:
        booking = Booking.objects.order_by('-created_at').first()

    # Ticket Booking Recommendation Engine:
    # Suggest next blockbusters based on the movie user just booked!
    recommended_movies = []
    if booking and booking.showtime and booking.showtime.movie:
        recommended_movies = BollywoodRecommendationEngine.get_booking_recommendations(booking.showtime.movie.id, top_n=4)
    else:
        recommended_movies = BollywoodRecommendationEngine.get_trending_bollywood_blockbusters(top_n=4)

    return render(request, "payment_success.html", {
        'booking': booking,
        'recommended_movies': recommended_movies
    })
