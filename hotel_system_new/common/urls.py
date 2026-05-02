from django.urls import path
from . import views
app_name = 'common'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.home, name='home'),
    path('edit-profile/', views.edit_profile_redirect, name='edit_profile'),
    path('add-record/', views.add_new_record, name='add_record'),
    path('logoff/', views.logoff_redirect, name='logoff'),
]
