import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

# Usamos get_user_model() por buenas prácticas de Django
User = get_user_model()

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 1. Buscamos el header 'Authorization'
        auth_header = request.headers.get('Authorization')
        
        # Si no hay header, devolvemos None (DRF sabrá que es un anónimo)
        if not auth_header:
            return None

        # 2. Verificamos que el formato sea "Bearer <token>"
        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None # Si no dice Bearer, lo ignoramos
        except ValueError:
            # Si el header está mal formado (ej. solo dice "Bearer" sin token)
            raise AuthenticationFailed('Formato de token inválido. Usa: Bearer <token>')

        # 3. Decodificamos el token
        try:
            # NOTA: Asegúrate de que el algoritmo coincida con el que usaste en JWTService
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('El token ha expirado. Por favor, refresca tu token.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('El token es inválido o está corrupto.')

        # 4. Extraemos el ID del usuario del payload
        # OJO: Aquí asumo que en tu JWTService guardaste el id como 'user_id'
        user_id = payload.get('user_id') 
        
        if not user_id:
            raise AuthenticationFailed('El token no contiene la información del usuario (falta user_id).')

        # 5. Buscamos al usuario en la base de datos
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('El usuario de este token ya no existe en el sistema.')

        # Si el usuario está inactivo (opcional pero recomendado)
        if not user.is_active:
            raise AuthenticationFailed('Este usuario está inactivo.')

        # 6. Éxito: Devolvemos la tupla (usuario_encontrado, token_usado)
        return (user, token)
