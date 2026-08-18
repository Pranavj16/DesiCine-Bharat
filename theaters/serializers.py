from rest_framework import serializers
from .models import Theater, Screen, Seat, Showtime
from movies.serializers import MovieListSerializer

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'row_label', 'seat_number', 'seat_type']


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ['id', 'screen_name', 'screen_type', 'total_rows', 'total_cols']


class TheaterSerializer(serializers.ModelSerializer):
    screens = ScreenSerializer(many=True, read_only=True)

    class Meta:
        model = Theater
        fields = ['id', 'name', 'brand', 'city', 'address', 'facilities', 'image_url', 'screens']


class ShowtimeListSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    theater_name = serializers.CharField(source='screen.theater.name', read_only=True)
    theater_city = serializers.CharField(source='screen.theater.city', read_only=True)
    screen_name = serializers.CharField(source='screen.screen_name', read_only=True)
    screen_type = serializers.CharField(source='screen.screen_type', read_only=True)

    class Meta:
        model = Showtime
        fields = [
            'id', 'movie', 'movie_title', 'theater_name', 'theater_city',
            'screen_name', 'screen_type', 'show_date', 'show_time',
            'language', 'format', 'silver_price', 'gold_price', 'recliner_price', 'is_active'
        ]


class ShowtimeDetailSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)
    theater = TheaterSerializer(source='screen.theater', read_only=True)
    screen = ScreenSerializer(read_only=True)
    seat_layout = serializers.SerializerMethodField()

    class Meta:
        model = Showtime
        fields = [
            'id', 'movie', 'theater', 'screen', 'show_date', 'show_time',
            'language', 'format', 'silver_price', 'gold_price', 'recliner_price',
            'seat_layout'
        ]

    def get_seat_layout(self, obj):
        seats = Seat.objects.filter(screen=obj.screen)
        booked_seat_ids = set(obj.booked_seats_all.values_list('seat_id', flat=True))

        layout = []
        for seat in seats:
            price = float(obj.gold_price)
            if seat.seat_type == 'SILVER':
                price = float(obj.silver_price)
            elif seat.seat_type == 'RECLINER':
                price = float(obj.recliner_price)

            layout.append({
                'id': seat.id,
                'row': seat.row_label,
                'number': seat.seat_number,
                'type': seat.seat_type,
                'price': price,
                'is_booked': seat.id in booked_seat_ids,
            })
        return layout
