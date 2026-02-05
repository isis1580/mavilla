from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


# -----------------------
# REGISTRATION & LOGIN
# -----------------------
class UserRegistrationSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    avatar = serializers.ImageField(required=False, allow_null=True)  # AJOUT avatar

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'password', 'avatar']

    def create(self, validated_data):
        return User.objects.create_user(
            phone_number=validated_data['phone_number'],
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            avatar=validated_data.get('avatar')
        )

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        if not user:
            raise serializers.ValidationError("Identifiants invalides.")
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'username': user.username,
                'phone_number': user.phone_number,
                'email': user.email,
                'avatar': user.avatar.url if user.avatar else None
            }
        }

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
# =========================
# PHOTOS & VIDEOS
# =========================
class PhotoSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['photos']

    def get_photos(self, obj):
        return absolute_url(self.context.get('request'), obj.photos)

class VideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['video']

    def get_video(self, obj):
        return absolute_url(self.context.get('request'), obj.video)

# =========================
# MAISONS
# =========================
class MaisonSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Maison
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        maison = Maison.objects.create(**validated_data)
        for photo in request.FILES.getlist('photos'):
            Photo.objects.create(maison=maison, photos=photo)
        for video in request.FILES.getlist('videos'):
            Video.objects.create(maison=maison, video=video)
        return maison

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
# HOTELS
# =========================
class HotelPhotoSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = HotelPhoto
        fields = ['photos']

    def get_photos(self, obj):
        return absolute_url(self.context.get('request'), obj.photos)

class HotelSerializer(serializers.ModelSerializer):
    photos = HotelPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        hotel = Hotel.objects.create(**validated_data)
        for photo in request.FILES.getlist('photos'):
            HotelPhoto.objects.create(hotel=hotel, photos=photo)
        return hotel

# =========================
# PARCELLES
# =========================
class ParcellePhotoSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = ParcellePhoto
        fields = ['photos']

    def get_photos(self, obj):
        return absolute_url(self.context.get('request'), obj.photos)

class ParcelleSerializer(serializers.ModelSerializer):
    photos = ParcellePhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Parcelle
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        parcelle = Parcelle.objects.create(**validated_data)
        for photo in request.FILES.getlist('photos'):
            ParcellePhoto.objects.create(parcelle=parcelle, photos=photo)
        return parcelle

# =========================
# PAYS
# =========================
class PaysSerializer(serializers.ModelSerializer):
    drapeau = serializers.SerializerMethodField()

    class Meta:
        model = Pays
        fields = ['nom', 'code', 'drapeau']

    def get_drapeau(self, obj):
        return absolute_url(self.context.get('request'), obj.drapeau)







# =========================
# MESSAGES
# =========================
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)
    receiver_name = serializers.CharField(source="receiver.username", read_only=True)

    class Meta:
        model = Message
        fields = "__all__"


# =========================
# NOTIFICATIONS
# =========================
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
