from django.db import models
from django.conf import settings
from django.db.models import Q

User = settings.AUTH_USER_MODEL

current_discount = 12

class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def perform_search(self, query, user=None):
        lookup = Q(name__icontains=query) | Q(company__icontains=query) | Q(description__icontains=query)
        return self.filter(lookup)
    

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def perform_search(self, query_string, user=None):
        return self.get_queryset().perform_search(query_string, user=user)


class Product(models.Model):
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    public = models.BooleanField(default=True)

    objects = ProductManager()

    @property
    def summary(self):
        return f"{self.company} {self.name} ({self.price})"
    
    @property
    def sale_price(self):
        current_price = float(self.price)
        discounted_price = current_price - (current_price * (current_discount / 100))
        return round(discounted_price, 2)
    
    def black_friday_price(self):
        return self.sale_price

    def __str__(self):
        return self.summary
