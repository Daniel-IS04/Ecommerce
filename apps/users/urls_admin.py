from rest_framework.routers import DefaultRouter
from apps.users.views.admin_user_views import AdminUserViewSet

router = DefaultRouter()

#investigar mas de routers

# se encara .refister de poder armar todo compeltamente la ruta 
#register cuenta contres pqaramtros (1,2,3)
router.register(r"users", AdminUserViewSet, basename="admin-users")

urlpatterns = router.urls
