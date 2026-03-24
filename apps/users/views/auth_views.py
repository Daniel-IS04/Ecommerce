from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

# Importaciones de SimpleJWT
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken as SimpleJWTRefreshToken
from django.conf import settings

# Tus Serializers y Modelos
from ..serializers.auth_serializers import (
    RegisterSerializer,
    MyTokenObtainPairSerializer,
)
from ..models.refresh_token import RefreshToken


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


class LoginView(GenericAPIView):
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
        lifetime = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]

        # NUEVO: Reemplazo. Eliminamos cualquier sesión/token anterior de este usuario
        RefreshToken.objects.filter(user=user).delete()

        # 1. Guardar el NUEVO Refresh Token en tu tabla
        RefreshToken.objects.create(
            user=user, token=tokens["refresh"], expires_at=timezone.now() + lifetime
        )

        response_data = {
            "user": {
                "first_name": user.first_name,
                "email": user.email,
                "role": getattr(user, "role", "user"),
            },
            "success": True,
            "token": tokens["access"],  # El frontend guarda esto en memoria
        }

        response = Response(response_data, status=status.HTTP_200_OK)

        # 2. Seteamos la Cookie HttpOnly
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh"],
            httponly=True,
            secure=settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE", False),
            samesite=settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE", "Lax"),
            max_age=int(lifetime.total_seconds()),
            path="/",
        )
        return response


class CustomTokenRefreshView(APIView):
    """
    Vista estática: Lee la cookie, valida en BD. Si venció, lo ELIMINA.
    Si está vivo, devuelve un nuevo access token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        cookie_token = request.COOKIES.get("refresh_token")
        if not cookie_token:
            return Response(
                {"error": "No se proporcionó refresh token en las cookies."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            db_token = RefreshToken.objects.get(token=cookie_token)

            # 1. Verificamos si el tiempo de BD ya venció
            if not db_token.is_valid():
                db_token.delete()  # <--- ELIMINACIÓN FÍSICA
                return Response(
                    {"error": "Token expirado. Se ha eliminado de la base de datos."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # 2. Validar criptográficamente el token original
            try:
                valid_refresh_token = SimpleJWTRefreshToken(cookie_token)
            except TokenError:
                # Si la firma del JWT falló o venció internamente, también lo borramos
                db_token.delete()  # <--- ELIMINACIÓN FÍSICA
                return Response(
                    {
                        "error": "Firma del token inválida o expirada criptográficamente. Se eliminó."
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # 3. Generar SOLO el nuevo Access Token
            new_access_token = str(valid_refresh_token.access_token)

            return Response({"token": new_access_token}, status=status.HTTP_200_OK)

        except RefreshToken.DoesNotExist:
            return Response(
                {"error": "Token no encontrado en los registros."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    """
    Elimina físicamente el token de la BD y destruye la cookie.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        cookie_token = request.COOKIES.get("refresh_token")

        if cookie_token:
            try:
                # Buscar y ELIMINAR FÍSICAMENTE de la base de datos
                db_token = RefreshToken.objects.get(token=cookie_token)
                db_token.delete()  # <--- ELIMINACIÓN FÍSICA AL SALIR
            except RefreshToken.DoesNotExist:
                pass

        response = Response(
            {"success": True, "message": "Sesión cerrada correctamente."},
            status=status.HTTP_200_OK,
        )

        # Eliminar la cookie enviando una fecha de expiración en el pasado
        response.delete_cookie("refresh_token", path="/")

        return response
