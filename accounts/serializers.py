from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from bookings.serializers import BookingDetailSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    bookings = BookingDetailSerializer(many=True, read_only=True)
    total_bookings = serializers.SerializerMethodField()
    total_spent = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'total_bookings', 'total_spent', 'bookings']

    def get_total_bookings(self, obj):
        return obj.bookings.count()

    def get_total_spent(self, obj):
        from django.db.models import Sum
        total = obj.bookings.filter(booking_status='CONFIRMED').aggregate(Sum('total_amount'))['total_amount__sum']
        return float(total) if total else 0.0
