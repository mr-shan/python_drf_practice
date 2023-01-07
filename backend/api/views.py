from django.http.response import JsonResponse
from django.forms.models import model_to_dict

from rest_framework.response import Response
from rest_framework.decorators import api_view

from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def index(request, *args, **kwargs):
    if request.method == 'GET':        
        instance = Product.objects.all().order_by('?').first()
        data = {}

        if instance:
            data = ProductSerializer(instance).data

        return Response(data)
    elif request.method == 'POST':        
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            try:
                serializer.save()
            except Exception as e:
                print(e)
            return Response(serializer.validated_data)
        else:
            return Response({'details': 'Invalid Data'})


# The typical django way of writing view functions.
# def index(request, *args, **kwargs):
#     random_product = Product.objects.all().order_by('?').first()
#     data = {}

#     if random_product:
#         # data['name'] = random_product.name
#         # data['company'] = random_product.company
#         # data['price'] = random_product.price
#         data = model_to_dict(random_product, fields=['name', 'company', 'price'])

#     return JsonResponse(data)
