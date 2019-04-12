from django.contrib import admin
from .models import ProductPrice, Product, GiftCard, BlackFriday

# Register your models here.

admin.site.register(Product)
admin.site.register(GiftCard)
admin.site.register(ProductPrice)
admin.site.register(BlackFriday)
