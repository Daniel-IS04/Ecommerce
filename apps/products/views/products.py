from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from apps.products.models.products import Product
from apps.products.serializers.products import (
    ProductCreateSerializer,
    ProductReadClientSerializer,
    ProductReadAdminSerializer,
    ProductUpdateSerializer,
    ProductRatingSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'price', 'stock']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'rating', 'created_at', 'stock']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        
        if self.request.user.is_authenticated and self.request.user.is_staff:
            queryset = super().get_queryset()
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        elif self.action == 'rate_product':
            return ProductRatingSerializer
        elif self.request.user.is_authenticated and self.request.user.is_staff:
            return ProductReadAdminSerializer
        return ProductReadClientSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(
            {"message": "Producto desactivado exitosamente"},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def rate_product(self, request, pk=None):
        product = self.get_object()
        serializer = ProductRatingSerializer(product, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Producto calificado exitosamente", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def activate(self, request, pk=None):
        product = self.get_object()
        product.is_active = True
        product.save()
        return Response(
            {"message": "Producto activado exitosamente"},
            status=status.HTTP_200_OK
        )
