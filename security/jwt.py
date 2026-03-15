import jwt
import secrets
from datetime import datetime, timedelta
from django.conf import settings 
from django.contrib.auth.models import AbstractBaseUser # para obtener el user def en settings.py

class JWTService:
    @staticmethod
    def generate_token(user: AbstractBaseUser):
        payload: dict[str, str | int | datetime] = {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }
        token: str =jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def generate_refresh_token():
        return secrets.token_hex(32)
        

    
