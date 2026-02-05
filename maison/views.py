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
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        maison = self.get_object()
        user = request.user
        # Vérifie si l'utilisateur a déjà liké
        liked = False
        like_obj = Like.objects.filter(maison=maison, user=user).first()
        if like_obj:
            like_obj.delete()
        else:
            Like.objects.create(maison=maison, user=user)
            liked = True

        likes_count = Like.objects.filter(maison=maison).count()
        return Response({'liked': liked, 'likes_count': likes_count}, status=status.HTTP_200_OK)
    
# ====Parcelles=================
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
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Publicite
from .serializers import PubliciteSerializer
import traceback
import logging

logger = logging.getLogger(__name__)

class PubliciteViewSet(viewsets.ModelViewSet):
    queryset = Publicite.objects.all()
    serializer_class = PubliciteSerializer

    def list(self, request, *args, **kwargs):
        try:
            # On récupère toutes les publicités
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True, context={'request': request})

            # On s'assure que chaque image est un lien absolu Cloudinary
            data = []
            for pub in serializer.data:
                if pub.get('photos'):
                    pub['photos'] = self.make_absolute_url(pub['photos'], request)
                data.append(pub)

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            print("🔥 ERREUR PUBLICITES 🔥")
            traceback.print_exc()  # Affiche la stack trace complète dans le terminal
            logger.error(f"Erreur PubliciteViewSet: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def make_absolute_url(self, url, request):
        """
        Transforme un chemin Cloudinary ou local en URL complète.
        """
        if not url:
            return None
        if url.startswith('http://') or url.startswith('https://'):
            return url
        if url.startswith('//'):
            return 'https:' + url
        slash = '' if url.startswith('/') else '/'
        return request.build_absolute_uri(f"{slash}{url}")

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




from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        ).order_by("created_at")


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")
