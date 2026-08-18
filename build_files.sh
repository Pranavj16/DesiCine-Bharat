#!/bin/bash
echo "🚀 Building DesiCine Cinema on Vercel..."
python3 -m pip install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
echo "✅ Build completed successfully!"
