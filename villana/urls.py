from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from maison.views import *
from maison.admin import admin_site
from frontend.views import FrontendAppView

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
    # Admin
    path('admin/', admin_site.urls),
    path('django-admin/', admin.site.urls),
    
    # Authentification et endpoints spécifiques (Prioritaires sur le router)
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path('api/search-users/', search_users, name='search-users'),
    path('api/liste_pays/', liste_pays, name='liste-pays'),
    path('api/detect_country/', detect_country, name='detect-country'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/statistiques-globales/', statistiques_globales, name='statistiques-globales'),

    # API via Router
    path('api/', include(router.urls)),

    # Frontend React - La page d'accueil doit être ICI
    path('', FrontendAppView.as_view(), name='home'),

    # Catch-all pour React (doit être en DERNIER)
    # Cela permet à React Router de gérer les URLs comme /login, /hotels, etc.
    re_path(r'^.*$', FrontendAppView.as_view()),
]
