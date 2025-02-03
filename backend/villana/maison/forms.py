from django import forms
from .models import *


class MaisonForm(forms.ModelForm):
    class Meta:
        model = Maison
        fields = ['type_maison', 'description', 'prix', 'nombre_chambres', 
                  'nombre_salles_de_bain', 'nombre_salon', 'nombre_cuisines', 
                  'surface', 'piscine', 'quartier', 'ville', 'pays']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['photos']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video']

class ParcelleForm(forms.ModelForm):
    class Meta:
        model = Parcelle
        fields = ['description', 'prix', 'surface', 'quartier']


class PubliciteForm(forms.ModelForm):
    class Meta:
        model = Publicite
        fields = ['titre', 'photos', 'lien']


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'  # Inclut tous les champs du modèle Hotel
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'prix': forms.NumberInput(attrs={'step': '0.01'}),
            'surface': forms.NumberInput(attrs={'step': '0.01'}),
        }


class ParcellePhotoForm(forms.ModelForm):
    class Meta:
        model = ParcellePhoto
        fields = ['photos']

class HotelPhotoForm(forms.ModelForm):
    class Meta:
        model = HotelPhoto
        fields = ['photos']
