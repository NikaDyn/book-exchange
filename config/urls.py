from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('book_list', permanent=False)),
    path('books/', include('exchange.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]