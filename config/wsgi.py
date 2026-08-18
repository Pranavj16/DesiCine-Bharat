"""
WSGI config for DesiCine Cinema project.
Exposes WSGI callable as `application` for Gunicorn and `app` for Vercel Serverless Functions.
"""

import os
import shutil
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# If running on Vercel Serverless environment and using SQLite fallback, copy db to /tmp
BASE_DIR = Path(__file__).resolve().parent.parent
if os.getenv('VERCEL') == '1' and not os.getenv('DATABASE_URL'):
    tmp_db = Path('/tmp/db.sqlite3')
    local_db = BASE_DIR / 'db.sqlite3'
    if local_db.exists() and not tmp_db.exists():
        try:
            shutil.copy2(local_db, tmp_db)
        except Exception:
            pass

application = get_wsgi_application()

# Vercel serverless entrypoint
app = application
