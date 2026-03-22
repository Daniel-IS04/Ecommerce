import jwt
import secrets
from django.utils import timezone  # Importación correcta en Django
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTService:
    @staticmethod
    def generate_token(user):
        # Usar timezone.now() garantiza un datetime "aware" compatible con UTC
        now = timezone.now()
        payload = {
            "user_id": user.id,
            "email": user.email,
            "exp": int(
                (now + timedelta(minutes=7)).timestamp()
            ),  # JWT exp espera un timestamp entero Unix
            "iat": int(now.timestamp()),  # Issued at: Buena práctica de seguridad
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def generate_refresh_token():
        return secrets.token_hex(32)
