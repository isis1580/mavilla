from django.contrib.auth.backends import BaseBackend
from maison.models import User
from django.db import models

class MultiFieldAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.filter(
                models.Q(username=username) |
                models.Q(phone_number=username) |
                models.Q(email=username)
            ).first()

            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
