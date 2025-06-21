from django.contrib import admin
from django.urls import path
from search.views import search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/search', search, name='search'),
]