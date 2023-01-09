from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    black_friday_price = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name', 
            'company',
            'price',
            'description',
            'black_friday_price',
        ]
        
    def get_black_friday_price(self, instance):
        if not isinstance(instance, Product):
            return None
        return instance.black_friday_price()