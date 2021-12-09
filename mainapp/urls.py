from django.urls import path
from .views import products

app_name = 'main_app'

urlpatterns = [
    path('', products, name='index'),
]