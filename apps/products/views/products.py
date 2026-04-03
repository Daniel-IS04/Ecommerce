from django.db.models.fields import PositiveIntegerRelDbTypeMixin
from django.views.generic import detail
from rest_framework import serializers, viewsets, status, filters
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from apps.products.models.products import Product
from apps.products.serializers.products import (
    ProductCreateSerializer,
    ProductReadClientSerializer,
    ProductReadAdminSerializer,
    ProductUpdateSerializer,
    ProductRatingSerializer,
)
from apps.products.views import products


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    filter_backends = [
        # GET /api/productos/?precio_min=100&precio_max=500
        # GET /api/productos/?categoria=electronica
        DjangoFilterBackend,  # permite hacer filtros complejos por [campos]
        filters.SearchFilter,  # puedo buscar varios campos a la vez
        filters.OrderingFilter,  # el orden en el response
    ]
    # Especifica qué campos permiten coincidencias exactas mediante parámetros de URL.
    # ?is_active=true o ?price=100
    filterset_fields = ["is_active", "price", "stock"]

    # Define las columnas donde el motor de búsqueda buscará
    # el texto enviado por el usuario ---> ?search=laptop
    search_fields = ["name", "description"]

    # Es una lista blanca de seguridad. Determina qué campos el cliente
    # tiene permiso de usar para ordenar
    ordering_fields = ["price", "rating", "created_at", "stock"]
    ordering = ["-created_at"]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "create":
            return ProductCreateSerializer
        elif self.action == ["updatepartial_update"]:
            return ProductUpdateSerializer
        elif self.action == "rate_product":
            return ProductRatingSerializer
        elif self.request.user.is_authenticated and self.request.user.is_staff:
            return ProductReadAdminSerializer
        return ProductReadClientSerializer

    def get_permissions(self):
        if self.action == ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(
            {
                "message": "Producto desactivado",
            },
            status=status.HTTP_200_OK,
        )

    @action(datail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def rate_product(self, request, pk=None):
        product = self.get_object()
        serializer = ProductRatingSerializer(
            product, data=request.data, many=False, partial=True
        )
        if serializer.is_valid():
            serializers.save()
            return Response(
                {
                    "message": "Producto calificado correctamente",
                    "data": serializers.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(datial=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def activate(self, request, pk=None):
        product = self.get_object()
        product.is_active = True
        product.save()
        return Response(
            {"message": "Produto Activado correctamente"},
            status=status.HTTP_200_OK,
        )
