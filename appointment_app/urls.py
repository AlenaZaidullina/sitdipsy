from django.urls import path
from . import views
from .views import PrivacyPolicyView, consent_form

urlpatterns = [
    path('', views.appointment, name='appointment'),
    path('api/available-dates/', views.get_available_dates, name='available_dates'),
    path('api/available-times/<str:date_str>/', views.get_available_times, name='available_times'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('consent-form/', consent_form, name='consent_form'),
]