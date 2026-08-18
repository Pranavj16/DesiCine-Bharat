from django.shortcuts import render
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from bookings.models import Booking, BookedSeat
from movies.models import Movie
from theaters.models import Theater, Showtime

class DashboardAnalyticsAPIView(APIView):
    permission_classes = [permissions.AllowAny] # Or IsAdminUser

    def get(self, request):
        total_revenue = Booking.objects.filter(booking_status='CONFIRMED').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_tickets = BookedSeat.objects.count()
        total_bookings = Booking.objects.count()
        total_movies = Movie.objects.count()
        total_theaters = Theater.objects.count()

        # Revenue by city
        city_stats = (
            Booking.objects.filter(booking_status='CONFIRMED')
            .values('showtime__screen__theater__city')
            .annotate(revenue=Sum('total_amount'), count=Count('id'))
            .order_by('-revenue')
        )

        # Top grossing movies
        movie_stats = (
            Booking.objects.filter(booking_status='CONFIRMED')
            .values('showtime__movie__title', 'showtime__movie__language', 'showtime__movie__poster')
            .annotate(revenue=Sum('total_amount'), tickets=Count('booked_seats'))
            .order_by('-revenue')[:5]
        )

        # Recent Bookings
        recent_bookings = Booking.objects.order_by('-created_at')[:10]
        recent_data = [
            {
                'booking_id': b.booking_id,
                'user': b.user.username,
                'movie': b.showtime.movie.title,
                'theater': f"{b.showtime.screen.theater.name}, {b.showtime.screen.theater.city}",
                'amount': float(b.total_amount),
                'status': b.booking_status,
                'date': b.created_at.strftime('%d %b %Y, %I:%M %p')
            }
            for b in recent_bookings
        ]

        return Response({
            'total_revenue_inr': float(total_revenue),
            'total_tickets_sold': total_tickets,
            'total_bookings': total_bookings,
            'total_movies_active': total_movies,
            'total_theaters': total_theaters,
            'revenue_by_city': list(city_stats),
            'top_grossing_movies': list(movie_stats),
            'recent_bookings': recent_data,
        })


def dashboard(request):
    total_revenue = Booking.objects.filter(booking_status='CONFIRMED').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_tickets = BookedSeat.objects.count()
    total_bookings = Booking.objects.count()
    total_movies = Movie.objects.count()

    recent_bookings = Booking.objects.select_related('user', 'showtime__movie', 'showtime__screen__theater').order_by('-created_at')[:8]
    top_movies = Movie.objects.order_by('-rating')[:5]

    return render(request, 'admin_dashboard.html', {
        'total_revenue': total_revenue,
        'total_tickets': total_tickets,
        'total_bookings': total_bookings,
        'total_movies': total_movies,
        'recent_bookings': recent_bookings,
        'top_movies': top_movies
    })