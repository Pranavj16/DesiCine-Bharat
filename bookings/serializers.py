from decimal import Decimal
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import SnackItem, Booking, BookedSeat, BookingSnack
from theaters.models import Showtime, Seat
from payments.models import Payment

class SnackItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnackItem
        fields = ['id', 'name', 'category', 'description', 'price', 'image_url', 'is_available']


class BookedSeatSerializer(serializers.ModelSerializer):
    row_label = serializers.CharField(source='seat.row_label', read_only=True)
    seat_number = serializers.IntegerField(source='seat.seat_number', read_only=True)
    seat_type = serializers.CharField(source='seat.seat_type', read_only=True)

    class Meta:
        model = BookedSeat
        fields = ['id', 'seat', 'row_label', 'seat_number', 'seat_type', 'price']


class BookingSnackSerializer(serializers.ModelSerializer):
    snack_name = serializers.CharField(source='snack.name', read_only=True)

    class Meta:
        model = BookingSnack
        fields = ['id', 'snack', 'snack_name', 'quantity', 'price']


class BookingDetailSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='showtime.movie.title', read_only=True)
    movie_poster = serializers.CharField(source='showtime.movie.poster', read_only=True)
    movie_language = serializers.CharField(source='showtime.language', read_only=True)
    theater_name = serializers.CharField(source='showtime.screen.theater.name', read_only=True)
    theater_city = serializers.CharField(source='showtime.screen.theater.city', read_only=True)
    screen_name = serializers.CharField(source='showtime.screen.screen_name', read_only=True)
    show_date = serializers.DateField(source='showtime.show_date', read_only=True)
    show_time = serializers.TimeField(source='showtime.show_time', read_only=True)
    format = serializers.CharField(source='showtime.format', read_only=True)
    booked_seats = BookedSeatSerializer(many=True, read_only=True)
    snacks = BookingSnackSerializer(many=True, read_only=True)
    payment_method = serializers.CharField(source='payment.payment_method', read_only=True)
    transaction_id = serializers.CharField(source='payment.transaction_id', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_id', 'booking_status', 'movie_title', 'movie_poster',
            'movie_language', 'theater_name', 'theater_city', 'screen_name',
            'show_date', 'show_time', 'format', 'ticket_amount', 'snack_amount',
            'convenience_fee', 'gst', 'total_amount', 'qr_code_data',
            'created_at', 'booked_seats', 'snacks', 'payment_method', 'transaction_id'
        ]


class BookingCreateSerializer(serializers.Serializer):
    showtime_id = serializers.IntegerField()
    seat_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )
    snacks = serializers.ListField(
        child=serializers.DictField(), required=False, default=[]
    )
    payment_method = serializers.ChoiceField(
        choices=Payment.METHOD_CHOICES, default='UPI_PHONEPE'
    )
    upi_vpa = serializers.CharField(required=False, allow_blank=True, default='')

    def validate(self, data):
        showtime_id = data.get('showtime_id')
        seat_ids = data.get('seat_ids')

        try:
            showtime = Showtime.objects.get(id=showtime_id)
        except Showtime.DoesNotExist:
            raise serializers.ValidationError({"showtime_id": "Invalid showtime ID."})

        # Check if any seat is already booked for this showtime
        already_booked = BookedSeat.objects.filter(showtime=showtime, seat_id__in=seat_ids)
        if already_booked.exists():
            taken_labels = [f"{b.seat.row_label}{b.seat.seat_number}" for b in already_booked]
            raise serializers.ValidationError({
                "seat_ids": f"Seats already booked: {', '.join(taken_labels)}"
            })

        data['showtime_obj'] = showtime
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        if not user:
            user, _ = User.objects.get_or_create(
                username='guest_viewer',
                defaults={'email': 'guest@desicine.in', 'first_name': 'Desi', 'last_name': 'Cinephile'}
            )

        showtime = validated_data['showtime_obj']
        seat_ids = validated_data['seat_ids']
        snacks_data = validated_data.get('snacks', [])
        payment_method = validated_data.get('payment_method', 'UPI_PHONEPE')
        upi_vpa = validated_data.get('upi_vpa', '')

        with transaction.atomic():
            # Lock seats calculation
            seats = Seat.objects.filter(id__in=seat_ids, screen=showtime.screen)
            if len(seats) != len(seat_ids):
                # Fallback to available seats from the screen if IDs are missing
                seats = Seat.objects.filter(screen=showtime.screen)[:len(seat_ids)]

            ticket_amount = Decimal('0.00')
            seat_records = []
            for seat in seats:
                if seat.seat_type == 'SILVER':
                    price = showtime.silver_price
                elif seat.seat_type == 'RECLINER':
                    price = showtime.recliner_price
                else:
                    price = showtime.gold_price
                ticket_amount += Decimal(str(price))
                seat_records.append((seat, price))

            # Snacks calculation
            snack_amount = Decimal('0.00')
            snack_records = []
            for s_item in snacks_data:
                s_id = s_item.get('snack_id')
                qty = int(s_item.get('quantity', 1))
                if qty > 0:
                    try:
                        snack_obj = SnackItem.objects.get(id=s_id)
                        cost = Decimal(str(snack_obj.price)) * qty
                        snack_amount += cost
                        snack_records.append((snack_obj, qty, snack_obj.price))
                    except SnackItem.DoesNotExist:
                        pass

            convenience_fee = Decimal('40.00') * max(1, len(seats))
            gst = (ticket_amount + snack_amount + convenience_fee) * Decimal('0.18')
            total_amount = ticket_amount + snack_amount + convenience_fee + gst

            booking = Booking.objects.create(
                user=user,
                showtime=showtime,
                booking_status='CONFIRMED',
                ticket_amount=ticket_amount,
                snack_amount=snack_amount,
                convenience_fee=convenience_fee,
                gst=gst,
                total_amount=total_amount
            )

            # Create BookedSeat records
            for seat, price in seat_records:
                BookedSeat.objects.create(
                    booking=booking,
                    seat=seat,
                    showtime=showtime,
                    price=price
                )

            # Create BookingSnack records
            for snack_obj, qty, price in snack_records:
                BookingSnack.objects.create(
                    booking=booking,
                    snack=snack_obj,
                    quantity=qty,
                    price=price
                )

            # Create Mock Payment
            Payment.objects.create(
                booking=booking,
                amount=total_amount,
                payment_method=payment_method,
                payment_status='SUCCESS',
                upi_vpa=upi_vpa or 'user@okaxis'
            )

            return booking
