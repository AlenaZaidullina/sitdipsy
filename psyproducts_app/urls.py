from django.urls import path
from . import views

urlpatterns = [
    path('', views.psyproducts, name='psyproducts'),
]
