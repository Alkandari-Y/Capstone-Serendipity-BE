from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings

from core.schema import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/docs/swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("api/docs/redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('accounts.urls')),
    path('api/', include('checkins.urls')),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


