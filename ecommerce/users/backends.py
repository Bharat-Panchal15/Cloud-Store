from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger('ecommerce.users.auth_backend')

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if password is None:
            logger.debug("Authentication failed: no password provided")
            return None

        try:
            if email:
                user = User.objects.get(email=email)
            elif username:
                user = User.objects.get(username=username)
            else:
                logger.debug("Authentication failed: no username or email provided")
                return None
            
        except User.DoesNotExist:
            logger.debug("Authentication failed: user does not exist")
            return None

        if user.check_password(password):
            logger.debug("Authentication successful", extra={'user_id': user.id})
            return user
        logger.debug("Authentication failed: incorrect password", extra={'user_id': user.id})
        return None
