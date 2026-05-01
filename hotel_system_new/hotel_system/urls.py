"""
URL configuration for hotel_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from common import views as common_views

urlpatterns = [
    path('', common_views.index, name='index'),  # Landing page as home
    path('admin/', admin.site.urls),
    path('common/', include('common.urls', namespace='common')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('rooms/', include('rooms.urls', namespace='rooms')),
    path('reservations/', include('reservations.urls', namespace='reservations')),
    path('services/', include('services.urls', namespace='services')),
    path('staff/', include('staff.urls', namespace='staff')),
    path('housekeeping/', include('housekeeping.urls', namespace='housekeeping')),
    path('maintenance/', include('maintenance.urls', namespace='maintenance')),
    path('billing/', include('billing.urls', namespace='billing')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
