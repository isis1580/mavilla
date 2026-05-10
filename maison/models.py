from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField
import uuid

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
    email = models.EmailField(unique=True)  # Simple et efficace
    avatar = CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_proprietaire = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email']

    objects = UserManager()

    def __str__(self):
         return str(self.username) if self.username else f"User {self.id}"

# =========================
# HELPERS
# =========================
class LocationMixin(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    adresse_complete = models.TextField(blank=True)
    
    class Meta:
        abstract = True

# =========================
# MAISONS
# =========================
class Maison(LocationMixin):
    TYPE_MAISON_CHOICES = [
        ('vente', 'À vendre'),
        ('location', 'À louer'),
        ('vacances', 'Location vacances'),
    ]
    
    CATEGORIE_CHOICES = [
        ('maison', 'Maison'),
        ('appartement', 'Appartement'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('duplex', 'Duplex'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_maisons", null=True, blank=True)
    type_maison = models.CharField(max_length=10, choices=TYPE_MAISON_CHOICES)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default='maison')
    titre = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    prix = models.DecimalField(max_digits=100, decimal_places=2)
    prix_promotion = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    nombre_chambres = models.PositiveIntegerField()
    nombre_salles_de_bain = models.PositiveIntegerField()
    nombre_salon = models.PositiveIntegerField(null=True, blank=True)
    nombre_cuisines = models.PositiveIntegerField(null=True, blank=True)
    surface = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    piscine = models.BooleanField(default=False)
    jardin = models.BooleanField(default=False)
    garage = models.BooleanField(default=False)
    climatiseur = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    meuble = models.BooleanField(default=False)
    quartier = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    pays = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    vue_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'{self.titre or self.type_maison} - {self.ville}'
    
    def increment_vue(self):
        self.vue_count += 1
        self.save(update_fields=['vue_count'])

class Photo(models.Model):
    maison = models.ForeignKey(Maison, related_name='photos', on_delete=models.CASCADE)
    photos = CloudinaryField('image', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    is_principale = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['ordre', 'id']

class Video(models.Model):
    maison = models.ForeignKey(Maison, related_name='videos', on_delete=models.CASCADE)
    video = CloudinaryField('video', blank=True, null=True)
    
    def __str__(self):
        return f'Vidéo de {self.maison}'

# =========================
# COMMENTAIRES & NOTES
# =========================
class Commentaire(models.Model):
    maison = models.ForeignKey(Maison, related_name='commentaires', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField()
    note = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date_creation']

class Like(models.Model):
    maison = models.ForeignKey(Maison, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('maison', 'user')

class Favori(models.Model):
    maison = models.ForeignKey(Maison, on_delete=models.CASCADE, related_name='favoris')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('maison', 'user')
        verbose_name = 'Favori'
        verbose_name_plural = 'Favoris'

# =========================
# RESIDENCES (Nouveau)
# =========================
class Residence(LocationMixin):
    TYPE_RESIDENCE_CHOICES = [
        ('residentiel', 'Résidentiel'),
        ('etudiant', 'Résidence étudiante'),
        ('senior', 'Résidence senior'),
        ('touristique', 'Résidence touristique'),
    ]
    ville = models.CharField(max_length=255)
    pays = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_residences")
    type_residence = models.CharField(max_length=20, choices=TYPE_RESIDENCE_CHOICES)
    nom = models.CharField(max_length=255)
    description = models.TextField()
    services_inclus = models.TextField(blank=True)  # JSON string des services
    reglement_interieur = models.TextField(blank=True)
    nombre_appartements = models.PositiveIntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nom

class ResidencePhoto(models.Model):
    residence = models.ForeignKey(Residence, related_name='photos', on_delete=models.CASCADE)
    photos = CloudinaryField('image', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['ordre', 'id']

# =========================
# HOTELS AMÉLIORÉS
# =========================
class Hotel(LocationMixin):
    CATEGORIE_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    
    TYPE_HOTEL_CHOICES = [
        ('hotel', 'Hôtel'),
        ('motel', 'Motel'),
        ('auberge', 'Auberge'),
        ('resort', 'Résort'),
        ('boutique', 'Hôtel boutique'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_hotels", null=True, blank=True)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    type_hotel = models.CharField(max_length=20, choices=TYPE_HOTEL_CHOICES, default='hotel')
    categorie = models.IntegerField(choices=CATEGORIE_CHOICES, default=3)
    prix_nuit = models.DecimalField(max_digits=10, decimal_places=2)
    services = models.TextField(blank=True)  # JSON string des services
    nombre_chambres = models.PositiveIntegerField(default=0)
    chambres_disponibles = models.PositiveIntegerField(default=0)
    heure_check_in = models.TimeField(default='14:00')
    heure_check_out = models.TimeField(default='12:00')
    ville = models.CharField(max_length=255)
    pays = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    note_moyenne = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f"{self.titre} ({'★' * self.categorie})"
    
    def update_note_moyenne(self):
        from django.db.models import Avg
        moyenne = self.notes.aggregate(Avg('note'))['note__avg'] or 0.0
        self.note_moyenne = round(moyenne, 2)
        self.save(update_fields=['note_moyenne'])

class HotelPhoto(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='photos', on_delete=models.CASCADE)
    photos = CloudinaryField('image', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    is_principale = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['ordre', 'id']

class HotelNote(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='notes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('hotel', 'user')

# =========================
# PARCELLES AMÉLIORÉES
# =========================
class Parcelle(LocationMixin):
    TYPE_PARCELLE_CHOICES = [
        ('agricole', 'Agricole'),
        ('residentielle', 'Résidentielle'),
        ('commerciale', 'Commerciale'),
        ('industrielle', 'Industrielle'),
        ('loisir', 'Loisir'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_parcelles", null=True, blank=True)
    type_parcelle = models.CharField(max_length=20, choices=TYPE_PARCELLE_CHOICES, default='residentielle')
    titre = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    prix = models.DecimalField(max_digits=20, decimal_places=2)
    surface = models.DecimalField(max_digits=10, decimal_places=2)
    quartier = models.CharField(max_length=100)
    ville = models.CharField(max_length=255)
    pays = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.titre or self.type_parcelle} - {self.surface}m² - {self.ville}"

class ParcellePhoto(models.Model):
    parcelle = models.ForeignKey(Parcelle, related_name='photos', on_delete=models.CASCADE)
    photos = CloudinaryField('image', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['ordre', 'id']

# =========================
# PUBLICITES
# =========================
class Publicite(models.Model):
    TYPE_PUB_CHOICES = [
        ('maison', 'Maison'),
        ('parcelle', 'Parcelle'),
        ('hotel', 'Hôtel'),
        ('residence', 'Résidence'),
        ('general', 'Général'),
    ]
    
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photos = CloudinaryField('image', blank=True, null=True)
    lien = models.URLField(blank=True, null=True)
    type_pub = models.CharField(max_length=20, choices=TYPE_PUB_CHOICES, default='general')
    ordre = models.PositiveIntegerField(default=0)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    clic_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.titre
    
    def increment_clic(self):
        self.clic_count += 1
        self.save(update_fields=['clic_count'])
    
    class Meta:
        ordering = ['ordre', '-date_debut']

# =========================
# PAYS
# =========================
class Pays(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    drapeau = CloudinaryField('image', blank=True, null=True)
    indicatif = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return self.nom

# =========================
# CONTACT & DEMANDES
# =========================
class Contact(models.Model):
    TYPE_CONTACT_CHOICES = [
        ('visite', 'Demande de visite'),
        ('info', 'Demande d\'information'),
        ('location', 'Demande de location'),
        ('achat', 'Demande d\'achat'),
        ('autre', 'Autre'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    sujet = models.CharField(max_length=255)
    message = models.TextField()
    type_contact = models.CharField(max_length=20, choices=TYPE_CONTACT_CHOICES, default='info')
    date_creation = models.DateTimeField(auto_now_add=True)
    is_traite = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.nom} - {self.sujet}"

class DemandeVisite(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('effectue', 'Effectué'),
    ]
    
    bien_type = models.CharField(max_length=50)  # 'maison', 'parcelle', 'hotel'
    bien_id = models.UUIDField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_souhaitee = models.DateTimeField()
    message = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Visite {self.bien_type} - {self.user.username}"

# =========================
# MESSAGES
# =========================
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
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
    
    class Meta:
        ordering = ['-created_at']

# =========================
# NOTIFICATIONS
# =========================
class Notification(models.Model):
    TYPE_CHOICES = [
        ('message', 'Message'),
        ('visite', 'Visite'),
        ('like', 'Like'),
        ('comment', 'Commentaire'),
        ('reservation', 'Réservation'),
        ('system', 'Système'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='system')
    data = models.JSONField(blank=True, null=True)  # Pour stocker des données supplémentaires
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

# =========================
# STATISTIQUES
# =========================
class Statistique(models.Model):
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=50)  # 'maison_vue', 'hotel_vue', 'user_inscription', etc.
    count = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('date', 'type')
        ordering = ['-date']