from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from .settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT


urlpatterns = static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT) + [
    path("admin/", admin.site.urls),
    path('api/dashboard/', include('dashboard_api.urls')),
]