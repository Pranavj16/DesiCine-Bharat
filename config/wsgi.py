"""
WSGI config for DesiCine Cinema project.
Exposes WSGI callable as `application` for Gunicorn and `app` for Vercel Serverless Functions.
Includes automatic cloud database self-healing & migration for fresh serverless deployments.
"""

import os
import shutil
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 1. Initialize Django WSGI application
application = get_wsgi_application()

# 2. Serverless Cloud Database Auto-Migration & Seeding
# Automatically detects if tables exist in the connected database (PostgreSQL/Supabase/Neon/SQLite)
# and runs migrate + seed_data if the database is newly created.
try:
    from django.db import connection
    from django.core.management import call_command

    tables = connection.introspection.table_names()
    if 'movies_movie' not in tables:
        print("⚡ [DesiCine Cloud] Fresh database detected! Running auto-migrations...")
        call_command('migrate', interactive=False)
        print("🎬 [DesiCine Cloud] Auto-seeding 48 Indian blockbusters & multiplexes...")
        from seed_bollywood_data import seed_data
        seed_data()
        print("✅ [DesiCine Cloud] Database populated successfully!")
except Exception as e:
    print(f"⚠️ [DesiCine Cloud] Auto-init notice: {e}")

# Vercel serverless entrypoint
app = application
