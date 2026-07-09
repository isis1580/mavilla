from rest_framework import viewsets, status, filters, generics
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone

from django.contrib.contenttypes.models import ContentType
import logging
import traceback
import os
from django.conf import settings
import firebase_admin
from firebase_admin import credentials, messaging

# Initialisation de Firebase
if not firebase_admin._apps:
    try:
        cert_path = os.path.join(settings.BASE_DIR, 'serviceAccountKey.json')
        if os.path.exists(cert_path):
            cred = credentials.Certificate(cert_path)
            firebase_admin.initialize_app(cred)
        else:
            # Initialisation par défaut (utile si configuré via env vars GOOGLE_APPLICATION_CREDENTIALS)
            firebase_admin.initialize_app()
    except Exception as e:
        print(f"⚠️ Firebase non initialisé: {e}")

logger = logging.getLogger(__name__)

from .models import *
from .serializers import *

# =========================
# MIXINS
# =========================
class PropertyActionMixin:
    """Mixin pour gérer les likes, favoris et commentaires génériques"""

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        content_type = ContentType.objects.get_for_model(obj)

        like_obj = Like.objects.filter(user=user, content_type=content_type, object_id=obj.id).first()
        liked = False
        if like_obj:
            like_obj.delete()
        else:
            Like.objects.create(user=user, content_type=content_type, object_id=obj.id)
            liked = True

            # Notification au propriétaire
            if hasattr(obj, 'owner') and obj.owner and obj.owner != user:
                model_name = obj._meta.verbose_name.lower()
                Notification.objects.create(
                    user=obj.owner,
                    title=f"Votre {model_name} a été aimé(e)",
                    body=f"{user.username} a aimé votre {model_name}",
                    type="like",
                    data={f"{model_name}_id": str(obj.id)}
                )

        return Response({'liked': liked, 'likes_count': obj.likes.count()}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def favori(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        content_type = ContentType.objects.get_for_model(obj)

        favori_obj = Favori.objects.filter(user=user, content_type=content_type, object_id=obj.id).first()
        favori = False
        if favori_obj:
            favori_obj.delete()
        else:
            Favori.objects.create(user=user, content_type=content_type, object_id=obj.id)
            favori = True

        return Response({'favori': favori}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def commenter(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        texte = request.data.get('texte')
        note = request.data.get('note')
        content_type = ContentType.objects.get_for_model(obj)

        if not texte:
            return Response({'error': 'Le texte du commentaire est requis.'}, status=status.HTTP_400_BAD_REQUEST)

        commentaire = Commentaire.objects.create(
            content_type=content_type,
            object_id=obj.id,
            user=user,
            texte=texte,
            note=note
        )

        # Mettre à jour la note moyenne si c'est un hôtel
        if hasattr(obj, 'update_note_moyenne'):
            obj.update_note_moyenne()

        # Notification au propriétaire
        if hasattr(obj, 'owner') and obj.owner and obj.owner != user:
            model_name = obj._meta.verbose_name.lower()
            Notification.objects.create(
                user=obj.owner,
                title=f"Nouveau commentaire sur votre {model_name}",
                body=f"{user.username} a commenté votre {model_name}",
                type="comment",
                data={f"{model_name}_id": str(obj.id), "commentaire_id": commentaire.id}
            )

        serializer = CommentaireSerializer(commentaire)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET'], permission_classes=[AllowAny])
    def commentaires(self, request, pk=None):
        obj = self.get_object()
        content_type = ContentType.objects.get_for_model(obj)
        commentaires = Commentaire.objects.filter(
            content_type=content_type,
            object_id=obj.id,
            is_approved=True
        ).order_by('-date_creation')
        serializer = CommentaireSerializer(commentaires, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def mes_favoris(self, request):
        user = request.user
        content_type = ContentType.objects.get_for_model(self.queryset.model)
        favoris = Favori.objects.filter(user=user, content_type=content_type)

        # Récupérer les IDs des objets favoris
        object_ids = favoris.values_list('object_id', flat=True)
        queryset = self.queryset.model.objects.filter(id__in=object_ids)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], permission_classes=[AllowAny])
    def statistiques(self, request, pk=None):
        obj = self.get_object()
        data = {
            'vue_count': getattr(obj, 'vue_count', 0),
            'likes_count': obj.likes.count(),
            'commentaires_count': obj.commentaires.filter(is_approved=True).count(),
            'note_moyenne': obj.commentaires.filter(note__isnull=False)
                .aggregate(Avg('note'))['note__avg'] or 0.0
        }
        return Response(data)

# =========================
# PAGINATION
# =========================
class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# =========================
# HOME
# =========================
def home(request):
    return HttpResponse("Bienvenue sur Villana - Plateforme Immobilière")

# =========================
# AUTH
# =========================
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.error(f"🔍 DONNÉES REÇUES: {request.data}")  # ← CHANGÉ
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Inscription réussie",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "phone_number": user.phone_number,
                    "email": user.email,
                    "is_staff": user.is_staff
                }
            }, status=status.HTTP_201_CREATED)
        
        logger.error(f"❌ ERREURS: {serializer.errors}")  # ← CHANGÉ
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import traceback

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.error("=== DÉBUT DE LA REQUÊTE LOGIN ===")
        logger.error(f"Données reçues: {request.data}")

        try:
            serializer = UserLoginSerializer(data=request.data)

            if serializer.is_valid():
                logger.error("✅ Sérialiseur valide, authentification réussie")
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            else:
                logger.error(f"❌ Sérialiseur invalide: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error("🔥🔥🔥 EXCEPTION CATASTROPHIQUE DANS LA VUE LOGIN 🔥🔥🔥")
            logger.error(f"Type d'exception: {type(e).__name__}")
            logger.error(f"Message: {str(e)}")
            logger.error("Traceback complet:")
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Erreur interne du serveur", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =========================
# MAISONS
# =========================
class MaisonViewSet(PropertyActionMixin, viewsets.ModelViewSet):
    queryset = Maison.objects.filter(is_active=True)
    serializer_class = MaisonSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre', 'description', 'ville', 'quartier', 'pays']
    ordering_fields = ['prix', 'date_creation', 'surface', 'vue_count']
    ordering = ['-date_creation']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_vue()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        # Si on demande les annonces d'un owner spécifique, on montre TOUT (même inactif)
        owner_id = self.request.query_params.get('owner')
        if owner_id:
            return Maison.objects.filter(owner_id=owner_id).order_by('-date_creation')

        # Sinon, comportement normal : uniquement les actives
        queryset = Maison.objects.filter(is_active=True)
        
        # Filtres de base
        type_maison = self.request.query_params.get('type')
        ville = self.request.query_params.get('ville')
        min_prix = self.request.query_params.get('min_prix')
        max_prix = self.request.query_params.get('max_prix')
        
        if type_maison:
            queryset = queryset.filter(type_maison=type_maison)
        if ville:
            queryset = queryset.filter(ville__icontains=ville)
        if min_prix:
            queryset = queryset.filter(prix__gte=min_prix)
        if max_prix:
            queryset = queryset.filter(prix__lte=max_prix)
        
        return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    # -------------------------------
    # Recherche avancée
    # -------------------------------
    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def recherche_avancee(self, request):
        serializer = RechercheMaisonSerializer(data=request.data)
        if serializer.is_valid():
            queryset = Maison.objects.filter(is_active=True)
            queryset = serializer.search(queryset)

            # Pagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer_result = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer_result.data)

            serializer_result = self.get_serializer(queryset, many=True)
            return Response(serializer_result.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =========================
# PARCELLES
# =========================
class ParcelleViewSet(PropertyActionMixin, viewsets.ModelViewSet):
    queryset = Parcelle.objects.filter(is_active=True)
    serializer_class = ParcelleSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre', 'description', 'ville', 'quartier', 'pays']
    ordering_fields = ['prix', 'date_creation', 'surface']
    ordering = ['-date_creation']

    def get_queryset(self):
        owner_id = self.request.query_params.get('owner')
        if owner_id:
            return Parcelle.objects.filter(owner_id=owner_id).order_by('-date_creation')
        return super().get_queryset()

    def get_serializer_context(self):
        return {"request": self.request}

# =========================
# HOTELS
# =========================
class HotelViewSet(PropertyActionMixin, viewsets.ModelViewSet):
    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre', 'description', 'ville', 'pays']
    ordering_fields = ['prix_nuit', 'note_moyenne', 'date_creation']
    ordering = ['-date_creation']

    def get_queryset(self):
        owner_id = self.request.query_params.get('owner')
        if owner_id:
            return Hotel.objects.filter(owner_id=owner_id).order_by('-date_creation')
        return super().get_queryset()

    def get_serializer_context(self):
        return {"request": self.request}

    # -------------------------------
    # Recherche hôtels par ville et catégorie
    # -------------------------------
    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def rechercher(self, request):
        ville = request.query_params.get('ville')
        categorie = request.query_params.get('categorie')
        min_note = request.query_params.get('min_note')
        max_prix = request.query_params.get('max_prix')

        queryset = self.get_queryset()
        
        if ville:
            queryset = queryset.filter(ville__icontains=ville)
        if categorie:
            queryset = queryset.filter(categorie=categorie)
        if min_note:
            queryset = queryset.filter(note_moyenne__gte=min_note)
        if max_prix:
            queryset = queryset.filter(prix_nuit__lte=max_prix)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# =========================
# RESIDENCES
# =========================
class ResidenceViewSet(PropertyActionMixin, viewsets.ModelViewSet):
    queryset = Residence.objects.filter(is_active=True)
    serializer_class = ResidenceSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'description', 'ville']
    
    def get_queryset(self):
        owner_id = self.request.query_params.get('owner')
        if owner_id:
            return Residence.objects.filter(owner_id=owner_id).order_by('-date_creation')
        return super().get_queryset()

    def get_serializer_context(self):
        return {"request": self.request}

# =========================
# PUBLICITES
# =========================
class PubliciteViewSet(viewsets.ModelViewSet):
    queryset = Publicite.objects.filter(is_active=True, date_fin__gte=timezone.now())
    serializer_class = PubliciteSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        type_pub = request.query_params.get('type', 'general')
        queryset = self.get_queryset().filter(type_pub=type_pub).order_by('ordre')
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], permission_classes=[AllowAny])
    def clic(self, request, pk=None):
        pub = self.get_object()
        pub.increment_clic()
        return Response({'message': 'Clic enregistré'})

# =========================
# PAYS
# =========================
def liste_pays(request):
    pays_list = list(Pays.objects.all().values('id', 'nom', 'code', 'drapeau', 'indicatif'))
    return JsonResponse(pays_list, safe=False)

def detect_country(request):
    code = request.GET.get('code')
    try:
        pays = Pays.objects.get(code=code.upper())
        return JsonResponse({
            'nom': pays.nom, 
            'code': pays.code, 
            'drapeau': pays.drapeau.url if pays.drapeau else None,
            'indicatif': pays.indicatif
        })
    except Pays.DoesNotExist:
        return JsonResponse({'error': 'Pays non trouvé'}, status=404)

# =========================
# CONTACT & DEMANDES
# =========================
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

class DemandeVisiteViewSet(viewsets.ModelViewSet):
    serializer_class = DemandeVisiteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DemandeVisite.objects.filter(user=self.request.user).order_by('-date_creation')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        # Notification au propriétaire
        bien_type = serializer.validated_data['bien_type']
        bien_id = serializer.validated_data['bien_id']
        
        # Ici vous devriez récupérer le propriétaire selon le type de bien
        # Pour simplifier, on crée une notification système
        Notification.objects.create(
            user=self.request.user,
            title="Demande de visite envoyée",
            body="Votre demande de visite a été envoyée avec succès",
            type="visite",
            data={"bien_type": bien_type, "bien_id": str(bien_id)}
        )

# =========================
# MESSAGES
# =========================
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        user = self.request.user
        autre_utilisateur = self.request.query_params.get('user')
        
        if autre_utilisateur:
            try:
                autre_user = User.objects.get(id=autre_utilisateur)
                return Message.objects.filter(
                    Q(sender=user, receiver=autre_user) | 
                    Q(sender=autre_user, receiver=user)
                ).order_by("created_at")
            except User.DoesNotExist:
                return Message.objects.none()
        
        return Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['GET'])
    def conversations(self, request):
        # Récupérer la liste des conversations (dernier message avec chaque utilisateur)
        user = request.user
        messages = Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver').order_by('-created_at')
        
        conversations = {}
        for msg in messages:
            other_user = msg.receiver if msg.sender == user else msg.sender
            if other_user.id not in conversations:
                conversations[other_user.id] = {
                    'user': {
                        'id': other_user.id,
                        'username': other_user.username,
                        'avatar': other_user.avatar.url if other_user.avatar else None
                    },
                    'last_message': MessageSerializer(msg).data,
                    'unread_count': Message.objects.filter(
                        sender=other_user, 
                        receiver=user, 
                        is_read=False
                    ).count()
                }
        
        return Response(list(conversations.values()))

    @action(detail=False, methods=['POST'])
    def mark_read(self, request):
        user_id = request.data.get('user_id')
        if user_id:
            Message.objects.filter(sender_id=user_id, receiver=request.user, is_read=False).update(is_read=True)
            return Response({'status': 'ok'})
        return Response({'error': 'missing user_id'}, status=400)

    @action(detail=True, methods=['POST'])
    def marquer_lu(self, request, pk=None):
        message = self.get_object()
        if message.receiver == request.user:
            message.is_read = True
            message.save()
            return Response({'status': 'marqué comme lu'})
        return Response({'error': 'Non autorisé'}, status=403)

# =========================
# NOTIFICATIONS
# =========================
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

    @action(detail=False, methods=['GET'])
    def non_lues(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'count': count})

    @action(detail=False, methods=['POST'])
    def tout_marquer_lu(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'toutes les notifications marquées comme lues'})

    @action(detail=True, methods=['POST', 'PATCH'])
    def marquer_lu(self, request, pk=None):
        notification = self.get_object()
        if notification.user == request.user:
            notification.is_read = True
            notification.save()
            return Response({'status': 'notification marquée lue'})
        return Response({'error': 'Non autorisé'}, status=403)

# =========================
# DASHBOARD & STATISTIQUES
# =========================
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.is_staff or user.is_superuser:
            # Dashboard admin
            aujourd_hui = timezone.now().date()
            debut_mois = aujourd_hui.replace(day=1)
            
            data = {
                'total_maisons': Maison.objects.filter(is_active=True).count(),
                'total_parcelles': Parcelle.objects.filter(is_active=True).count(),
                'total_hotels': Hotel.objects.filter(is_active=True).count(),
                'total_residences': Residence.objects.filter(is_active=True).count(),
                'total_users': User.objects.count(),
                'nouvelles_demandes': Contact.objects.filter(
                    is_traite=False, 
                    date_creation__date=aujourd_hui
                ).count(),
                'inscriptions_mois': User.objects.filter(
                    date_joined__gte=debut_mois
                ).count(),
                'top_villes': Maison.objects.filter(is_active=True)
                    .values('ville').annotate(count=Count('id'))
                    .order_by('-count')[:10]
            }
        else:
            # Dashboard utilisateur/propriétaire
            data = {
                'mes_maisons': Maison.objects.filter(owner=user, is_active=True).count(),
                'mes_parcelles': Parcelle.objects.filter(owner=user, is_active=True).count(),
                'mes_hotels': Hotel.objects.filter(owner=user, is_active=True).count(),
                'mes_residences': Residence.objects.filter(owner=user, is_active=True).count(),
                'messages_non_lus': Message.objects.filter(receiver=user, is_read=False).count(),
                'notifications_non_lues': Notification.objects.filter(user=user, is_read=False).count(),
                'favoris': Favori.objects.filter(user=user).count()
            }
        
        return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def statistiques_globales(request):
    """Statistiques globales accessibles à tous"""
    data = {
        'total_biens': Maison.objects.filter(is_active=True).count() + 
                      Parcelle.objects.filter(is_active=True).count() +
                      Hotel.objects.filter(is_active=True).count(),
        'villes_actives': Maison.objects.filter(is_active=True)
            .values('ville').annotate(count=Count('id'))
            .order_by('-count')[:5],
        'hotels_top': Hotel.objects.filter(is_active=True, note_moyenne__gte=4)
            .order_by('-note_moyenne')[:5],
        'maisons_populaires': Maison.objects.filter(is_active=True)
            .annotate(likes_count=Count('likes'))
            .order_by('-likes_count')[:5]
    }
    return Response(data)
# =========================
# RECHERCHE D'UTILISATEURS
# =========================
@api_view(['GET'])
@permission_classes([AllowAny])
def search_users(request):
    """
    Recherche d'utilisateurs par username, email ou téléphone
    Endpoint: /search-users/?q=jean
    """
    query = request.query_params.get('q', '')
    
    if not query:
        return Response([])
    
    # Recherche dans les 3 champs
    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(email__icontains=query) |
        Q(phone_number__icontains=query)
    )[:20]  # Limite à 20 résultats
    
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)
# =========================
# MEDIA DEBUG
# =========================
def photo_list_view(request):
    photos = list(Photo.objects.values())
    return JsonResponse(photos, safe=False)

def video_list_view(request):
    videos = list(Video.objects.values())
    return JsonResponse(videos, safe=False)

# =========================
# APP VERSIONING
# =========================
@api_view(['GET'])
@permission_classes([AllowAny])
def get_latest_version(request):
    """Récupère la dernière version de l'application disponible"""
    latest = AppVersion.objects.first()
    if latest:
        return Response(AppVersionSerializer(latest).data)
    return Response({"detail": "Aucune version trouvée"}, status=404)



from rest_framework import viewsets, permissions

class AlerteViewSet(viewsets.ModelViewSet):
    serializer_class = AlerteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # L'utilisateur ne voit que ses propres alertes
        return Alerte.objects.filter(user=self.request.user)

# =========================
# NOTIFICATIONS PUSH & APPELS
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_fcm_token(request):
    """Enregistre le token FCM du téléphone pour les notifications push"""
    fcm_token = request.data.get('fcm_token')
    if not fcm_token:
        return Response({'error': 'Token requis'}, status=400)

    user = request.user
    user.fcm_token = fcm_token
    user.save(update_fields=['fcm_token'])
    return Response({'status': 'token enregistré'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_call(request):
    """Prévient le destinataire qu'un appel arrive via Firebase"""
    receiver_id = request.data.get('receiver_id')
    channel_name = request.data.get('channel_name')
    is_video = request.data.get('is_video', True)

    if not receiver_id or not channel_name:
        return Response({'error': 'Paramètres manquants'}, status=400)

    try:
        receiver = User.objects.get(id=receiver_id)
        if not receiver.fcm_token:
             return Response({'error': 'Destinataire non disponible (pas de token)'}, status=404)

        # Préparation du message Data (silencieux pour déclencher l'UI d'appel)
        message = messaging.Message(
            data={
                'type': 'call',
                'channelName': str(channel_name),
                'callerName': str(request.user.username),
                'callerAvatar': request.user.avatar.url if request.user.avatar else '',
                'isVideo': str(is_video).lower(),
                'callerId': str(request.user.id)
            },
            token=receiver.fcm_token,
        )

        response = messaging.send(message)
        return Response({'status': 'appel envoyé', 'message_id': response})

    except User.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=404)
    except Exception as e:
        logger.error(f"Erreur FCM: {traceback.format_exc()}")
        return Response({'error': str(e)}, status=500)
