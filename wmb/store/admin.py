from django.contrib import admin

from .models import Product, Branch, ProductImage, Order

admin.site.register(Product)
admin.site.register(Branch)
admin.site.register(ProductImage)
admin.site.register(Order)
