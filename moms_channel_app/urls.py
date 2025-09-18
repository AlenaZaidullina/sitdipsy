from django.urls import path
from . import views

urlpatterns = [
    path('', views.moms_channel, name='moms_channel'),
]
