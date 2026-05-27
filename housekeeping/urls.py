from django.urls import path
from . import views

app_name = 'housekeeping'

urlpatterns = [
    path('tasks/', views.housekeeping_tasks, name='housekeeping_tasks'),
]
