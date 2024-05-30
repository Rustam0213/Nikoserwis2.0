from django.contrib import admin
from django.urls import path, include
from .views import CustomLoginView, Register, application_details, profile, wiadomosc, user_profile, kod
from django.conf import settings

urlpatterns = [
      path('', include('django.contrib.auth.urls')),
      path('kod/', kod, name='kod'), 
      path('rejestracja/', Register.as_view(), name='register'),
      path('login/', CustomLoginView.as_view(), name='login'),
      path('konto/', profile, name='profile'),
      path('wiadomosc', wiadomosc, name='wiadomosc'),
      path('zgloszenie/<int:application_id>/', application_details, name='application_details'),
      path('dane-konta', user_profile, name='user_profile'),
]
