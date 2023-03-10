from django.http.response import JsonResponse
from django.forms.models import model_to_dict

from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import generics, viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework import permissions, authentication
from django_filters.rest_framework import DjangoFilterBackend

from products.models import Product
from products.serializers import ProductSerializer
from .authentication import TokenAuthentication
# Create your views here.


# special generic views that django offers
class ProductDetailsAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListCreateAPIViewSet(viewsets.GenericViewSet):
    """Used as /api/products/"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company', 'name']

    def list(self, request):
        # query_set = Product.objects.order_by('-company')
        # serializer = ProductSerializer(query_set, many=True)
        serializer = ProductSerializer(self.filter_queryset(self.get_queryset()), many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.validated_data)
        else:
            return Response({'details': 'Invalid Data'})


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('company')
    serializer_class = ProductSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company', 'name']

    def get_queryset(self):
        query_set = Product.objects.all()
        if not self.request.user.is_superuser:
            query_set = query_set.filter(user=self.request.user)
        return query_set


class ProductSearchAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query_string = self.request.GET.get('q')
        if query_string:
            return queryset.perform_search(query_string)
        else:
            return queryset

    # def perform_create(self, serializer):
    #     company = serializer.validated_data.get('company')
    #     print(company)
    #     if company.upper() == 'APPLE':
    #         # raise generics.ValidationError('No Apple products are allowed in store')
    #         return Response('Failed to save product. No Apple devices allowed', status=403)
    #     else:
    #         serializer.save()
    #         return Response(serializer.validated_data)


# Mixin based classes

# class AppleProductListModelMixin(ListModelMixin, generics.GenericAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()

#     def get(self, request, *args, **kwargs):
#         company = request.query_params.get('company')
#         if company:
#             self.queryset = self.queryset.filter(company__iexact=company)
#         return super().list(request, *args, **kwargs)


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



# function based views with each HTTP request types handled specifically 

# @api_view(['GET', 'POST'])
# def index(request, *args, **kwargs):
#     if request.method == 'GET':
#         instance = Product.objects.all().order_by('?').first()
#         data = {}

#         if instance:
#             data = ProductSerializer(instance).data

#         return Response(data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             print(serializer.validated_data)
#             # try:
#             #     serializer.save()
#             # except Exception as e:
#             #     print(e)
#             return Response(serializer.validated_data)
#         else:
#             return Response({'details': 'Invalid Data'})