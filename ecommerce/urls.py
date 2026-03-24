"""
URL configuration for ecommerce project.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# ELIMINAMOS las importaciones de SimpleJWT
# Ya no necesitamos TokenObtainPairView ni TokenRefreshView aquí

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Documentación de la API (Swagger/Redoc)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # ELIMINAMOS las rutas api/token/ y api/token/refresh/
    # Delegación a las Apps (El enrutamiento real ocurre dentro de cada app)
    path("api/", include("apps.products.urls")),
    # Todas tus rutas de autenticación y perfil ahora viven dentro de este include
    # (ej. api/users/login/, api/users/refresh/, api/users/logout/, api/users/me/)
    path("api/users/", include("apps.users.urls")),
]

'''Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    
    # Apps URLs
    path('api/', include('apps.products.urls')),
    path('api/users/', include('apps.users.urls')),
]'''
