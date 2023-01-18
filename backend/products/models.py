from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

current_discount = 12


class Product(models.Model):
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

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
