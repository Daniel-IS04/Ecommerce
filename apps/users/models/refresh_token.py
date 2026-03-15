from django.db import models
from django.conf import settings # pasar las Variables de entorno en settings.py
from datetime import datetime,timedelta

from rest_framework_simplejwt.tokens import Token

class RefreshToken (models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="refresh_Tokens"
    )
    token = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_revoked = models.BooleanField(default=False)

    def is_valid(self):
        return not self.is_revoked and datetime.utcnow() > self.expires_at

    def __str__(self):
        return f"Refresh Token for {self.user.email}"

