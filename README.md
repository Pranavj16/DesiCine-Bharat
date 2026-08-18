# 🎬 DesiCine Cinema — Next-Gen Bollywood Ticket Booking & AI Recommendation Platform

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-blue.svg)](https://www.postgresql.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**DesiCine Cinema** is a full-stack Indian cinema ticketing platform built with **Django 6**, **Django REST Framework (DRF)**, and **Tailwind CSS**. It combines real-time seat reservation, an Indian UPI payment gateway simulation, an in-seat Desi snacks counter, and an **AI Thematic & Content-Based Recommendation Engine** tailored for Indian cinephiles.

---

## 🌟 Key Features

- **🎭 48 Handcrafted Indian Blockbusters**: Featuring authentic HD localized posters across Bollywood, Tollywood, Kollywood, Sandalwood, and Mollywood.
- **🧠 Thematic & Content-Based Recommendation Engine**:
  - **7-Genre Taxonomy**: *Education & Inspirational*, *Horror Comedy & Folklore*, *Crime & Underworld*, *Patriotism & Armed Forces*, *Mythology & Sci-Fi*, *Sports & Biopics*, and *Romance & Classics*.
  - **Thematic Keyword Matcher**: Queries themes, genres, plot points, actors, and directors with multi-field semantic scoring.
  - **Lifecycle Booking Recommendations**: Recommends complementary blockbusters directly during movie details, seat selection, and post-booking ticket confirmation.
- **💺 Interactive Dolby Atmos Seat Matrix**: Real-time visual seating layout across Recliner, Gold, and Silver acoustic classes.
- **🍿 Desi In-Seat Snack Counter**: Add Punjabi Samosas, Kulhad Masala Chai, Cheese Popcorn, and combos to bookings.
- **⚡ Indian Payment Simulator**: Support for Google Pay UPI, PhonePe, Paytm, and RuPay card checkouts.
- **🎟️ Digital Souvenir Entry Pass**: Generates a 70mm cinema ticket stub with a QR code and Pass ID.
- **📊 Real-Time Admin Analytics Dashboard**: Live visual KPIs tracking Gross Revenue, Ticket Sales, Multiplex Occupancy, and City-level stats.

---

## 🏗️ System Architecture

```mermaid
graph TD
    subgraph Client Layer
        A[Web Browser / Mobile Web]
        B[Pinterest-Style Dynamic UI]
        C[Interactive Seat Matrix & Soundwaves]
    end

    subgraph Presentation & Template Layer
        D[Django Templates / Tailwind CSS]
        E[Vanilla JS Async Fetch Client]
    end

    subgraph API Layer - Django REST Framework
        F[MovieViewSet /by_genre /recommend_by_topic]
        G[TheaterViewSet & ShowtimeViewSet]
        H[BookingViewSet & SnackViewSet]
        I[Admin Analytics API]
    end

    subgraph Business Logic & AI Engines
        J[Bollywood Recommendation Engine]
        K[Thematic Topic Matcher]
        L[Content-Based Cosine Similarity Engine]
        M[Seat Collision & Lock Manager]
        N[Fare & GST Calculator]
    end

    subgraph Storage & Infrastructure
        O[(PostgreSQL / SQLite Database)]
        P[WhiteNoise Static Storage]
        Q[Gunicorn WSGI Server]
    end

    A --> B
    B --> D
    D --> E
    E -->|REST API Requests| F & G & H & I
    F --> J
    J --> K & L
    H --> M & N
    F & G & H & I --> O
    P -->|Cached Posters & Static CSS| A
    Q --> E
```

---

## 🔄 Booking & Recommendation Data Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as Cinephile
    participant UI as DesiCine Frontend
    participant DRF as DRF API Layer
    participant AI as Recommendation Engine
    participant DB as Cloud Database (PostgreSQL)

    User->>UI: Selects Movie (e.g., 12th Fail)
    UI->>DRF: GET /api/movies/1/
    UI->>AI: GET /api/movies/1/recommendations/
    AI-->>UI: Returns similar films (Super 30, 3 Idiots, Nil Battey Sannata)
    User->>UI: Picks Showtime & Selects Seats (D4, D5)
    User->>UI: Adds Snacks (Samosa + Chai) & Selects GPay UPI
    UI->>DRF: POST /api/bookings/ (showtime, seats, snacks, payment)
    DRF->>DB: Atomic Transaction (Lock Seats, Create Booking, Generate Payment)
    DB-->>DRF: Booking Confirmed (ID: DESI-E479A527)
    DRF-->>UI: 201 Created with Ticket Details
    UI->>AI: GET /api/movies/1/booking_recommendations/
    AI-->>UI: Returns Next Weekend Suggestions
    UI->>User: Renders 70mm Digital Souvenir Pass + AI Next Show Recommendations
```

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/movies/` | `GET` | Paginated list of movies with filter parameters |
| `/api/movies/by_genre/` | `GET` | Organizes all 48 films into 7 Indian cinema genre categories |
| `/api/movies/recommend_by_topic/?topic=<name>` | `GET` | Thematic query matches across themes, plot, cast, and director |
| `/api/movies/{id}/recommendations/` | `GET` | Content-based recommendations for a specific movie |
| `/api/movies/{id}/booking_recommendations/` | `GET` | Complementary shows for seat selection & ticket confirmation |
| `/api/theaters/` | `GET` | Multiplexes, screens, and location details |
| `/api/showtimes/{id}/` | `GET` | Showtime details, pricing, and live seat layout |
| `/api/snacks/` | `GET` | In-seat Indian snacks menu |
| `/api/bookings/` | `POST` | Atomically books seats, adds snacks, and creates payment record |
| `/dashboard/api/analytics/` | `GET` | Gross revenue, ticket count, and occupancy metrics |

---

## 🚀 Quick Start Guide (Local Setup)

### 1. Prerequisites
- **Python 3.10+** (Python 3.12 recommended)
- **Git**

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/desicine-cinema.git
cd desicine-cinema
```

### 3. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy the template `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 6. Apply Migrations & Seed Bollywood Data
```bash
python manage.py migrate
python seed_bollywood_data.py
```

### 7. Run the Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Open **`http://127.0.0.1:8000/`** in your browser.

---

## ☁️ Production Cloud Deployment Guide

DesiCine Cinema is configured for cloud deployment on **Render**, **Railway**, **Fly.io**, **AWS**, or **Heroku**.

### 1. Environment Variables in Production
Set the following environment variables in your cloud hosting dashboard:

| Variable | Example Value | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | `your-secure-random-key` | Django secret key |
| `DEBUG` | `False` | Must be False in production |
| `ALLOWED_HOSTS` | `.onrender.com,.railway.app,yourdomain.com` | Allowed hostnames |
| `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com,https://yourdomain.com` | Trusted HTTPS origins |
| `DATABASE_URL` | `postgres://user:pass@host:5432/dbname?sslmode=require` | Cloud PostgreSQL connection string |

### 2. Build & Start Commands
- **Build Command**:
  ```bash
  pip install -r requirements.txt && python manage.py migrate && python seed_bollywood_data.py && python manage.py collectstatic --noinput
  ```
- **Start Command**:
  ```bash
  gunicorn config.wsgi:application --log-file -
  ```

---

## 🧪 Automated Test Suite

Run the full automated test suite verifying DRF endpoints, recommendation engine algorithms, and booking creation:

```bash
python test_drf_apis.py
```

---

## 📂 Project Directory Structure

```text
Movie Booking/
├── accounts/               # User authentication & profile management
├── admin_dashboard/        # Visual analytics & box-office telemetry
├── bookings/               # Seat reservation, snack ordering & ticket pass
├── config/                 # Root Django settings, URLs, WSGI & ASGI
├── movies/                 # Movies, genres & recommendation engine
│   ├── recommendation_engine.py  # AI Thematic & Content-Based algorithms
│   └── views.py            # DRF ViewSets & template views
├── payments/               # Payment models & UPI simulator
├── static/
│   ├── images/             # UI aesthetics & backdrop artwork
│   └── posters/            # 48 authentic localized movie posters (.jpg)
├── templates/              # Cinematic UI templates (Tailwind CSS)
│   ├── home.html           # Homepage & Genre Classifications
│   ├── movie_details.html  # Showtimes & Similar Movies
│   ├── seat_selection.html # Dolby Atmos Seat Matrix & In-booking recs
│   ├── checkout.html       # UPI Payment & Snack selection
│   ├── payment_success.html# Digital Souvenir Ticket Pass
│   └── admin_dashboard.html# Box office analytics
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── manage.py               # Django CLI management entrypoint
├── Procfile                # Production process runner for Gunicorn
├── requirements.txt        # Production Python dependencies
├── seed_bollywood_data.py  # 48-movie & multiplex seeder
└── test_drf_apis.py        # Automated test verification suite
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
