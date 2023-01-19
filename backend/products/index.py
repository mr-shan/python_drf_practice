from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Product

@register(Product)
class ProductIndex(AlgoliaIndex):
    fields=[
        'name',
        'company',
        'description',
        'price',
        'public',
        'user',
    ]
    index_name='drf_product_index'
