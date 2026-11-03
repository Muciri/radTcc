from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/schema/',
        SpectacularAPIView.as_view(
            permission_classes=[AllowAny], authentication_classes=[], throttle_classes=[]
        ),
        name='schema',
    ),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema',
            permission_classes=[AllowAny],
            authentication_classes=[],
            throttle_classes=[],
        ),
        name='docs',
    ),
    path('api/<version>/publico/', include('catalogo.urls_publico')),
    path('api/<version>/gestao/', include('catalogo.urls_gestao')),
]
