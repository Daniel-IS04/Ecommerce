from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

# Importaciones de SimpleJWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Tus Serializers
from ..serializers.auth_serializers import (
    RegisterSerializer,
    MyTokenObtainPairSerializer,
)


class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    "errors": serializer.errors,
                    "messages": "No se pudo registrar el usuario por errores de validación.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """
    Sustituye a tu antigua LoginView.
    Usa el serializer personalizado para meter datos en el payload.
    """

    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = serializer.user
        tokens = serializer.validated_data

        response_data = {
            "user": {
                "first_name": user.first_name,
                "email": user.email,
                "role": getattr(user, "role", "user"),
            },
            "success": True,
            "token": tokens["access"],  # Access Token para localStorage
        }

        response = Response(response_data, status=status.HTTP_200_OK)

        # Seteamos el Refresh Token en la Cookie HttpOnly
        # El max_age debería coincidir con tu REFRESH_TOKEN_LIFETIME de settings
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh"],
            httponly=True,
            secure=False,  # Cambiar a True en producción (HTTPS)
            samesite="Lax",
            max_age=24 * 60 * 60,  # 1 día
            path="/api/auth/refresh/",  # Seguridad: solo se envía a la ruta de refresh
        )

        return response


# Ya no necesitas implementar la lógica manual.
# Solo heredas y SimpleJWT lee la cookie (si configuraste AUTH_COOKIE en settings)
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    # Si en settings configuraste AUTH_COOKIE, esta vista buscará el refresh ahí automáticamente.
