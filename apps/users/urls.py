from django.urls import path, include

from .views.auth_views import RegisterView, LoginView
from .views.me_views import MeView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", MeView.as_view()),
    path("api/admin/", include("apps.users.urls_admin")),

]
