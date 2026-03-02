from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from apps.users.permissions import IsRoleAdmin
from apps.users.serializers.admin_user_serializer import AdminUserSerizalizer

User = get_user_model()


class AdminUserViewSet(ModelViewSet):
    """
    CRUD admin de usuarios (backend).
    - GET list:    /api/admin/users/
    - GET detail:  /api/admin/users/<id>/
    - POST create: /api/admin/users/
    - PATCH update:/api/admin/users/<id>/
    """

    """ 
    Aclaramos algo, primero  esto solo maneja las respeus tas y la logica
    derivandolas en otros, este caso utilizamos
    modelViewSet ya que trae todo para el CRUD , de manera general 
    """
    # para listar todo o solo una parte =>
    queryset = User.objects.all().order_by("id")
    serializer_class = AdminUserSerizalizer
    
    permission_classes = [IsRoleAdmin]
    # para que no puedan usar DELETE o PUT si no quieres
    http_method_names = ["get", "post", "patch"]
