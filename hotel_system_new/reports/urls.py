from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('addNewReport/', views.add_report, name='add_report'),
]
