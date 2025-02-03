from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from maison.views import *
from rest_framework.routers import DefaultRouter

# Configuration du routeur pour les publicités
router = DefaultRouter()
router.register(r'publicites', PubliciteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    # Routes pour les maisons
    path('maisons/', MaisonListView.as_view(), name='maison-list'),
    
    # Routes pour les parcelles
    path('parcelles/', ParcelleList.as_view(), name='parcelle-list'),
    path('parcelles/<int:pk>/', ParcelleDetail.as_view(), name='parcelle-detail'),

    # Routes pour les hôtels
    path('hotels/', HotelList.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', HotelDetail.as_view(), name='hotel-detail'),
   
    # Routes pour les photos et vidéos
    path('photos/', photo_list_view, name='photo-list'),  # Nouvelle route pour les photos
    path('videos/', video_list_view, name='video-list'),  # Nouvelle route pour les vidéos
    path('liste_pays/', liste_pays, name='liste_pays'),
    path('publicites/', PubliciteViewSet.as_view({'get': 'list', 'post': 'create'}), name='publicite_list'),  # Liste et création de publicités
    path('parcelle-photos/', ParcellePhotoList.as_view(), name='parcelle_photo_list'),  # Liste et création de photos de parcelles
    path('hotel-photos/', HotelPhotoList.as_view(), name='hotel_photo_list'),  # Liste et création de photos d'hôtels
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]
# Configuration pour servir les fichiers médias en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)