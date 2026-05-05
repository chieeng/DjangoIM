from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('addNewReports/', views.add_report, name='add_report'),
]
