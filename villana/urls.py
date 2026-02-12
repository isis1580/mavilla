from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from maison.views import *
from maison.admin import admin_site

router = DefaultRouter()
router.register(r'maisons', MaisonViewSet, basename='maison')
router.register(r'parcelles', ParcelleViewSet, basename='parcelle')
router.register(r'hotels', HotelViewSet, basename='hotel')
router.register(r'residences', ResidenceViewSet, basename='residence')
router.register(r'publicites', PubliciteViewSet, basename='publicite')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'demandes-visite', DemandeVisiteViewSet, basename='demandevisite')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # Admin - PRIORITAIRE
    path('admin/', admin_site.urls),
    path('django-admin/', admin.site.urls),
    
    # Home
    path('', home, name='home'),

    # Auth et endpoints spécifiques - AVANT le router
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('search-users/', search_users, name='search-users'),

    # Pays
    path('liste_pays/', liste_pays, name='liste-pays'),
    path('detect_country/', detect_country, name='detect-country'),

    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('statistiques-globales/', statistiques_globales, name='statistiques-globales'),

    # Media debug
    path('photos/', photo_list_view, name='photo-list'),
    path('videos/', video_list_view, name='video-list'),

    # DRF auth
    path('api-auth/', include('rest_framework.urls')),
    
    # 🔥 ROUTER À LA FIN - Capture tout ce qui n'est pas capturé avant
    path('', include(router.urls)),
]