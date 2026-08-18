from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, Review
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewSerializer
from .recommendation_engine import BollywoodRecommendationEngine
from theaters.models import Showtime

# ==================== DRF VIEWSETS ====================

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        genre = self.request.query_params.get('genre')
        language = self.request.query_params.get('language')
        search = self.request.query_params.get('search')
        trending = self.request.query_params.get('trending')

        if genre and genre.lower() != 'all':
            qs = qs.filter(
                Q(genre__icontains=genre) |
                Q(theme_tags__icontains=genre) |
                Q(title__icontains=genre)
            )
        if language and language.lower() != 'all':
            qs = qs.filter(language__iexact=language)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(cast__icontains=search) |
                Q(director__icontains=search) |
                Q(genre__icontains=search) |
                Q(theme_tags__icontains=search) |
                Q(tagline__icontains=search) |
                Q(description__icontains=search)
            )
        if trending:
            qs = qs.filter(is_trending=True)
        return qs.distinct()

    @action(detail=True, methods=['get'])
    def recommendations(self, request, pk=None):
        """Content-based Bollywood recommendations for this movie."""
        movie = self.get_object()
        similar = BollywoodRecommendationEngine.get_content_based_recommendations(movie.id, top_n=6)
        serializer = MovieListSerializer(similar, many=True)
        return Response({
            'source_movie': movie.title,
            'recommendations': serializer.data
        })

    @action(detail=True, methods=['get'])
    def booking_recommendations(self, request, pk=None):
        """High-affinity movie recommendations shown during ticket booking flow."""
        movie = self.get_object()
        recs = BollywoodRecommendationEngine.get_booking_recommendations(movie.id, top_n=4)
        serializer = MovieListSerializer(recs, many=True)
        return Response({
            'booked_movie': movie.title,
            'recommendations_for_next_show': serializer.data
        })

    @action(detail=False, methods=['get'])
    def by_genre(self, request):
        """
        Genre Classification Endpoint:
        Returns all movies classified into 7 core Bollywood genres.
        """
        classified = BollywoodRecommendationEngine.classify_all_movies_by_genre()
        response_data = {}
        for genre_name, data in classified.items():
            serializer = MovieListSerializer(data["movies"], many=True)
            response_data[genre_name] = {
                "icon": data["icon"],
                "description": data["description"],
                "count": data["count"],
                "movies": serializer.data
            }
        return Response(response_data)

    @action(detail=False, methods=['get'])
    def personalized(self, request):
        """Personalized AI recommendations based on user viewing & booking habits."""
        user = request.user if request.user.is_authenticated else None
        recs = BollywoodRecommendationEngine.get_user_personalized_recommendations(user, top_n=6)
        serializer = MovieListSerializer(recs, many=True)
        return Response({
            'user': user.username if user else 'Guest (Bollywood Hits)',
            'personalized_recommendations': serializer.data
        })

    @action(detail=False, methods=['get'])
    def recommend_by_topic(self, request):
        """
        AI Semantic Topic & Mood Matcher:
        Recommends movies by specific topic/theme (e.g., 'Education', 'UPSC', 'Patriotism', 'Crime', 'Horror Comedy', 'Sports').
        """
        topic = request.query_params.get('topic', '').strip()
        recs = BollywoodRecommendationEngine.get_topic_or_theme_recommendations(topic, top_n=8)
        serializer = MovieListSerializer(recs, many=True)
        return Response({
            'topic': topic or 'Trending',
            'count': len(recs),
            'recommendations': serializer.data
        })

    @action(detail=False, methods=['get'])
    def trending_bollywood(self, request):
        """Top trending Indian and Bollywood blockbuster movies."""
        hits = BollywoodRecommendationEngine.get_trending_bollywood_blockbusters(top_n=8)
        serializer = MovieListSerializer(hits, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, pk=None):
        movie = self.get_object()
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================== TEMPLATE VIEWS ====================

def home(request):
    hero_12th = Movie.objects.filter(title__icontains='12th Fail').first() or Movie.objects.first()
    hero_stree = Movie.objects.filter(title__icontains='Stree 2').first() or Movie.objects.filter(title__icontains='Stree').first() or Movie.objects.last()
    now_showing = Movie.objects.filter(is_now_showing=True)[:16]
    trending = Movie.objects.order_by('-rating')[:5]
    classified_genres = BollywoodRecommendationEngine.classify_all_movies_by_genre()
    
    return render(request, "home.html", {
        'hero_12th': hero_12th,
        'hero_stree': hero_stree,
        'now_showing': now_showing,
        'trending_movies': trending,
        'classified_genres': classified_genres
    })

def movie_details(request, movie_id=None):
    if movie_id:
        movie = get_object_or_404(Movie, pk=movie_id)
    else:
        movie = Movie.objects.filter(is_trending=True).first() or Movie.objects.first()
    
    showtimes = Showtime.objects.filter(movie=movie, is_active=True).select_related('screen__theater')
    # Ticket Booking Recommendation Engine: fetch complementary similar blockbusters
    similar_movies = BollywoodRecommendationEngine.get_booking_recommendations(movie.id, top_n=6)

    return render(request, "movie_details.html", {
        'movie': movie,
        'showtimes': showtimes,
        'similar_movies': similar_movies
    })
