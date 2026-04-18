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
    path('common/', include('common.urls')),
    path('accounts/', include('accounts.urls')),
    path('rooms/', include('rooms.urls')),
    path('reservations/', include('reservations.urls')),
    path('services/', include('services.urls')),
    path('staff/', include('staff.urls')),
    path('housekeeping/', include('housekeeping.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('billing/', include('billing.urls')),
    path('reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
