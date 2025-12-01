from rest_framework import serializers
from .models import *
from rest_framework import serializers

#inscription
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
#connexion
from rest_framework_simplejwt.tokens import RefreshToken

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # Peut être email, numéro ou username
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        from django.contrib.auth import authenticate
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Identifiants invalides.")

        # Génère des jetons JWT
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

 
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['photos']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')  # Récupérer la requête
        if instance.photos:  # Vérifiez si l'instance a une photo
            representation['photos'] = request.build_absolute_uri(instance.photos.url)  # Renvoie l'URL complète
        else:
            representation['photos'] = None  # Ou une valeur par défaut
        return representation
    

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video']

class MaisonSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Maison
        fields = '__all__'

    def create(self, validated_data):
        maison = Maison.objects.create(**validated_data)
        photos_data = self.context['request'].FILES.getlist('photos')
        videos_data = self.context['request'].FILES.getlist('videos')

        for photo_data in photos_data:
            Photo.objects.create(maison=maison, photos=photo_data)

        for video_data in videos_data:
            Video.objects.create(maison=maison, video=video_data)

        return maison

class PubliciteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicite
        fields = '__all__'  # Inclut tous les champs du modèle

class ParcellePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcellePhoto
        fields = ['photos']  # Incluez les champs nécessaires

class ParcelleSerializer(serializers.ModelSerializer):
    photos = ParcellePhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Parcelle
        fields = '__all__'  # Inclut tous les champs

    def create(self, validated_data):
        parcelle = Parcelle.objects.create(**validated_data)
        photos_data = self.context['request'].FILES.getlist('photos')

        for photo_data in photos_data:
            ParcellePhoto.objects.create(parcelle=parcelle, photos=photo_data)

        return parcelle

class HotelPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPhoto
        fields = ['photos']  # Incluez les champs nécessaires

class HotelSerializer(serializers.ModelSerializer):
    photos = HotelPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'  # Inclut tous les champs

    def create(self, validated_data):
        hotel = Hotel.objects.create(**validated_data)
        photos_data = self.context['request'].FILES.getlist('photos')

        for photo_data in photos_data:
            HotelPhoto.objects.create(hotel=hotel, photos=photo_data)

        return hotel


class ParcellePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcellePhoto
        fields = ['photos']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.photos:
            representation['photos'] = request.build_absolute_uri(instance.photos.url)
        else:
            representation['photos'] = None
        return representation

class HotelPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPhoto
        fields = ['photos']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.photos:
            representation['photos'] = request.build_absolute_uri(instance.photos.url)
        else:
            representation['photos'] = None
        return representation

class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = ['nom', 'code', 'drapeau']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.drapeau:
            representation['drapeau'] = request.build_absolute_uri(instance.drapeau.url)
        else:
            representation['drapeau'] = None
        return representation