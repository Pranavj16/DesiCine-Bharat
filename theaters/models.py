from django.db import models
from movies.models import Movie

class Theater(models.Model):
    CITY_CHOICES = [
        ('Mumbai', 'Mumbai'),
        ('Delhi-NCR', 'Delhi-NCR'),
        ('Bengaluru', 'Bengaluru'),
        ('Hyderabad', 'Hyderabad'),
        ('Chennai', 'Chennai'),
        ('Kolkata', 'Kolkata'),
        ('Pune', 'Pune'),
        ('Ahmedabad', 'Ahmedabad'),
        ('Jaipur', 'Jaipur'),
        ('Chandigarh', 'Chandigarh'),
    ]

    BRAND_CHOICES = [
        ('PVR INOX', 'PVR INOX Multiplex'),
        ('Cinepolis', 'Cinépolis VIP'),
        ('MovieMax', 'MovieMax Cinemas'),
        ('Miraj', 'Miraj Cinemas'),
        ('Carnival', 'Carnival Cinemas'),
    ]

    name = models.CharField(max_length=150)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, default='PVR INOX')
    city = models.CharField(max_length=50, choices=CITY_CHOICES, default='Mumbai')
    address = models.CharField(max_length=255)
    facilities = models.CharField(max_length=255, default='Dolby Atmos 7.1, 4K Laser, In-Seat Dining, Recliners')
    image_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):

        return f"{self.name} - {self.city}"


class Screen(models.Model):
    SCREEN_TYPES = [
        ('IMAX 3D', 'IMAX with Laser 3D'),
        ('Dolby Atmos 4K', 'Dolby Atmos 4K Laser'),
        ('4DX', '4DX Motion Experience'),
        ('ICE Immersive', 'ICE Immersive Experience'),
        ('Gold Class / INSIGNIA', 'INSIGNIA Luxury Lounge'),
        ('Standard 2D', 'Standard Digital 2D'),
    ]

    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='screens')
    screen_name = models.CharField(max_length=50) # e.g. "Screen 1 - IMAX", "Screen 2 - INSIGNIA"
    screen_type = models.CharField(max_length=50, choices=SCREEN_TYPES, default='Dolby Atmos 4K')
    total_rows = models.IntegerField(default=8) # Rows A to H
    total_cols = models.IntegerField(default=12) # 1 to 12 seats per row

    def __str__(self):
        return f"{self.theater.name} - {self.screen_name} ({self.screen_type})"


class Seat(models.Model):
    SEAT_TYPES = [
        ('SILVER', 'Silver Class (Front Rows)'),
        ('GOLD', 'Gold Prime (Center Executive)'),
        ('RECLINER', 'Royal Recliner (VIP Lounge)'),
    ]

    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='seats')
    row_label = models.CharField(max_length=5) # e.g. "A", "B", "C"
    seat_number = models.IntegerField() # e.g. 1, 2, 3...
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPES, default='GOLD')

    class Meta:
        unique_together = ('screen', 'row_label', 'seat_number')
        ordering = ['row_label', 'seat_number']

    def __str__(self):
        return f"{self.screen.screen_name} - {self.row_label}{self.seat_number} ({self.seat_type})"


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='showtimes')
    show_date = models.DateField()
    show_time = models.TimeField()
    language = models.CharField(max_length=50, default='Hindi')
    format = models.CharField(max_length=50, default='Dolby Atmos 4K')
    silver_price = models.DecimalField(max_digits=6, decimal_places=2, default=220.00)
    gold_price = models.DecimalField(max_digits=6, decimal_places=2, default=380.00)
    recliner_price = models.DecimalField(max_digits=6, decimal_places=2, default=650.00)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['show_date', 'show_time']

    def __str__(self):
        return f"{self.movie.title} at {self.screen.theater.name} ({self.show_date} {self.show_time})"
