from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
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
router.register(r'visites', DemandeVisiteViewSet, basename='visite') # Alias pour Flutter
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'evaluations', AppReviewViewSet, basename='evaluation')
router.register(r'mediations', MediationViewSet, basename='mediation')
router.register(r'professionals', ProfessionalRequestViewSet, basename='professional')
router.register(r'support', SupportTicketViewSet, basename='support')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'alertes', AlerteViewSet, basename='alerte')

urlpatterns = [
    # ✅ Redirection /admin → /admin/
    path('admin', RedirectView.as_view(url='/admin/', permanent=True)),
    
    # ✅ ADMIN
    path('admin/', admin_site.urls),
    path('django-admin/', admin.site.urls),
    
    # ✅ API
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/search-users/', search_users, name='search-users'),
    path('api/liste_pays/', liste_pays, name='liste-pays'),
    path('api/detect_country/', detect_country, name='detect-country'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/statistiques-globales/', statistiques_globales, name='statistiques-globales'),
    path('api/app-version/latest/', get_latest_version, name='latest-version'),
    path('api/register-fcm/', register_fcm_token, name='register-fcm'),
    path('api/initiate-call/', initiate_call, name='initiate-call'),
    path('api/', include(router.urls)),
    
    # ✅ FRONTEND
    path('', FrontendAppView.as_view(), name='home'),
    
    # ✅ CATCH-ALL - UNIQUEMENT POUR LE FRONTEND
    # Exclure admin, static, media, api
    re_path(r'^(?!(admin|static|media|api)/).*$', FrontendAppView.as_view()),
]