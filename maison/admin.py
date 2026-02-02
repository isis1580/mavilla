from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *

# =========================
# Inlines pour les photos et vidéos
# =========================
class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

class ParcellePhotoInline(admin.TabularInline):
    model = ParcellePhoto
    extra = 1

class HotelPhotoInline(admin.TabularInline):
    model = HotelPhoto
    extra = 1

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

# =========================
# Admin pour Maison
# =========================
class MaisonAdmin(admin.ModelAdmin):
    list_display = ('type_maison', 'description', 'prix', 'nombre_chambres', 'nombre_salles_de_bain', 'ville')
    inlines = [PhotoInline, VideoInline]

# =========================
# Admin pour Parcelle
# =========================
class ParcelleAdmin(admin.ModelAdmin):
    list_display = ('description', 'prix', 'surface', 'quartier', 'date_creation')
    inlines = [ParcellePhotoInline]

# =========================
# Admin pour Hôtel
# =========================
class HotelAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description', 'date_creation')
    inlines = [HotelPhotoInline]

# =========================
# Admin pour User personnalisé
# =========================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'is_active', 'is_staff')

class UserAdmin(admin.ModelAdmin):
    form = CustomUserCreationForm
    list_display = ('username', 'phone_number', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'phone_number', 'email')

# =========================
# Enregistrement des modèles
# =========================
admin.site.register(User, UserAdmin)
admin.site.register(Maison, MaisonAdmin)
admin.site.register(Publicite)
admin.site.register(Pays)
admin.site.register(Parcelle, ParcelleAdmin)
admin.site.register(Hotel, HotelAdmin)
