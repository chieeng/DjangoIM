from django.contrib import admin
from .models import Invoice, Payment, Discount


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'reservation', 'total_amount', 'invoice_status', 'due_date')
    list_filter = ('invoice_status', 'due_date')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'invoice', 'amount_paid', 'payment_method', 'payment_status')
    list_filter = ('payment_status', 'payment_method', 'payment_date')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_name', 'percentage', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
