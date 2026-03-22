from django.urls import path, include

from .views.auth_views import RegisterView, LoginView, TokenRefreshView
from .views.me_views import MeView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", MeView.as_view()),
    path("peroooooooooooooooooooooadmin/", include("apps.users.urls_admin")),
    path("refresh/", TokenRefreshView.as_view()),
]
