from django.http.response import JsonResponse
from django.forms.models import model_to_dict

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

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
            # try:
            #     serializer.save()
            # except Exception as e:
            #     print(e)
            return Response(serializer.validated_data)
        else:
            return Response({'details': 'Invalid Data'})



# special generic views that django offers
class ProductDetailsAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('company')
    serializer_class = ProductSerializer

    def get_queryset(self):
        query_set = Product.objects.all()
        comp_name = self.request.query_params.get('company')
        if comp_name is not None:
            query_set = query_set.filter(company__iexact=comp_name)
        return query_set

    def perform_create(self, serializer):
        company = serializer.validated_data.get('company')
        print(company)
        if company.upper() == 'APPLE':
            raise generics.ValidationError('No Apple products are allowed in store')
        else:
            instance = serializer.save()


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
