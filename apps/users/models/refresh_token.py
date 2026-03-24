from django.db import models
from django.conf import settings
from django.utils import timezone


class RefreshToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="refresh_tokens",
    )
    token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    # is_revoked eliminado completamente de acuerdo a tu lógica de eliminación física.

    def is_valid(self):
        # Ahora solo evaluamos que el tiempo actual sea menor al de expiración
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"Refresh Token for {self.user.email}"
