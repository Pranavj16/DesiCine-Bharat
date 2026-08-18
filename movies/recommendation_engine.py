import re
import math
from collections import Counter
from django.db.models import Q
from .models import Movie, Review
from bookings.models import Booking

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

class BollywoodRecommendationEngine:
    """
    Intelligent & High-Precision Recommendation Engine for Indian Cinema:
    1. Content-Based Filtering: High-precision matching on theme_tags, genre, synopsis, cast, director.
    2. Thematic & Mood Matcher: Strict topic semantic matching (Education, UPSC, Crime, Horror, Patriotism, Sports, Mythology, Romance).
    3. Ticket Booking Recommendations: Recommends complementary blockbusters when users are booking/confirming tickets.
    4. Genre Classification: Clean categorization of all films into 7 major Indian cinema genres.
    5. User-Affinity Filtering: Based on past bookings and user preference history.
    6. Trending & Box Office Blockbusters.
    """

    GENRE_TAXONOMY = {
        "Education & Inspirational": {
            "icon": "🎓",
            "keywords": ["education", "upsc", "student", "ias", "ips", "teacher", "school", "college", "exam", "coaching", "maths", "restart"],
            "description": "Inspiring journeys of student struggle, IAS/IPS exams, mentorship, and life lessons."
        },
        "Horror Comedy & Folklore": {
            "icon": "👻",
            "keywords": ["horror", "bhoot", "ghost", "chanderi", "manjulika", "munjya", "bhediya", "hastar", "supernatural", "curse", "folklore"],
            "description": "Spine-chilling scares blended with roaring comedy, Indian folklore, and creature fun."
        },
        "Crime, Underworld & Mafia": {
            "icon": "🕶️",
            "keywords": ["crime", "mafia", "gangster", "underworld", "violence", "syndicate", "shootout", "cartel", "narcotics", "smuggling"],
            "description": "High-octane crime sagas, red sandalwood cartels, coal mafia feuds, and intense thrillers."
        },
        "Patriotism & Armed Forces": {
            "icon": "🇮🇳",
            "keywords": ["patriotism", "army", "military", "war", "soldier", "surgical strike", "kargil", "air force", "spy", "raw", "nation"],
            "description": "Unsung bravery of Indian soldiers, air force fighter pilots, and covert black-ops."
        },
        "Mythology, Epics & Sci-Fi": {
            "icon": "🕉️",
            "keywords": ["mythology", "mahabharata", "kalki", "daiva", "panjurli", "hanuman", "god", "astraverse", "fantasy", "epic", "baahubali"],
            "description": "Grand Indian mythological lore, futuristic dystopian prophecies, and sacred tribal deities."
        },
        "Sports, Biopics & Survival": {
            "icon": "🏏",
            "keywords": ["sports", "wrestling", "cricket", "hockey", "athletics", "olympics", "world cup", "biopic", "survival", "guna caves", "coach"],
            "description": "Triumph of the underdog, true sports legends, and breathtaking real-life survival rescues."
        },
        "Romance, Musicals & Classics": {
            "icon": "❤️",
            "keywords": ["romance", "love", "ddlj", "geet", "wedding", "musical", "tragedy", "singing", "feel good", "classic", "sholay"],
            "description": "Timeless evergreen romances, legendary curry western classics, and soulful musical journeys."
        }
    }

    @staticmethod
    def _create_movie_soup(movie):
        """
        Creates a high-precision weighted metadata string for vectorization.
        Theme tags and genres are heavily weighted.
        """
        tags = (movie.theme_tags or '').replace(',', ' ')
        genres = (movie.genre or '').replace(',', ' ')

        soup_parts = [
            f"{tags} " * 8,         # Highest weight to explicit theme tags
            f"{genres} " * 6,       # High weight to genre taxonomy
            f"{movie.title} " * 3,
            f"{movie.director} " * 2,
            f"{movie.cast} " * 2,
            movie.tagline or '',
            movie.description or ''
        ]
        return " ".join(soup_parts).lower()

    @staticmethod
    def _calculate_cosine_similarity(text1, text2):
        """
        Zero-dependency pure-Python Cosine Vector Similarity.
        Guarantees serverless compatibility without external dependencies.
        """
        words1 = re.findall(r'\b\w+\b', text1.lower())
        words2 = re.findall(r'\b\w+\b', text2.lower())
        c1 = Counter(words1)
        c2 = Counter(words2)
        intersection = set(c1.keys()) & set(c2.keys())
        numerator = sum([c1[x] * c2[x] for x in intersection])
        sum1 = sum([c1[x]**2 for x in c1.keys()])
        sum2 = sum([c2[x]**2 for x in c2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            return 0.0
        return float(numerator) / denominator

    @classmethod
    def get_content_based_recommendations(cls, movie_id, top_n=6):
        """
        Returns top_n similar movies based on semantic and genre/theme similarity.
        Guarantees genre coherence and strict deduplication.
        """
        movies = list(Movie.objects.all())
        if len(movies) <= 1:
            return []

        target_idx = None
        for idx, m in enumerate(movies):
            if m.id == movie_id:
                target_idx = idx
                break

        if target_idx is None:
            return []

        target_movie = movies[target_idx]
        target_tags = set(w.lower() for w in (target_movie.theme_tags or '').replace(',', ' ').split() if len(w) > 2)
        target_genres = set(w.lower() for w in target_movie.genre.replace(',', ' ').split() if len(w) > 2)
        target_soup = cls._create_movie_soup(target_movie)

        scored_movies = []

        if HAS_SKLEARN:
            try:
                corpus = [cls._create_movie_soup(m) for m in movies]
                tfidf = TfidfVectorizer(stop_words='english', token_pattern=r'(?u)\b\w+\b', ngram_range=(1, 2))
                tfidf_matrix = tfidf.fit_transform(corpus)
                cosine_sim = cosine_similarity(tfidf_matrix[target_idx], tfidf_matrix).flatten()
            except Exception:
                cosine_sim = [cls._calculate_cosine_similarity(target_soup, cls._create_movie_soup(m)) for m in movies]
        else:
            cosine_sim = [cls._calculate_cosine_similarity(target_soup, cls._create_movie_soup(m)) for m in movies]

        for idx, score in enumerate(cosine_sim):
            if idx == target_idx:
                continue
            candidate = movies[idx]
            candidate_tags = set(w.lower() for w in (candidate.theme_tags or '').replace(',', ' ').split() if len(w) > 2)
            candidate_genres = set(w.lower() for w in candidate.genre.replace(',', ' ').split() if len(w) > 2)

            # Overlap boost
            tag_overlap = len(target_tags.intersection(candidate_tags))
            genre_overlap = len(target_genres.intersection(candidate_genres))

            if tag_overlap > 0 or genre_overlap > 0 or score > 0.05:
                rating_val = float(candidate.rating) if candidate.rating is not None else 8.0
                final_score = (score * 5.0) + (tag_overlap * 3.0) + (genre_overlap * 2.0) + (rating_val * 0.2)
                scored_movies.append((candidate, final_score))

        scored_movies.sort(key=lambda x: x[1], reverse=True)

        seen_ids = set()
        recs = []
        for m, _ in scored_movies:
            if m.id not in seen_ids and m.id != movie_id:
                seen_ids.add(m.id)
                recs.append(m)
            if len(recs) >= top_n:
                break

        if len(recs) < top_n:
            fallback = Movie.objects.exclude(id__in=[movie_id] + list(seen_ids)).order_by('-rating')[:top_n - len(recs)]
            recs.extend(fallback)

        return recs

    @classmethod
    def get_booking_recommendations(cls, movie_id, top_n=4):
        """
        Specialized recommendation for the ticket booking flow (seat selection & confirmation).
        Delivers high-affinity, complementary blockbuster suggestions.
        """
        return cls.get_content_based_recommendations(movie_id, top_n=top_n)

    @classmethod
    def recommend_by_thematic_topic(cls, topic, limit=12, top_n=None):
        """
        Multi-field semantic search across themes, plot synopsis, genre, title, cast, and director.
        """
        if top_n is not None:
            limit = top_n

        topic = (topic or '').strip().lower()
        if not topic:
            return cls.get_trending_bollywood_blockbusters(limit)

        q_filter = (
            Q(theme_tags__icontains=topic) |
            Q(genre__icontains=topic) |
            Q(title__icontains=topic) |
            Q(description__icontains=topic) |
            Q(cast__icontains=topic) |
            Q(director__icontains=topic)
        )

        matched_category = None
        for cat_name, cat_info in cls.GENRE_TAXONOMY.items():
            if topic in cat_name.lower() or any(topic == kw or kw in topic for kw in cat_info["keywords"]):
                matched_category = cat_name
                break

        if matched_category:
            cat_keywords = cls.GENRE_TAXONOMY[matched_category]["keywords"]
            for kw in cat_keywords:
                q_filter |= Q(theme_tags__icontains=kw) | Q(genre__icontains=kw) | Q(description__icontains=kw)

        matched_movies = Movie.objects.filter(q_filter).distinct()
        results = list(matched_movies.order_by('-rating')[:limit])
        if not results:
            results = list(cls.get_trending_bollywood_blockbusters(limit))

        return results

    @classmethod
    def classify_all_movies_by_genre(cls):
        """
        Classifies all movies in the database into the 7 primary Indian cinema taxonomies.
        """
        all_movies = list(Movie.objects.all())
        classified = {}

        for genre_name, info in cls.GENRE_TAXONOMY.items():
            keywords = info["keywords"]
            genre_movies = []

            for movie in all_movies:
                haystack = f"{movie.genre or ''} {movie.theme_tags or ''} {movie.description or ''} {movie.title}".lower()
                if any(kw in haystack for kw in keywords):
                    genre_movies.append(movie)

            genre_movies.sort(key=lambda m: m.rating, reverse=True)
            classified[genre_name] = {
                "icon": info["icon"],
                "description": info["description"],
                "count": len(genre_movies),
                "movies": genre_movies
            }

        return classified

    @classmethod
    def get_user_personalized_recommendations(cls, user, top_n=6):
        """
        Hybrid user recommendation based on past bookings and rating affinities.
        """
        if not user or not user.is_authenticated:
            return cls.get_trending_bollywood_blockbusters(limit=top_n)

        booked_movies = Movie.objects.filter(
            showtimes__bookings__user=user,
            showtimes__bookings__booking_status='CONFIRMED'
        ).distinct()

        if not booked_movies.exists():
            return cls.get_trending_bollywood_blockbusters(limit=top_n)

        user_genres = []
        user_tags = []
        for m in booked_movies:
            user_genres.extend([g.strip() for g in m.genre.split(',') if g.strip()])
            if m.theme_tags:
                user_tags.extend([t.strip() for t in m.theme_tags.split(',') if t.strip()])

        booked_ids = list(booked_movies.values_list('id', flat=True))
        q = Q()
        for g in set(user_genres):
            q |= Q(genre__icontains=g)
        for t in set(user_tags):
            q |= Q(theme_tags__icontains=t)

        recs = Movie.objects.filter(q).exclude(id__in=booked_ids).distinct().order_by('-rating')[:top_n]
        if len(recs) < top_n:
            more = Movie.objects.exclude(id__in=booked_ids).exclude(id__in=[r.id for r in recs]).order_by('-rating')[:top_n - len(recs)]
            recs = list(recs) + list(more)

        return recs

    # Alias for views compatibility
    get_topic_or_theme_recommendations = recommend_by_thematic_topic

    @classmethod
    def get_trending_bollywood_blockbusters(cls, limit=8, top_n=None):
        """
        Returns top trending blockbusters.
        """
        if top_n is not None:
            limit = top_n
        return list(Movie.objects.all().order_by('-rating')[:limit])
