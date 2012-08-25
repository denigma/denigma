from django.conf import settings

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class AuthenticationBackend(ModelBackend):
    
    def authenticate(self, **credentials):
        lookup_params = {}
        if settings.ACCOUNT_EMAIL_AUTHENTICATION:
            field, identity = "email__iexact", credentials.get("email")
        else:
            field, identity = "username__iexact", credentials.get("username")
        if identity is None:
            return None
        lookup_params[field] = identity
        try:
            user = User.objects.get(**lookup_params)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(credentials["password"]):
                return user


EmailModelBackend = AuthenticationBackend