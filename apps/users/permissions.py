from rest_framework.permissions import BasePermission

class IsRoleAdmin (BasePermission):

    #para recordar el has_permission es polimorfismo
    #de una clase heredada [BasePermission]
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
        
        return getattr(user,"role",None) == "admin"
    
    