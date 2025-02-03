from django.views import *
from rest_framework import generics
from .models import *
from django.http import HttpResponse

from .forms import *
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from django.http import JsonResponse

import json
from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.response import Response



from rest_framework.views import APIView
from rest_framework.response import Response


def home(request):
    return HttpResponse("Bienvenue sur Villana !")
#inscription
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer

class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Inscription réussie",
                "user": {
                    "username": user.username,
                    "phone_number": user.phone_number,
                    "email": user.email,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#connexion
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MaisonListView(APIView):
    def get(self, request):
        maisons = Maison.objects.all()
        serializer = MaisonSerializer(maisons, many=True, context={'request': request})  # Passer le contexte
        return Response(serializer.data)


def photo_list_view(request):
    photos = list(Photo.objects.values())  # Récupère les photos
    return JsonResponse(photos, safe=False)

def video_list_view(request):
    videos = list(Video.objects.values())  # Récupère les vidéos
    return JsonResponse(videos, safe=False)


class PubliciteViewSet(viewsets.ModelViewSet):
    queryset = Publicite.objects.all()
    serializer_class = PubliciteSerializer


def liste_pays(request):
    pays = list(pays.objects.all().values('nom', 'code', 'drapeau'))
    return JsonResponse(pays, safe=False)

def detect_country(request):
    code = request.GET.get('code')  # Récupérer le code du pays depuis la requête
    try:
        pays = Pays.objects.get(code=code)
        return JsonResponse({'nom': pays.nom, 'code': pays.code, 'drapeau': pays.drapeau.url})
    except Pays.DoesNotExist:
        return JsonResponse({'error': 'Pays non trouvé'}, status=404)
    
class ParcelleList(generics.ListCreateAPIView):
    queryset = Parcelle.objects.all()
    serializer_class = ParcelleSerializer

class ParcelleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parcelle.objects.all()
    serializer_class = ParcelleSerializer

class ParcellePhotoList(generics.ListCreateAPIView):
    queryset = ParcellePhoto.objects.all()
    serializer_class = ParcellePhotoSerializer

class ParcellePhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParcellePhoto.objects.all()
    serializer_class = ParcellePhotoSerializer

class HotelList(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelPhotoList(generics.ListCreateAPIView):
    queryset = HotelPhoto.objects.all()
    serializer_class = HotelPhotoSerializer

class HotelPhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelPhoto.objects.all()
    serializer_class = HotelPhotoSerializer





