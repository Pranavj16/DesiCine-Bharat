#!/bin/bash
echo "🚀 Building DesiCine Cinema on Vercel..."
pip install -r requirements.txt
python manage.py collectstatic --noinput
echo "✅ Build completed successfully!"
