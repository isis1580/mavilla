from django import forms
from .models import (
    Maison, Photo, Video,
    Parcelle, ParcellePhoto,
    Publicite,
    Hotel, HotelPhoto,
    Pays
)

# =========================
# MAISONS
# =========================
class MaisonForm(forms.ModelForm):
    class Meta:
        model = Maison
        fields = [
            'type_maison', 'description', 'prix',
            'nombre_chambres', 'nombre_salles_de_bain',
            'nombre_salon', 'nombre_cuisines',
            'surface', 'piscine',
            'quartier', 'ville', 'pays'
        ]

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['photos']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video']

# =========================
# PARCELLES
# =========================
class ParcelleForm(forms.ModelForm):
    class Meta:
        model = Parcelle
        fields = ['description', 'prix', 'surface', 'quartier']

class ParcellePhotoForm(forms.ModelForm):
    class Meta:
        model = ParcellePhoto
        fields = ['photos']

# =========================
# PUBLICITES
# =========================
class PubliciteForm(forms.ModelForm):
    class Meta:
        model = Publicite
        fields = ['titre', 'photos', 'lien']

# =========================
# HOTELS
# =========================
class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['titre', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class HotelPhotoForm(forms.ModelForm):
    class Meta:
        model = HotelPhoto
        fields = ['photos']

# =========================
# PAYS
# =========================
class PaysForm(forms.ModelForm):
    class Meta:
        model = Pays
        fields = ['nom', 'code', 'drapeau']
