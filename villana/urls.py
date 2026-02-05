from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from maison.views import *

router = DefaultRouter()
router.register(r'maisons', MaisonViewSet, basename='maison')
router.register(r'parcelles', ParcelleViewSet, basename='parcelle')
router.register(r'parcelle-photos', ParcellePhotoViewSet, basename='parcellephoto')
router.register(r'hotels', HotelViewSet, basename='hotel')
router.register(r'hotel-photos', HotelPhotoViewSet, basename='hotelphoto')
router.register(r'publicites', PubliciteViewSet, basename='publicite')
router.register("messages", MessageViewSet)
router.register("notifications", NotificationViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # Auth
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),

    # Pays
    path('liste_pays/', liste_pays, name='liste-pays'),
    path('detect_country/', detect_country, name='detect-country'),

    # Media debug
    path('photos/', photo_list_view, name='photo-list'),
    path('videos/', video_list_view, name='video-list'),

    # DRF router
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
