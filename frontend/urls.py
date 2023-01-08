from django.contrib import admin
from django.urls import path, include
from .views import index

app_name = 'frontend'

urlpatterns = [
    path('', index, name=''),
    path('create', index),
    path('join', index),
    path('party', index, name='party'),
]