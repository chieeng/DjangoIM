from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('addNewReports/', views.add_report, name='add_report'),
    path('api/report-data/', views.get_report_data, name='get_report_data'),
    path('<int:pk>/', views.report_detail, name='report_detail'),
    path('<int:pk>/edit/', views.edit_report, name='edit_report'),
    path('<int:pk>/delete/', views.delete_report, name='delete_report'),
]
