from django.contrib import admin
from django.urls import path, include
from informacja import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('nikoserwisadmin/', admin.site.urls),
    path('uzytkownicy/', include('crm.urls')),
    path('', views.main_page, name = 'main_page'),
    path('nowosci/', views.nowosci, name = 'nowosci'),
    path('promocje/', views.promocje, name = 'promocje'),
    path('humor/', views.humor, name = 'humor'),
    path('polityka-prywatnosci/', views.polityka, name = 'polityka'),
    path('error/', views.error, name = 'error'),
    path('kalendarz', views.calendar, name='calendar'),  
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
