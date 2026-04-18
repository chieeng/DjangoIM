from django.shortcuts import render
from .models import Invoice, Payment


def invoice_list(request):
    """List invoices"""
    if request.user.is_authenticated:
        invoices = Invoice.objects.filter(reservation__customer=request.user)
    else:
        invoices = Invoice.objects.none()
    context = {'invoices': invoices}
    return render(request, 'billing/invoice_list.html', context)


def payment_history(request):
    """View payment history"""
    if request.user.is_authenticated:
        payments = Payment.objects.filter(invoice__reservation__customer=request.user)
    else:
        payments = Payment.objects.none()
    context = {'payments': payments}
    return render(request, 'billing/payment_history.html', context)
