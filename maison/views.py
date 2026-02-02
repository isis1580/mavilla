from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from .models import *
from .serializers import *


# =========================
# Home
# =========================
def home(request):
    return HttpResponse("Bienvenue sur Villana !")


# =========================
# Auth
# =========================
class UserRegistrationView(APIView):
    def post(self, request):
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


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# Maisons
# =========================
class MaisonViewSet(viewsets.ModelViewSet):
    queryset = Maison.objects.all()
    serializer_class = MaisonSerializer

    def get_serializer_context(self):
        return {"request": self.request}


# =========================
# Parcelles
# =========================
class ParcelleViewSet(viewsets.ModelViewSet):
    queryset = Parcelle.objects.all()
    serializer_class = ParcelleSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class ParcellePhotoViewSet(viewsets.ModelViewSet):
    queryset = ParcellePhoto.objects.all()
    serializer_class = ParcellePhotoSerializer

    def get_serializer_context(self):
        return {"request": self.request}


# =========================
# Hotels
# =========================
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class HotelPhotoViewSet(viewsets.ModelViewSet):
    queryset = HotelPhoto.objects.all()
    serializer_class = HotelPhotoSerializer

    def get_serializer_context(self):
        return {"request": self.request}


# =========================
# Publicités
# =========================
class PubliciteViewSet(viewsets.ModelViewSet):
    queryset = Publicite.objects.all()
    serializer_class = PubliciteSerializer

    def get_serializer_context(self):
        return {"request": self.request}


# =========================
# Pays
# =========================
def liste_pays(request):
    pays_list = list(Pays.objects.all().values('nom', 'code', 'drapeau'))
    return JsonResponse(pays_list, safe=False)


def detect_country(request):
    code = request.GET.get('code')
    try:
        pays = Pays.objects.get(code=code)
        return JsonResponse({'nom': pays.nom, 'code': pays.code, 'drapeau': pays.drapeau.url})
    except Pays.DoesNotExist:
        return JsonResponse({'error': 'Pays non trouvé'}, status=404)


# =========================
# Media debug
# =========================
def photo_list_view(request):
    photos = list(Photo.objects.values())
    return JsonResponse(photos, safe=False)


def video_list_view(request):
    videos = list(Video.objects.values())
    return JsonResponse(videos, safe=False)
