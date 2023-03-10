from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product

chinese_company_list = ['oppo', 'vivo', 'realme', 'oneplus', 'xiomi', 'mi', 'huawei']

def iphone_validator(value):
    print(value)
    if 'iphone' in value.lower():
        raise serializers.ValidationError(detail='No iPhones please')
    return value

class ProductSerializer(serializers.ModelSerializer):
    black_friday_price = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(validators=[iphone_validator])
    user = serializers.CharField(read_only=True)
    # product_details_url = serializers.SerializerMethodField(read_only=True)
    
    # This works only with model serializer.
    # url = serializers.HyperlinkedIdentityField('product-details', lookup_field='pk')
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name', 
            'company',
            'price',
            'description',
            'black_friday_price',
            'user'
        ]
        
    def validate_company(self, value):
        if value.lower() in chinese_company_list:
            raise serializers.ValidationError(detail='No CHINESE company allowed here.')
        return value
        
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['user'] = request.user
            
        return super().create(validated_data)
        
    def get_black_friday_price(self, instance):
        if not isinstance(instance, Product):
            return None
        return instance.black_friday_price()