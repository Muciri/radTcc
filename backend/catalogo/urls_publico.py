from django.urls import path
from .views.publico import listar_trabalhos_publicos

urlpatterns = [
    path('trabalhos/', listar_trabalhos_publicos, name='listar-trabalhos-publicos'),
]