from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ..serializers.user_serializers import UserSerializer


# podemos que el usuario vea y edite su propio perfil
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)
    
    #editar mi perfil
    def patch(self, request):
        #lo editable
        allowed = {"first_name", "last_name", "phone_number"}
        
        #filtro de sens
        data = {k: v for k, v in request.data.items() if k in allowed}

        #cargar los cambios
        for k, v in data.items():
            setattr(request.user, k, v)
        
        #guarda
        request.user.save()
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

