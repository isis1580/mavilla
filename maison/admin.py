from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from django.utils import timezone

from .models import *

# =========================
# Inlines
# =========================
class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.photos:
            return format_html('<img src="{}" width="100" height="100" />', obj.photos.url)
        return "Pas d'image"
    preview.short_description = "Aperçu"

class ParcellePhotoInline(admin.TabularInline):
    model = ParcellePhoto
    extra = 1
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.photos:
            return format_html('<img src="{}" width="100" height="100" />', obj.photos.url)
        return "Pas d'image"
    preview.short_description = "Aperçu"

class HotelPhotoInline(admin.TabularInline):
    model = HotelPhoto
    extra = 1
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.photos:
            return format_html('<img src="{}" width="100" height="100" />', obj.photos.url)
        return "Pas d'image"
    preview.short_description = "Aperçu"

class ResidencePhotoInline(admin.TabularInline):
    model = ResidencePhoto
    extra = 1
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.photos:
            return format_html('<img src="{}" width="100" height="100" />', obj.photos.url)
        return "Pas d'image"
    preview.short_description = "Aperçu"

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

class CommentaireInline(admin.TabularInline):
    model = Commentaire
    extra = 0
    readonly_fields = ['user', 'date_creation']
    can_delete = True

class HotelNoteInline(admin.TabularInline):
    model = HotelNote
    extra = 0
    readonly_fields = ['user', 'date_creation']

# =========================
# Filters
# =========================
class VilleListFilter(admin.SimpleListFilter):
    title = 'ville'
    parameter_name = 'ville'

    def lookups(self, request, model_admin):
        villes = Maison.objects.values_list('ville', flat=True).distinct()
        return [(ville, ville) for ville in villes]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ville=self.value())
        return queryset

# =========================
# Admin pour Maison
# =========================
class MaisonAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_maison', 'categorie', 'prix', 'ville', 'quartier', 
                   'nombre_chambres', 'is_active', 'vue_count', 'date_creation')
    list_filter = ('type_maison', 'categorie', 'ville', 'is_active', 'date_creation', VilleListFilter)
    search_fields = ('titre', 'description', 'ville', 'quartier', 'pays')
    readonly_fields = ('vue_count', 'date_creation', 'date_modification')
    inlines = [PhotoInline, VideoInline, CommentaireInline]
    list_per_page = 20
    fieldsets = (
        ('Informations générales', {
            'fields': ('owner', 'titre', 'type_maison', 'categorie', 'description')
        }),
        ('Caractéristiques', {
            'fields': ('prix', 'prix_promotion', 'nombre_chambres', 'nombre_salles_de_bain', 
                      'nombre_salon', 'nombre_cuisines', 'surface', 'piscine', 'jardin', 'garage')
        }),
        ('Localisation', {
            'fields': ('quartier', 'ville', 'pays', 'latitude', 'longitude', 'adresse_complete')
        }),
        ('Statut', {
            'fields': ('is_active', 'is_premium', 'vue_count', 'date_creation', 'date_modification')
        }),
    )
    actions = ['activer_maisons', 'desactiver_maisons', 'marquer_premium']

    def activer_maisons(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} maisons activées.")
    activer_maisons.short_description = "Activer les maisons sélectionnées"

    def desactiver_maisons(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} maisons désactivées.")
    desactiver_maisons.short_description = "Désactiver les maisons sélectionnées"

    def marquer_premium(self, request, queryset):
        queryset.update(is_premium=True)
        self.message_user(request, f"{queryset.count()} maisons marquées comme premium.")
    marquer_premium.short_description = "Marquer comme premium"

# =========================
# Admin pour Parcelle
# =========================
class ParcelleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_parcelle', 'prix', 'surface', 'ville', 'quartier', 
                   'is_active', 'date_creation')
    list_filter = ('type_parcelle', 'ville', 'is_active')
    search_fields = ('titre', 'description', 'ville', 'quartier')
    readonly_fields = ('date_creation', 'date_modification')
    inlines = [ParcellePhotoInline]

# =========================
# Admin pour Hôtel
# =========================
class HotelAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_hotel', 'categorie_stars', 'prix_nuit', 'ville', 
                   'note_moyenne', 'chambres_disponibles', 'is_active')
    list_filter = ('type_hotel', 'categorie', 'ville', 'is_active')
    search_fields = ('titre', 'description', 'ville', 'pays')
    readonly_fields = ('note_moyenne', 'date_creation')
    inlines = [HotelPhotoInline, HotelNoteInline]
    
    def categorie_stars(self, obj):
        return '★' * obj.categorie
    categorie_stars.short_description = 'Catégorie'

# =========================
# Admin pour Résidence
# =========================
class ResidenceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_residence', 'owner', 'nombre_appartements', 
                   'ville', 'pays', 'is_active', 'date_creation')
    list_filter = ('type_residence', 'is_active')
    search_fields = ('nom', 'description', 'ville', 'pays')
    readonly_fields = ('date_creation',)
    inlines = [ResidencePhotoInline]

# =========================
# Admin pour User personnalisé
# =========================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'is_active', 
                 'is_staff', 'is_proprietaire', 'is_verified')

class UserAdmin(admin.ModelAdmin):
    form = CustomUserCreationForm
    list_display = ('username', 'phone_number', 'email', 'is_proprietaire', 
                   'is_verified', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_proprietaire', 'is_verified', 'is_active', 'is_staff')
    search_fields = ('username', 'phone_number', 'email')
    readonly_fields = ('date_joined',)
    fieldsets = (
        ('Informations de base', {
            'fields': ('username', 'phone_number', 'email', 'avatar')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 
                      'is_proprietaire', 'is_verified')
        }),
        ('Dates', {
            'fields': ('date_joined', 'last_login')
        }),
    )
    actions = ['verifier_utilisateurs', 'rendre_proprietaires']

    def verifier_utilisateurs(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} utilisateurs vérifiés.")
    verifier_utilisateurs.short_description = "Vérifier les utilisateurs sélectionnés"

    def rendre_proprietaires(self, request, queryset):
        queryset.update(is_proprietaire=True)
        self.message_user(request, f"{queryset.count()} utilisateurs marqués comme propriétaires.")
    rendre_proprietaires.short_description = "Rendre propriétaires"

# =========================
# Admin pour Commentaire
# =========================
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('user', 'maison', 'note', 'texte_preview', 'is_approved', 'date_creation')
    list_filter = ('is_approved', 'date_creation')
    search_fields = ('texte', 'user__username', 'maison__titre')
    list_editable = ('is_approved',)
    actions = ['approuver_commentaires', 'desapprouver_commentaires']

    def texte_preview(self, obj):
        return obj.texte[:50] + '...' if len(obj.texte) > 50 else obj.texte
    texte_preview.short_description = 'Texte'

    def approuver_commentaires(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} commentaires approuvés.")
    approuver_commentaires.short_description = "Approuver les commentaires"

    def desapprouver_commentaires(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} commentaires désapprouvés.")
    desapprouver_commentaires.short_description = "Désapprouver les commentaires"

# =========================
# Admin pour Publicité
# =========================
class PubliciteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_pub', 'is_active', 'date_debut', 'date_fin', 
                   'clic_count', 'ordre')
    list_filter = ('type_pub', 'is_active')
    list_editable = ('ordre', 'is_active')
    search_fields = ('titre', 'description')
    readonly_fields = ('clic_count',)

# =========================
# Admin pour Contact
# =========================
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'type_contact', 'sujet', 
                   'is_traite', 'date_creation')
    list_filter = ('type_contact', 'is_traite', 'date_creation')
    search_fields = ('nom', 'email', 'sujet', 'message')
    readonly_fields = ('date_creation',)
    list_editable = ('is_traite',)
    actions = ['marquer_traites']

    def marquer_traites(self, request, queryset):
        queryset.update(is_traite=True)
        self.message_user(request, f"{queryset.count()} contacts marqués comme traités.")
    marquer_traites.short_description = "Marquer comme traité"

# =========================
# Admin pour Notification
# =========================
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title_preview', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('title', 'body', 'user__username')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)
    actions = ['marquer_comme_lu']

    def title_preview(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_preview.short_description = 'Titre'

    def marquer_comme_lu(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} notifications marquées comme lues.")
    marquer_comme_lu.short_description = "Marquer comme lu"

# =========================
# Admin pour Message
# =========================
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'text_preview', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('text', 'sender__username', 'receiver__username')
    readonly_fields = ('created_at',)

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Message'

# =========================
# Admin pour Pays
# =========================
class PaysAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'indicatif', 'drapeau_preview')
    search_fields = ('nom', 'code', 'indicatif')

    def drapeau_preview(self, obj):
        if obj.drapeau:
            return format_html('<img src="{}" width="30" height="20" />', obj.drapeau.url)
        return "Pas de drapeau"
    drapeau_preview.short_description = 'Drapeau'

# =========================
# Dashboard Admin Personnalisé
# =========================
class VillanaAdminSite(admin.AdminSite):
    site_header = "Administration Villana"
    site_title = "Villana Admin"
    index_title = "Tableau de bord"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Statistiques pour le dashboard
        aujourd_hui = timezone.now().date()
        
        stats = {
            'total_maisons': Maison.objects.count(),
            'maisons_actives': Maison.objects.filter(is_active=True).count(),
            'total_utilisateurs': User.objects.count(),
            'nouveaux_utilisateurs': User.objects.filter(date_joined__date=aujourd_hui).count(),
            'demandes_contact': Contact.objects.filter(is_traite=False).count(),
            'commentaires_attente': Commentaire.objects.filter(is_approved=False).count(),
            'dernieres_maisons': Maison.objects.order_by('-date_creation')[:5],
        }
        
        extra_context['stats'] = stats
        return super().index(request, extra_context)

# =========================
# Enregistrement des modèles
# =========================
admin_site = VillanaAdminSite(name='villana_admin')

admin_site.register(User, UserAdmin)
admin_site.register(Maison, MaisonAdmin)
admin_site.register(Publicite, PubliciteAdmin)
admin_site.register(Pays, PaysAdmin)
admin_site.register(Parcelle, ParcelleAdmin)
admin_site.register(Hotel, HotelAdmin)
admin_site.register(Residence, ResidenceAdmin)
admin_site.register(Commentaire, CommentaireAdmin)
admin_site.register(Contact, ContactAdmin)
admin_site.register(Notification, NotificationAdmin)
admin_site.register(Message, MessageAdmin)
admin_site.register(Favori)
admin_site.register(Like)
admin_site.register(HotelNote)
admin_site.register(DemandeVisite)
admin_site.register(Statistique)

# Pour garder la compatibilité avec l'admin Django par défaut
admin.site.register(User, UserAdmin)
admin.site.register(Maison, MaisonAdmin)
admin.site.register(Publicite, PubliciteAdmin)
admin.site.register(Pays, PaysAdmin)
admin.site.register(Parcelle, ParcelleAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Residence, ResidenceAdmin)
admin.site.register(Commentaire, CommentaireAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Favori)
admin.site.register(Like)
admin.site.register(HotelNote)
admin.site.register(DemandeVisite)
admin.site.register(Statistique)