from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Le numéro de téléphone est requis')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)  # Hash le mot de passe pour la sécurité
        user.save(using=self._db)  # Sauvegarde l'utilisateur dans la base de données
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True)  # Le numéro de téléphone est unique
    is_active = models.BooleanField(default=True)  # Permet de désactiver un compte si besoin
    is_staff = models.BooleanField(default=False)  # Indique si l'utilisateur a des privilèges d'administrateur

    USERNAME_FIELD = 'phone_number'  # On utilise le numéro de téléphone comme identifiant
    REQUIRED_FIELDS = []  # Aucun autre champ n'est requis pour créer un utilisateur

    objects = CustomUserManager()  # On associe le gestionnaire personnalisé

    def __str__(self):
        return self.phone_number
