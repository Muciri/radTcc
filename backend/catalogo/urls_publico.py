from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.publico import TrabalhoPublicoViewSet, estatisticas

# SimpleRouter evita a página raiz do DefaultRouter, que exigiria autenticação
router = SimpleRouter()
router.register("trabalhos", TrabalhoPublicoViewSet, basename="publico-trabalho")

urlpatterns = [
    path("estatisticas/", estatisticas, name="publico-estatisticas"),
    path("", include(router.urls)),
]
