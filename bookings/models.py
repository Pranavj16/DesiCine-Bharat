import uuid
from django.db import models
from django.contrib.auth.models import User
from theaters.models import Showtime, Seat

class SnackItem(models.Model):
    CATEGORY_CHOICES = [
        ('COMBO', 'Bollywood Blockbuster Combos'),
        ('SNACKS', 'Desi Snacks & Samosas'),
        ('BEVERAGES', 'Chai & Beverages'),
        ('POPCORN', 'Gourmet Popcorn'),
        ('DESSERT', 'Desi Sweet Treats'),
    ]

    name = models.CharField(max_length=100) # e.g. "Dilli 6 Masala Samosa (2 pcs) + Masala Chai"
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='COMBO')
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2) # in INR
    image_url = models.URLField(max_length=500, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'id']

    def __str__(self):

        return f"{self.name} - ₹{self.price}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Payment Pending'),
        ('CONFIRMED', 'Booking Confirmed'),
        ('CANCELLED', 'Booking Cancelled'),
    ]

    booking_id = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    ticket_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    snack_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    convenience_fee = models.DecimalField(max_digits=6, decimal_places=2, default=45.00)
    gst = models.DecimalField(max_digits=6, decimal_places=2, default=38.00)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    qr_code_data = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = 'DESI-' + uuid.uuid4().hex[:8].upper()
        if not self.qr_code_data:
            self.qr_code_data = f"TICKET:{self.booking_id}:{self.showtime_id}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.booking_id} - {self.user.username} ({self.showtime.movie.title})"


class BookedSeat(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booked_seats')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='booked_seats_all')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='booking_history')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('showtime', 'seat')

    def __str__(self):
        return f"{self.seat.row_label}{self.seat.seat_number} for {self.showtime}"


class BookingSnack(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='snacks')
    snack = models.ForeignKey(SnackItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.snack.name} for {self.booking.booking_id}"
