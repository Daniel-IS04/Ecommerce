from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.auth_serializers import RegisterSerializer, LoginSerializer
from ..serializers.user_serializers import UserSerializer
from drf_spectacular.utils import extend_schema
from security.jwt import JWTService
from datetime import datetime, timedelta
from ..models.refresh_token import RefreshToken
from rest_framework.permissions import AllowAny


class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    # LIB -> establecemos una instancia del serializer
    serializer_class = RegisterSerializer

    def post(self, request):
        #                     LIB
        serializer = self.get_serializer(data=request.data)
        # serializer ya me devuelve un JSON y validado
        if not serializer.is_valid(raise_exception=True):
            # Response(data=None, status=None, headers=None, content_type=None)
            return Response(
                data={
                    "errors": serializer.errors,
                    "messages": "No pudo registrar correctamente",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()  # guardamos

        return Response(  # devolvemos la respeusta
            RegisterSerializer(user).data, status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer, responses=LoginSerializer)
    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        access_token = JWTService.generate_token(user)
        refresh_token = JWTService.generate_refresh_token()

        expires = datetime.utcnow() + timedelta(days=7)
        RefreshToken.objects.create(user=user, token=refresh_token, expires_at=expires)

        user_return = UserSerializer(user).data
        response = Response(
            {"name": user_return, "success": True, "token": access_token},
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,  # Impide que JS lea la cookie (Seguridad extra)
            secure=True,  # Ponlo en False si estás probando en localhost sin HTTPS
            samesite="Lax",  # Protege contra ataques CSRF
            max_age=7 * 24 * 60 * 60,  # Tiempo de vida en segundos (7 días)
        )
        return response


# esto me dio flojera hacer ...xd
class TokenRefreshView(APIView):
    def post(self, request):
        # Leemos la cookie que el navegador envía automáticamente
        refresh_token_str = request.COOKIES.get("refresh_token")

        if not refresh_token_str:
            return Response(
                {"error": "No se encontró el refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            # Buscamos el token en la base de datos
            token_obj = RefreshToken.objects.get(token=refresh_token_str)

            if not token_obj.is_valid():
                return Response(
                    {"error": "Token expirado o revocado"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Todo está bien, le damos un nuevo access token de 15 minutos
            new_access_token = JWTService.generate_token(token_obj.user)

            return Response(
                {"success": True, "token": new_access_token}, status=status.HTTP_200_OK
            )

        except RefreshToken.DoesNotExist:
            return Response(
                {"error": "Token inválido"}, status=status.HTTP_401_UNAUTHORIZED
            )
