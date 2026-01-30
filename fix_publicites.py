# fix_publicites.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "villana.settings")
django.setup()

from maison.models import Publicite

PLACEHOLDER_PATH = 'public/placeholder.jpg'  # mets ici un vrai fichier

for pub in Publicite.objects.all():
    try:
        _ = pub.photos.url
    except ValueError:
        pub.photos = PLACEHOLDER_PATH
        pub.save()
        print(f"Fixed Publicite {pub.id} with placeholder.")
