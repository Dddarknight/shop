from django.contrib import admin
from shop.products.models import Product, PropertyObject, Value, Status, Image


admin.site.register(Product)
admin.site.register(PropertyObject)
admin.site.register(Value)
admin.site.register(Status)
admin.site.register(Image)
