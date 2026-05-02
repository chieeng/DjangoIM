from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
app_name = 'common'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('admin/', admin.site.urls),
    path('booking/', include('booking.urls')),
]
