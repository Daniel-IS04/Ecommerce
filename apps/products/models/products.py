from django.db import models
from django.db.models import F

class Product(models.Model) :
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    rating = models.IntegerField(blank=True, null=True, default=0)
    stock = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        
        
    def decrease_stock(self, quantity=1):
        updated = Product.objects.filter(id=self.id, stock__gte=quantity).update(stock=F('stock')-quantity)
        if updated == 0:
            return False  
        return True

        
    def __str__(self):
        return self.name