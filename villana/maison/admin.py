from django.contrib import admin
from .models import *

# Inline for managing photos in Maison admin interface
class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1  # Allows adding one more photo at a time

# Inline for managing photos in Parcelle admin interface
class ParcellePhotoInline(admin.TabularInline):
    model = ParcellePhoto
    extra = 1  # Allows adding one more photo at a time

# Inline for managing photos in Hotel admin interface
class HotelPhotoInline(admin.TabularInline):
    model = HotelPhoto
    extra = 1  # Allows adding one more photo at a time

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1  # Permet d'ajouter une vidéo supplémentaire

# Personnalisation de l'admin de Maison pour inclure l'inline Photo et Video
class MaisonAdmin(admin.ModelAdmin):
    list_display = ('type_maison', 'description', 'prix', 'nombre_chambres', 'nombre_salles_de_bain', 'ville')
    inlines = [PhotoInline, VideoInline]  # Ajoutez l'inline pour les vidéos ici

# Parcelle admin customization to include the ParcellePhoto inline
class ParcelleAdmin(admin.ModelAdmin):
    list_display = ('description', 'prix', 'surface', 'quartier', 'date_creation')
    inlines = [ParcellePhotoInline]  # Add the inline models here

# Hotel admin customization to include the HotelPhoto inline
class HotelAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description', 'date_creation')
    inlines = [HotelPhotoInline]  # Add the inline models here
# Registering the models with the admin panel

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'is_active', 'is_staff')

class UserAdmin(admin.ModelAdmin):
    form = CustomUserCreationForm
    list_display = ('username', 'phone_number', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'phone_number', 'email')

admin.site.register(User, UserAdmin)


admin.site.register(Maison, MaisonAdmin)
admin.site.register(Publicite)
admin.site.register(Pays)
admin.site.register(Parcelle, ParcelleAdmin)
admin.site.register(Hotel, HotelAdmin)

