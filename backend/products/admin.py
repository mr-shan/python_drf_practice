from django.contrib import admin

from .models import Product

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'price')

# admin.site.register(Product, ProductAdmin)