from django.contrib import admin
from django.utils.html import format_html
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_date', 'total_bookings_display', 'revenue_display', 'occupancy_rate_display')
    list_filter = ('report_date',)
    search_fields = ('notes',)
    readonly_fields = ('total_bookings', 'revenue', 'occupancy_rate', 'data_summary')
    fieldsets = (
        ('Report Information', {
            'fields': ('report_date',)
        }),
        ('Auto-Calculated Metrics', {
            'fields': ('total_bookings', 'revenue', 'occupancy_rate'),
            'description': '<strong>These fields are automatically calculated from the database when the report is created or updated.</strong>'
        }),
        ('Data Summary', {
            'fields': ('data_summary',),
            'classes': ('collapse',)
        }),
        ('Additional Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        })
    )

    def total_bookings_display(self, obj):
        """Display total bookings with color coding"""
        if obj.total_bookings == 0:
            color = 'red'
        elif obj.total_bookings < 5:
            color = 'orange'
        else:
            color = 'green'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.total_bookings
        )
    total_bookings_display.short_description = 'Total Bookings'

    def revenue_display(self, obj):
        """Display revenue with currency formatting"""
        color = 'green' if obj.revenue > 0 else 'red'
        formatted = f'{obj.revenue:,.2f}'          
        return format_html(
            '<span style="color: {}; font-weight: bold;">₱{}</span>',
            color,
            formatted                              
        )
    revenue_display.short_description = 'Total Revenue'

    def occupancy_rate_display(self, obj):
        """Display occupancy rate with color coding"""
        if obj.occupancy_rate < 30:               
            color = 'red'
        elif obj.occupancy_rate < 70:
            color = 'orange'
        else:
            color = 'green'
        formatted = f'{obj.occupancy_rate:.1f}'    
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}%</span>',
            color,
            formatted                            
        )
    occupancy_rate_display.short_description = 'Occupancy Rate'

    def data_summary(self, obj):
        """Display a summary of all calculated data"""
        if not obj.id:
            return "Save the report to see data summary"
        revenue_fmt = f'{obj.revenue:,.2f}'        
        occupancy_fmt = f'{obj.occupancy_rate:.1f}' 
        return format_html(
            '<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">'
            '<p><strong>Report Date:</strong> {}</p>'
            '<p><strong>Total Bookings:</strong> {}</p>'
            '<p><strong>Total Revenue:</strong> ₱{}</p>'
            '<p><strong>Occupancy Rate:</strong> {}%</p>'
            '</div>',
            obj.report_date,
            obj.total_bookings,
            revenue_fmt,
            occupancy_fmt
        )
    data_summary.short_description = 'Data Summary'

    def save_model(self, request, obj, form, change):
        """Override save to ensure calculate_data is called"""
        obj.calculate_data()
        super().save_model(request, obj, form, change)