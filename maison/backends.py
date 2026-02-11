from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User

class MultiFieldAuthenticationBackend(ModelBackend):
    """
    Authentification avec username, email ou phone_number
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        # Chercher l'utilisateur par username, email ou phone_number
        try:
            user = User.objects.get(
                Q(username=username) | 
                Q(email=username) | 
                Q(phone_number=username)
            )
        except User.DoesNotExist:
            User().set_password(password)  # Pour éviter les attaques par timing
            return None
        except User.MultipleObjectsReturned:
            # En cas de doublon, priorité: phone_number > email > username
            user = User.objects.filter(phone_number=username).first()
            if not user:
                user = User.objects.filter(email=username).first()
            if not user:
                user = User.objects.filter(username=username).first()
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None