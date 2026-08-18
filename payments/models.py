import uuid
from django.db import models
from bookings.models import Booking

class Payment(models.Model):
    METHOD_CHOICES = [
        ('UPI_GPAY', 'Google Pay UPI'),
        ('UPI_PHONEPE', 'PhonePe UPI'),
        ('UPI_PAYTM', 'Paytm UPI'),
        ('UPI_GENERIC', 'Generic UPI (BHIM/ID)'),
        ('CREDIT_CARD', 'Credit / Debit Card (RuPay/Visa/Mastercard)'),
        ('NET_BANKING', 'Net Banking (HDFC/SBI/ICICI/Axis)'),
    ]

    STATUS_CHOICES = [
        ('SUCCESS', 'Payment Completed'),
        ('FAILED', 'Payment Failed'),
        ('PENDING', 'Payment In-Progress'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=64, unique=True, editable=False)
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES, default='UPI_PHONEPE')
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUCCESS')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    upi_vpa = models.CharField(max_length=100, blank=True, null=True) # e.g. "user@okhdfcbank"
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = 'TXN_IND_' + uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_id} - {self.payment_status} (₹{self.amount})"
