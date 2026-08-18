from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Movie(models.Model):
    CERTIFICATION_CHOICES = [
        ('U', 'Universal (U)'),
        ('U/A', 'Parental Guidance (U/A)'),
        ('A', 'Adults Only (A)'),
        ('S', 'Special Class (S)'),
    ]

    LANGUAGE_CHOICES = [
        ('Hindi', 'Hindi (Bollywood)'),
        ('Telugu', 'Telugu (Tollywood)'),
        ('Tamil', 'Tamil (Kollywood)'),
        ('Malayalam', 'Malayalam (Mollywood)'),
        ('Kannada', 'Kannada (Sandalwood)'),
        ('Punjabi', 'Punjabi'),
        ('English', 'English (Hollywood Dubbed)'),
    ]

    title = models.CharField(max_length=150)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    genre = models.CharField(max_length=100) # e.g. "Action, Masala, Thriller"
    theme_tags = models.CharField(max_length=255, blank=True, null=True, help_text="Themes e.g. education, upsc, student, crime, horror")
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, default='Hindi')
    certification = models.CharField(max_length=10, choices=CERTIFICATION_CHOICES, default='U/A')
    duration = models.IntegerField(default=150, help_text="Duration in minutes")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=8.5)
    tomatometer = models.IntegerField(default=90, help_text="Audience Score percentage")
    poster = models.URLField(max_length=500)
    backdrop = models.URLField(max_length=500, blank=True, null=True)
    trailer_url = models.URLField(max_length=500, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    director = models.CharField(max_length=100, default='Bollywood Legend')
    cast = models.CharField(max_length=255, default='Superstar Ensemble')
    music_director = models.CharField(max_length=100, blank=True, null=True)
    is_trending = models.BooleanField(default=False)
    is_now_showing = models.BooleanField(default=True)
    is_bollywood_hit = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-rating', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.language})"


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} on {self.movie.title} - {self.rating}★"