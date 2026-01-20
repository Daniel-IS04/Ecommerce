from rest_framework import serializers
from apps.products.models.products import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']
        
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value
    
    
class ProductReadClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'rating', 'stock']
        


class ProductReadAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'rating', 'stock', 'is_active']
        


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['rating'] 

    def validate_calification(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La calificación debe estar entre 1 y 5")
        return value


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'is_active', 'rating']
        
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return value
    
    def validate_rating(self, value):
        if value is not None and (value < 0 or value > 5):
            raise serializers.ValidationError("La calificación debe estar entre 0 y 5")
        return value