from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.auth_serializers import RegisterSerializer, LoginSerializer
from ..serializers.user_serializers import UserSerializer
from drf_spectacular.utils import extend_schema
from security.jwt import JWTService

class RegisterView(GenericAPIView):
    #LIB -> establecemos una instancia del serializer
    serializer_class = RegisterSerializer

    def post(self, request):
        #                     LIB
        serializer = self.get_serializer(data=request.data)
        # serializer ya me devuelve un JSON y validado
        if not serializer.is_valid(raise_exception=True): 
            # Response(data=None, status=None, headers=None, content_type=None)
            return Response(
                data={"errors":serializer.errors, "messages": "No pudo registrar correctamente"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save() # guardamos 

        return Response( # devolvemos la respeusta
            RegisterSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses=LoginSerializer
    )
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token: str = JWTService.generate_token(user)
        user_return = UserSerializer(user).data
        return Response(
            {
                "name": user_return,
                "success": True,
                "token": token
            },
            status=status.HTTP_200_OK
        )


