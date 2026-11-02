from django.urls import path
from .views.publico import TrabalhoPublicoViewSet, estatisticas

urlpatterns = [
    path("trabalhos", TrabalhoPublicoViewSet.as_view({"get": "list"}), name="listar-trabalhos-publicos",),
    path("trabalhos/<int:id_trabalho>", TrabalhoPublicoViewSet.as_view({"get": "retrieve"}), name="detalhar-trabalho-publico",),
    path("estatisticas", estatisticas, name="estatisticas")
]