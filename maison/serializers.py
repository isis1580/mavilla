from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

# =========================
# USERS
# =========================

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email'),
            password=validated_data['password']
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
            }
        }

# =========================
# HELPERS
# =========================

def absolute_url(request, filefield):
    if not filefield:
        return None
    try:
        return request.build_absolute_uri(filefield.url)
    except:
        return None

# =========================
# PHOTOS & VIDEOS
# =========================

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['photos']

    def to_representation(self, instance):
        request = self.context.get('request')
        return {'photos': absolute_url(request, instance.photos)}

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video']

    def to_representation(self, instance):
        request = self.context.get('request')
        return {'video': absolute_url(request, instance.video)}

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
    class Meta:
        model = Publicite
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        rep['photos'] = absolute_url(request, instance.photos)
        return rep

# =========================
# PARCELLES
# =========================

class ParcellePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcellePhoto
        fields = ['photos']

    def to_representation(self, instance):
        request = self.context.get('request')
        return {'photos': absolute_url(request, instance.photos)}

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
# HOTELS
# =========================

class HotelPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPhoto
        fields = ['photos']

    def to_representation(self, instance):
        request = self.context.get('request')
        return {'photos': absolute_url(request, instance.photos)}

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
# PAYS
# =========================

class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = ['nom', 'code', 'drapeau']

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        rep['drapeau'] = absolute_url(request, instance.drapeau)
        return rep
