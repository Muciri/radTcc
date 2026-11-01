from django.urls import path
from .views.publico import listar_trabalhos_publicos, ver_trabalho

urlpatterns = [
    path('trabalhos', listar_trabalhos_publicos, name='listar-trabalhos-publicos'),
    path('trabalhos/<int:id_trabalho>', ver_trabalho, name='listar-trabalhos-publicos'),
]