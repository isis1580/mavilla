from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Avg, Count, Q

# -----------------------
# HELPERS
# -----------------------
def absolute_url(request, filefield):
    if not filefield:
        return None
    try:
        return filefield.url  # CloudinaryField fournit directement l'URL publique
    except:
        return None

# -----------------------
# REGISTRATION & LOGIN
# -----------------------
class UserRegistrationSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'password', 'avatar', 'is_proprietaire']

    def create(self, validated_data):
        return User.objects.create_user(
            phone_number=validated_data['phone_number'],
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            avatar=validated_data.get('avatar'),
            is_proprietaire=validated_data.get('is_proprietaire', False)
        )

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        from django.contrib.auth import authenticate
        
        # Essayer avec le phone_number comme username
        user = authenticate(
            username=data.get('phone_number'),
            password=data.get('password')
        )
        
        if not user:
            raise serializers.ValidationError("Identifiants invalides.")
        
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'phone_number': user.phone_number,
                'email': user.email,
                'avatar': user.avatar.url if user.avatar else None,
                'is_proprietaire': user.is_proprietaire,
                'is_verified': user.is_verified
            }
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'email', 'avatar', 
                 'is_proprietaire', 'is_verified', 'date_joined']
        read_only_fields = ['date_joined']

# =========================
# PHOTOS & VIDEOS
# =========================
class PhotoSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'photos', 'ordre', 'is_principale']

    def get_photos(self, obj):
        return absolute_url(self.context.get('request'), obj.photos)

class VideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'video']

    def get_video(self, obj):
        return absolute_url(self.context.get('request'), obj.video)

# =========================
# COMMENTAIRES & LIKES
# =========================
class CommentaireSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Commentaire
        fields = ['id', 'user', 'user_name', 'user_avatar', 'texte', 'note',
                 'date_creation', 'date_modification', 'is_approved']
        read_only_fields = ['user', 'date_creation', 'date_modification']
    
    def get_user_avatar(self, obj):
        if obj.user.avatar:
            return obj.user.avatar.url
        return None
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'maison', 'date_creation']
        read_only_fields = ['user', 'date_creation']

class FavoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favori
        fields = ['id', 'user', 'maison', 'date_creation']
        read_only_fields = ['user', 'date_creation']

# =========================
# MAISONS
# =========================
class MaisonSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    commentaires = CommentaireSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    commentaires_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_favori = serializers.SerializerMethodField()
    note_moyenne = serializers.SerializerMethodField()
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Maison
        fields = '__all__'
        read_only_fields = ['id', 'date_creation', 'date_modification', 'vue_count']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_commentaires_count(self, obj):
        return obj.commentaires.filter(is_approved=True).count()
    
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False
    
    def get_is_favori(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favoris.filter(user=user).exists()
        return False
    
    def get_note_moyenne(self, obj):
        moyenne = obj.commentaires.filter(note__isnull=False).aggregate(Avg('note'))['note__avg']
        return round(moyenne, 2) if moyenne else 0.0
    
    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        maison = Maison.objects.create(**validated_data)
        
        # Gestion des photos
        for index, photo in enumerate(request.FILES.getlist('photos')):
            Photo.objects.create(
                maison=maison, 
                photos=photo,
                ordre=index,
                is_principale=(index == 0)
            )
        
        # Gestion des vidéos
        for video in request.FILES.getlist('videos'):
            Video.objects.create(maison=maison, video=video)
        
        return maison

# =========================
# RECHERCHE & FILTRES
# =========================
class RechercheMaisonSerializer(serializers.Serializer):
    type_maison = serializers.CharField(required=False)
    categorie = serializers.CharField(required=False)
    ville = serializers.CharField(required=False)
    pays = serializers.CharField(required=False)
    min_prix = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_prix = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_chambres = serializers.IntegerField(min_value=0, required=False)
    min_salles_bain = serializers.IntegerField(min_value=0, required=False)
    min_surface = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)
    max_surface = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)
    piscine = serializers.BooleanField(required=False)
    jardin = serializers.BooleanField(required=False)
    garage = serializers.BooleanField(required=False)
    meuble = serializers.BooleanField(required=False)
    latitude = serializers.DecimalField(max_digits=10, decimal_places=7, required=False)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=7, required=False)
    rayon_km = serializers.IntegerField(min_value=1, default=10, required=False)
    
    def search(self, queryset):
        validated_data = self.validated_data
        
        if validated_data.get('ville'):
            queryset = queryset.filter(ville__icontains=validated_data['ville'])
        
        if validated_data.get('pays'):
            queryset = queryset.filter(pays__icontains=validated_data['pays'])
        
        if validated_data.get('type_maison'):
            queryset = queryset.filter(type_maison=validated_data['type_maison'])
        
        if validated_data.get('categorie'):
            queryset = queryset.filter(categorie=validated_data['categorie'])
        
        if validated_data.get('min_prix'):
            queryset = queryset.filter(prix__gte=validated_data['min_prix'])
        
        if validated_data.get('max_prix'):
            queryset = queryset.filter(prix__lte=validated_data['max_prix'])
        
        if validated_data.get('min_chambres'):
            queryset = queryset.filter(nombre_chambres__gte=validated_data['min_chambres'])
        
        if validated_data.get('min_salles_bain'):
            queryset = queryset.filter(nombre_salles_de_bain__gte=validated_data['min_salles_bain'])
        
        if validated_data.get('min_surface'):
            queryset = queryset.filter(surface__gte=validated_data['min_surface'])
        
        if validated_data.get('max_surface'):
            queryset = queryset.filter(surface__lte=validated_data['max_surface'])
        
        if validated_data.get('piscine') is not None:
            queryset = queryset.filter(piscine=validated_data['piscine'])
        
        if validated_data.get('jardin') is not None:
            queryset = queryset.filter(jardin=validated_data['jardin'])
        
        if validated_data.get('garage') is not None:
            queryset = queryset.filter(garage=validated_data['garage'])
        
        if validated_data.get('meuble') is not None:
            queryset = queryset.filter(meuble=validated_data['meuble'])
        
        # Recherche par géolocalisation
        if validated_data.get('latitude') and validated_data.get('longitude'):
            point = Point(float(validated_data['longitude']), float(validated_data['latitude']))
            rayon = validated_data.get('rayon_km', 10) * 1000  # Conversion en mètres
            
            # Filtrage par distance (nécessite l'extension PostGIS)
            queryset = queryset.filter(
                latitude__isnull=False,
                longitude__isnull=False
            ).extra(
                where=[f"""
                    ST_DistanceSphere(
                        ST_MakePoint(longitude, latitude),
                        ST_MakePoint({point.x}, {point.y})
                    ) <= {rayon}
                """]
            )
        
        return queryset.filter(is_active=True)

# =========================
# HOTELS
# =========================
class HotelPhotoSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = HotelPhoto
        fields = ['id', 'photos', 'ordre', 'is_principale']

    def get_photos(self, obj):
        return absolute_url(self.context.get('request'), obj.photos)

class HotelNoteSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = HotelNote
        fields = ['id', 'user', 'user_name', 'note', 'commentaire', 'date_creation']
        read_only_fields = ['user', 'date_creation']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class HotelSerializer(serializers.ModelSerializer):
    photos = HotelPhotoSerializer(many=True, read_only=True)
    notes = HotelNoteSerializer(many=True, read_only=True)
    note_moyenne = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    notes_count = serializers.SerializerMethodField()
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ['id', 'date_creation', 'note_moyenne']
    
    def get_notes_count(self, obj):
        return obj.notes.count()
    
    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        hotel = Hotel.objects.create(**validated_data)
        
        for index, photo in enumerate(request.FILES.getlist('photos')):
            HotelPhoto.objects.create(
                hotel=hotel, 
                photos=photo,
                ordre=index,
                is_principale=(index == 0)
            )
        return hotel

# =========================
# RESIDENCES
# =========================
class ResidencePhotoSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = ResidencePhoto
        fields = ['id', 'photos', 'ordre']

    def get_photos(self, obj):
        return absolute_url(self.context.get('request'), obj.photos)

class ResidenceSerializer(serializers.ModelSerializer):
    photos = ResidencePhotoSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Residence
        fields = '__all__'
        read_only_fields = ['id', 'date_creation']
    
    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        residence = Residence.objects.create(**validated_data)
        
        for index, photo in enumerate(request.FILES.getlist('photos')):
            ResidencePhoto.objects.create(
                residence=residence, 
                photos=photo,
                ordre=index
            )
        return residence

# =========================
# PARCELLES
# =========================
class ParcellePhotoSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = ParcellePhoto
        fields = ['id', 'photos', 'ordre']

    def get_photos(self, obj):
        return absolute_url(self.context.get('request'), obj.photos)

class ParcelleSerializer(serializers.ModelSerializer):
    photos = ParcellePhotoSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Parcelle
        fields = '__all__'
        read_only_fields = ['id', 'date_creation', 'date_modification']
    
    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        parcelle = Parcelle.objects.create(**validated_data)
        
        for index, photo in enumerate(request.FILES.getlist('photos')):
            ParcellePhoto.objects.create(
                parcelle=parcelle, 
                photos=photo,
                ordre=index
            )
        return parcelle

# =========================
# PUBLICITES
# =========================
class PubliciteSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Publicite
        fields = '__all__'

    def get_photos(self, obj):
        return absolute_url(self.context.get('request'), obj.photos)

# =========================
# PAYS
# =========================
class PaysSerializer(serializers.ModelSerializer):
    drapeau = serializers.SerializerMethodField()

    class Meta:
        model = Pays
        fields = ['id', 'nom', 'code', 'drapeau', 'indicatif']

    def get_drapeau(self, obj):
        return absolute_url(self.context.get('request'), obj.drapeau)

# =========================
# CONTACT & DEMANDES
# =========================
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['date_creation', 'is_traite']

class DemandeVisiteSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = DemandeVisite
        fields = '__all__'
        read_only_fields = ['user', 'date_creation', 'date_modification']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

# =========================
# MESSAGES
# =========================
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)
    receiver_name = serializers.CharField(source="receiver.username", read_only=True)
    sender_avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ['sender', 'created_at', 'is_read']
    
    def get_sender_avatar(self, obj):
        if obj.sender.avatar:
            return obj.sender.avatar.url
        return None
    
    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

# =========================
# NOTIFICATIONS
# =========================
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ['user', 'created_at']

# =========================
# STATISTIQUES
# =========================
class StatistiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistique
        fields = '__all__'

# =========================
# DASHBOARD
# =========================
class DashboardSerializer(serializers.Serializer):
    total_maisons = serializers.IntegerField()
    total_parcelles = serializers.IntegerField()
    total_hotels = serializers.IntegerField()
    total_residences = serializers.IntegerField()
    total_users = serializers.IntegerField()
    nouvelles_demandes = serializers.IntegerField()
    revenu_mensuel = serializers.DecimalField(max_digits=12, decimal_places=2)
    top_villes = serializers.DictField(child=serializers.IntegerField())