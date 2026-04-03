from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from ..serializers.user_serializers import UserSerializer
from ..serializers.me_serializers import MeSerializer


# podemos que el usuario vea y edite su propio perfil
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    # editar mi perfil
    @extend_schema(request=MeSerializer, responses=UserSerializer)
    def patch(self, request):
        serializers = MeSerializer(request.user, data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)

        serializers.save()
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
