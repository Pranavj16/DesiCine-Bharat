import os, sys, django

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Movie
from movies.recommendation_engine import BollywoodRecommendationEngine

topics = ['Education', 'UPSC', 'Crime', 'Horror', 'Patriotism', 'Sports', 'Mythology', 'Romance']

print('🎯 TESTING THEMATIC RECOMMENDATIONS:')
for t in topics:
    recs = BollywoodRecommendationEngine.get_topic_or_theme_recommendations(t, top_n=6)
    titles = [m.title for m in recs]
    print(f'📌 Topic: {t:12} -> {titles}')

print('\n🎯 TESTING CONTENT-BASED SIMILARITY:')
stree = Movie.objects.filter(title__icontains='Stree 2').first()
if stree:
    similar_stree = BollywoodRecommendationEngine.get_content_based_recommendations(stree.id, top_n=5)
    print(f'👻 Similar to "{stree.title}" -> {[m.title for m in similar_stree]}')

twelfth = Movie.objects.filter(title__icontains='12th Fail').first()
if twelfth:
    similar_12th = BollywoodRecommendationEngine.get_content_based_recommendations(twelfth.id, top_n=5)
    print(f'🎓 Similar to "{twelfth.title}" -> {[m.title for m in similar_12th]}')

animal = Movie.objects.filter(title__icontains='Animal').first()
if animal:
    similar_animal = BollywoodRecommendationEngine.get_content_based_recommendations(animal.id, top_n=5)
    print(f'🕶️ Similar to "{animal.title}" -> {[m.title for m in similar_animal]}')
