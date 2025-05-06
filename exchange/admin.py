from django.contrib import admin
from .models import Book, ExchangeOffer, ExchangeRequest

admin.site.register(Book)
admin.site.register(ExchangeOffer)
admin.site.register(ExchangeRequest)
