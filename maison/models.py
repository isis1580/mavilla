from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from cloudinary.models import CloudinaryField

# =========================
# USER CUSTOM
# =========================
class UserManager(BaseUserManager):
    def create_user(self, phone_number, username, email=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Le numéro de téléphone est requis.")
        if not username:
            raise ValueError("Le nom d'utilisateur est requis.")
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")
        return self.create_user(phone_number, username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email']

    objects = UserManager()

    def __str__(self):
        return self.username

# =========================
# MAISONS
# =========================
class Maison(models.Model):
    TYPE_MAISON_CHOICES = [
        ('vente', 'À vendre'),
        ('location', 'À louer'),
    ]
    type_maison = models.CharField(max_length=10, choices=TYPE_MAISON_CHOICES)
    description = models.TextField()
    prix = models.DecimalField(max_digits=100, decimal_places=2)
    nombre_chambres = models.PositiveIntegerField()
    nombre_salles_de_bain = models.PositiveIntegerField()
    nombre_salon = models.PositiveIntegerField(null=True, blank=True)
    nombre_cuisines = models.PositiveIntegerField(null=True, blank=True)
    surface = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    piscine = models.BooleanField(default=False)
    quartier = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    pays = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type_maison} - {self.ville}'

class Photo(models.Model):
    maison = models.ForeignKey(Maison, related_name='photos', on_delete=models.CASCADE)
    photos = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return f'Photo de {self.maison}'

class Video(models.Model):
    maison = models.ForeignKey(Maison, related_name='videos', on_delete=models.CASCADE)
    video = CloudinaryField('video', blank=True, null=True)

    def __str__(self):
        return f'Vidéo de {self.maison}'

# =========================
# PUBLICITES
# =========================
class Publicite(models.Model):
    titre = models.CharField(max_length=255)
    photos = CloudinaryField('image', blank=True, null=True)
    lien = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titre

# =========================
# PARCELLES
# =========================
class Parcelle(models.Model):
    description = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    surface = models.DecimalField(max_digits=10, decimal_places=2)
    quartier = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class ParcellePhoto(models.Model):
    parcelle = models.ForeignKey(Parcelle, related_name='photos', on_delete=models.CASCADE)
    photos = CloudinaryField('image', blank=True, null=True)

# =========================
# HOTELS
# =========================
class Hotel(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class HotelPhoto(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='photos', on_delete=models.CASCADE)
    photos = CloudinaryField('image', blank=True, null=True)

# =========================
# PAYS
# =========================
class Pays(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    drapeau = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.nom



# =========================
# MESSAGES
# =========================
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        Notification.objects.create(
            user=self.receiver,
            title=f"Nouveau message de {self.sender.username}",
            body=self.text[:50],
            type="message"
        )

    def __str__(self):
        return f"{self.sender} → {self.receiver}"


# =========================
# NOTIFICATIONS
# =========================
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    type = models.CharField(max_length=50,  default="system")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
