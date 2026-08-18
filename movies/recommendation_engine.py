import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Q
from .models import Movie, Review
from bookings.models import Booking

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
        Creates a high-precision weighted metadata string for TF-IDF vectorization.
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

        # Build corpus
        corpus = [cls._create_movie_soup(m) for m in movies]

        try:
            tfidf = TfidfVectorizer(stop_words='english', token_pattern=r'(?u)\b\w+\b', ngram_range=(1, 2))
            tfidf_matrix = tfidf.fit_transform(corpus)
            cosine_sim = cosine_similarity(tfidf_matrix[target_idx], tfidf_matrix).flatten()

            scored_movies = []
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
                    final_score = (score * 5.0) + (tag_overlap * 3.0) + (genre_overlap * 2.0) + (candidate.rating * 0.2)
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

            return recs
        except Exception:
            return list(Movie.objects.exclude(id=movie_id).order_by('-rating')[:top_n])

    @classmethod
    def get_booking_recommendations(cls, movie_id, top_n=4):
        """
        Specialized recommendation method for ticket booking & confirmation flows.
        Returns high-affinity similar blockbusters to encourage next booking.
        """
        return cls.get_content_based_recommendations(movie_id=movie_id, top_n=top_n)

    @classmethod
    def classify_all_movies_by_genre(cls):
        """
        Classifies all movies in the database into the 7 primary Bollywood genre buckets.
        Returns a dictionary with genre metadata and list of matching movies.
        """
        all_movies = list(Movie.objects.all())
        classified = {}

        for genre_name, meta in cls.GENRE_TAXONOMY.items():
            matched_movies = []
            seen_ids = set()
            keywords = meta["keywords"]

            for movie in all_movies:
                text_to_check = f"{movie.genre} {movie.theme_tags} {movie.title} {movie.description}".lower()
                
                # Check keyword matches
                match_count = sum(1 for kw in keywords if kw in text_to_check)
                if match_count > 0 and movie.id not in seen_ids:
                    seen_ids.add(movie.id)
                    matched_movies.append((movie, match_count, movie.rating))

            # Sort by match strength and rating
            matched_movies.sort(key=lambda x: (x[1], x[2]), reverse=True)
            classified[genre_name] = {
                "icon": meta["icon"],
                "description": meta["description"],
                "count": len(matched_movies),
                "movies": [m[0] for m in matched_movies]
            }

        return classified

    @classmethod
    def get_topic_or_theme_recommendations(cls, topic_query, top_n=8):
        """
        AI Semantic Topic & Mood Matcher:
        Recommends movies strictly matching the user's selected topic.
        """
        if not topic_query:
            return cls.get_trending_bollywood_blockbusters(top_n)

        topic_clean = topic_query.lower().strip()
        all_movies = list(Movie.objects.all())

        topic_synonyms = {
            'education': ['education', 'upsc', 'student', 'school', 'college', 'engineering', 'maths', 'teacher', 'ias', 'ips', 'exam', 'coaching', 'study', 'restart'],
            'upsc': ['upsc', 'ias', 'ips', 'civil services', 'restart', 'exam', 'education', 'aspirant', 'student'],
            'crime': ['crime', 'mafia', 'gangster', 'underworld', 'cartel', 'violence', 'shootout', 'syndicate', 'smuggling', 'narcotics', 'dhanbad'],
            'horror': ['horror', 'ghost', 'bhoot', 'chanderi', 'manjulika', 'munjya', 'bhediya', 'hastar', 'supernatural', 'monster', 'folklore', 'curse'],
            'patriotism': ['patriotism', 'army', 'military', 'war', 'surgical strike', 'kargil', 'fighter', 'air force', 'raw', 'spy', 'soldier', 'nation', 'flag'],
            'sports': ['sports', 'wrestling', 'cricket', 'hockey', 'athletics', 'flying sikh', 'world cup', 'biopic', 'olympics', 'guna caves', 'survival', 'coach'],
            'mythology': ['mythology', 'kalki', 'mahabharata', 'panjurli', 'daiva', 'guliga', 'lord hanuman', 'astraverse', 'god', 'brahmashira', 'baahubali'],
            'romance': ['romance', 'love', 'ddlj', 'geet', 'raj simran', 'wedding', 'feel good', 'musical', 'aashiqui', 'heartbreak', 'romantic comedy', 'classic']
        }

        keywords = [topic_clean]
        for key, syn_list in topic_synonyms.items():
            if key in topic_clean or topic_clean in key:
                keywords = syn_list
                break

        scored_candidates = []
        for m in all_movies:
            m_text = f"{m.genre} {m.theme_tags} {m.title} {m.tagline} {m.description}".lower()
            match_score = 0.0

            for kw in keywords:
                if kw in (m.theme_tags or '').lower():
                    match_score += 4.0
                if kw in m.genre.lower():
                    match_score += 3.0
                if kw in m.title.lower():
                    match_score += 3.0
                if kw in (m.tagline or '').lower() or kw in (m.description or '').lower():
                    match_score += 1.0

            if match_score >= 1.0:
                final_rank = match_score + (float(m.rating) * 0.5)
                scored_candidates.append((m, final_rank))

        scored_candidates.sort(key=lambda x: x[1], reverse=True)

        seen_ids = set()
        results = []
        for m, _ in scored_candidates:
            if m.id not in seen_ids:
                seen_ids.add(m.id)
                results.append(m)
            if len(results) >= top_n:
                break

        return results

    @classmethod
    def get_user_personalized_recommendations(cls, user=None, top_n=6):
        """
        AI Affinity based on user's past bookings & ratings.
        """
        if not user or not user.is_authenticated:
            return cls.get_trending_bollywood_blockbusters(top_n)

        user_bookings = Booking.objects.filter(user=user).select_related('showtime__movie')
        booked_movies = [b.showtime.movie for b in user_bookings if b.showtime and b.showtime.movie]

        if not booked_movies:
            return cls.get_trending_bollywood_blockbusters(top_n)

        booked_tags = []
        for m in booked_movies:
            if m.theme_tags:
                booked_tags.extend(m.theme_tags.lower().split(','))
            if m.genre:
                booked_tags.extend(m.genre.lower().split(','))

        booked_movie_ids = {m.id for m in booked_movies}
        all_movies = Movie.objects.exclude(id__in=booked_movie_ids)

        scored = []
        for m in all_movies:
            m_text = f"{m.theme_tags} {m.genre}".lower()
            affinity = sum(1 for tag in booked_tags if tag.strip() in m_text)
            score = (affinity * 2.0) + (float(m.rating) * 0.5)
            scored.append((m, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        seen_ids = set()
        results = []
        for m, _ in scored:
            if m.id not in seen_ids:
                seen_ids.add(m.id)
                results.append(m)
            if len(results) >= top_n:
                break

        return results

    @staticmethod
    def get_trending_bollywood_blockbusters(top_n=8):
        """Returns top rated & trending Indian blockbuster films with strict deduplication."""
        movies = list(Movie.objects.filter(is_trending=True).order_by('-rating', '-tomatometer')[:top_n * 2])
        if len(movies) < top_n:
            movies += list(Movie.objects.order_by('-rating')[:top_n * 2])

        seen_ids = set()
        unique_hits = []
        for m in movies:
            if m.id not in seen_ids:
                seen_ids.add(m.id)
                unique_hits.append(m)
            if len(unique_hits) >= top_n:
                break

        return unique_hits
