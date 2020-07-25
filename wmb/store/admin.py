from django.contrib import admin

from .models import Product, Branch, ProductImage

admin.site.register(Product)
admin.site.register(Branch)
admin.site.register(ProductImage)
