# create_superuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'villana.settings')
django.setup()

from maison.models import User

phone = os.environ.get('DJANGO_SUPERUSER_PHONE', '80070699')
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@villana.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(phone_number=phone).exists():
    User.objects.create_superuser(
        phone_number=phone,
        username=username,
        email=email,
        password=password
    )
    print(f"✅ Superutilisateur {username} créé avec succès!")
else:
    print(f"ℹ️ Le superutilisateur {username} existe déjà.")