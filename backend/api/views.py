from django.http.response import JsonResponse
from django.forms.models import model_to_dict

from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import generics, viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework import permissions, authentication

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


class ProductListCreateAPIViewSet(viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [authentication.SessionAuthentication]

    def list(self, request):
        query_set = Product.objects.order_by('-company')
        serializer = ProductSerializer(query_set, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            company_name = serializer.validated_data.get('company')
            if company_name.lower() == 'apple':
                return Response({'details': 'Please, no Apple products allowd'}, status=403)
            serializer.save()
        else:
            return Response({'details': 'Invalid Data'})


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
            # raise generics.ValidationError('No Apple products are allowed in store')
            return Response('Failed to save product. No Apple devices allowd', status=403)
        else:
            instance = serializer.save()


# Mixin based classes

class AppleProductListModelMixin(ListModelMixin, generics.GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        company = request.query_params.get('company')
        if company:
            self.queryset = self.queryset.filter(company__iexact=company)
        return super().list(request, *args, **kwargs)


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
