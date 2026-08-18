from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    booking_id = serializers.CharField(source='booking.booking_id', read_only=True)
    movie_title = serializers.CharField(source='booking.showtime.movie.title', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'transaction_id', 'booking_id', 'movie_title',
            'payment_method', 'payment_status', 'amount', 'upi_vpa', 'created_at'
        ]
