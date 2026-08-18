from rest_framework import serializers
from .models import Movie, Review
from django.contrib.auth.models import User

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'tagline', 'genre', 'theme_tags', 'language', 'certification',
            'duration', 'rating', 'tomatometer', 'poster', 'backdrop',
            'is_trending', 'is_now_showing', 'is_bollywood_hit'
        ]


class MovieDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    similar_movies = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'tagline', 'description', 'genre', 'theme_tags', 'language',
            'certification', 'duration', 'rating', 'tomatometer', 'poster',
            'backdrop', 'trailer_url', 'release_date', 'director', 'cast',
            'music_director', 'is_trending', 'is_now_showing', 'is_bollywood_hit',
            'reviews', 'similar_movies'
        ]

    def get_similar_movies(self, obj):
        from .recommendation_engine import BollywoodRecommendationEngine
        similar = BollywoodRecommendationEngine.get_content_based_recommendations(obj.id, top_n=4)
        return MovieListSerializer(similar, many=True).data
