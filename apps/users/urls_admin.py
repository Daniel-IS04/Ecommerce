from rest_framework.routers import DefaultRouter
from apps.users.views.admin_user_views import AdminUserViewSet

# me genera todas las aplicacion (get, post, ... patch)
router = DefaultRouter()

router.register(r"users", AdminUserViewSet, basename="admin-users")

# de cualquier importancion en otro archivo solo captara urlpatterns
urlpatterns = router.urls
