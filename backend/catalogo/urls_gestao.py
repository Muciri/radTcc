from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views.gestao import (
    AutorViewSet,
    CursoViewSet,
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
    path('token/', obtain_auth_token, name='token'),
    path('', include(router.urls)),
]
