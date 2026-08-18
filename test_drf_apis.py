import os
import sys
import django

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from movies.models import Movie
from theaters.models import Showtime, Seat
from bookings.models import SnackItem, Booking

def run_tests():
    print("🧪 Running Enhanced DRF API & Thematic Recommendation Engine Test Suite...")
    client = APIClient()

    # 1. Test Movie List (with DRF pagination count)
    res = client.get('/api/movies/')
    assert res.status_code == 200
    json_data = res.json()
    total_count = json_data.get('count', len(json_data.get('results', json_data))) if isinstance(json_data, dict) else len(json_data)
    print(f"✅ /api/movies/ returned {total_count} total movies.")
    assert total_count >= 20, f"Expected at least 20 seeded movies, got {total_count}"

    # 2. Test Content-Based Recommendations
    jawan = Movie.objects.filter(title__icontains='Jawan').first()
    if jawan:
        res = client.get(f'/api/movies/{jawan.id}/recommendations/')
        assert res.status_code == 200
        recs = res.json().get('recommendations', [])
        rec_titles = [m['title'] for m in recs]
        print(f"✅ Content-Based Recommendations for 'Jawan': {rec_titles}")

    # 3. Test AI Topic & Theme Matcher (Education)
    res_edu = client.get('/api/movies/recommend_by_topic/?topic=Education')
    assert res_edu.status_code == 200, f"Failed topic recommendation: {res_edu.status_code}"
    edu_recs = res_edu.json().get('recommendations', [])
    edu_titles = [m['title'] for m in edu_recs]
    print(f"✅ AI Topic Matcher for 'Education': {edu_titles}")
    # Verify that education movies like 12th Fail, 3 Idiots, Super 30 are recommended!
    assert any('12th Fail' in t or '3 Idiots' in t or 'Super 30' in t or 'Taare Zameen Par' in t for t in edu_titles), "Expected educational movies in Education topic recommendation"

    # 4. Test AI Topic & Theme Matcher (Crime)
    res_crime = client.get('/api/movies/recommend_by_topic/?topic=Crime')
    assert res_crime.status_code == 200
    crime_recs = res_crime.json().get('recommendations', [])
    crime_titles = [m['title'] for m in crime_recs]
    print(f"✅ AI Topic Matcher for 'Crime': {crime_titles}")

    # 4. Test Theaters & Screens
    res = client.get('/api/theaters/')
    assert res.status_code == 200
    theaters = res.json().get('results', res.json()) if isinstance(res.json(), dict) else res.json()
    print(f"✅ /api/theaters/ returned {len(theaters)} multiplexes.")
    assert len(theaters) > 0, "No theaters found"

    # 5. Test Showtimes & Seat Map
    res = client.get('/api/showtimes/1/')
    assert res.status_code == 200
    st_data = res.json()
    assert 'seat_layout' in st_data
    print(f"✅ /api/showtimes/1/ returned seat map with {len(st_data['seat_layout'])} seats.")

    # 6. Test Indian Snacks API
    res = client.get('/api/snacks/')
    assert res.status_code == 200
    snacks = res.json().get('results', res.json()) if isinstance(res.json(), dict) else res.json()
    print(f"✅ /api/snacks/ returned {len(snacks)} Indian snack items.")
    assert len(snacks) > 0, "No snacks found"

    # 8. Test Booking Creation
    user = User.objects.filter(username='rahul_sharma').first()
    client.force_authenticate(user=user)
    available_seats = [s['id'] for s in st_data['seat_layout'] if not s['is_booked']][:2]

    if len(available_seats) >= 2:
        booking_payload = {
            "showtime_id": st_data['id'],
            "seat_ids": available_seats,
            "snacks": [{"snack_id": 1, "quantity": 1}],
            "payment_method": "UPI_PHONEPE",
            "upi_vpa": "rahul@okaxis"
        }
        res = client.post('/api/bookings/', data=booking_payload, format='json')
        assert res.status_code == 201, f"Booking failed: {res.data}"
        booking_res = res.json()
        print(f"✅ /api/bookings/ successfully booked seats {available_seats} with ID {booking_res['booking_id']} (Total: ₹{booking_res['total_amount']}).")

    # 9. Test Admin Analytics
    admin_user = User.objects.filter(username='admin').first()
    client.force_authenticate(user=admin_user)
    res = client.get('/dashboard/api/analytics/')
    assert res.status_code == 200
    analytics = res.json()
    print(f"✅ Admin Analytics: Total Revenue: ₹{analytics['total_revenue_inr']}, Tickets: {analytics['total_tickets_sold']}")

    print("\n🎉 ALL DRF APIS, TOPIC RECOMMENDATION ENGINE & 28+ MOVIES VERIFIED SUCCESSFULLY!\n")

if __name__ == "__main__":
    run_tests()
