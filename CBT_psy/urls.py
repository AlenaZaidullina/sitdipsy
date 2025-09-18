from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import logging

logger = logging.getLogger(__name__)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls'), name='index'),
    path('appt/', include('appointment_app.urls')),
    path('products/', include('psyproducts_app.urls')),
    path('bot/', include('bot.urls')),
    path('channel/', include('moms_channel_app.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
