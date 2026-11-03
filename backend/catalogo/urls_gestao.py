from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.gestao import (
    AutorViewSet,
    CursoViewSet,
    ObterTokenView,
    OrientadorViewSet,
    PalavraChaveViewSet,
    TrabalhoGestaoViewSet,
)

router = DefaultRouter()
router.register('trabalhos', TrabalhoGestaoViewSet, basename='gestao-trabalho')
router.register('cursos', CursoViewSet, basename='gestao-curso')
router.register('orientadores', OrientadorViewSet, basename='gestao-orientador')
router.register('autores', AutorViewSet, basename='gestao-autor')
router.register('palavras-chave', PalavraChaveViewSet, basename='gestao-palavra-chave')

urlpatterns = [
    path('token/', ObterTokenView.as_view(), name='token'),
    path('', include(router.urls)),
]
