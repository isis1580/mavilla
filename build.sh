#!/usr/bin/env bash
# build.sh

echo "🚀 Installation des dépendances..."
pip install -r requirements.txt

echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Build terminé !"