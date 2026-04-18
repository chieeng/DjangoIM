from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('payments/', views.payment_history, name='payment_history'),
]
