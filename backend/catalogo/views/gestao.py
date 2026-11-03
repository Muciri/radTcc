from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from catalogo.excecoes import Conflito
from catalogo.models import Autor, Curso, Orientador, PalavraChave, Trabalho
from catalogo.serializers.gestao import (
    AutorSerializer,
    CursoSerializer,
    OrientadorSerializer,
    PalavraChaveSerializer,
    TrabalhoGestaoSerializer,
)


class TrabalhoGestaoViewSet(viewsets.ModelViewSet):
    """
    Cadastro e manutenção de trabalhos, em qualquer situação.

    O campo `cadastrado_por` é definido pelo token da requisição e não
    é aceito no corpo. Para publicar, o trabalho precisa ter nota e data de defesa.
    """

    serializer_class = TrabalhoGestaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["situacao", "ano", "curso"]

    def get_queryset(self):
        return Trabalho.objects.select_related(
            "curso", "orientador", "coorientador", "cadastrado_por"
        ).prefetch_related("autores", "palavras_chave")

    def perform_create(self, serializer):
        serializer.save(cadastrado_por=self.request.user)


class CursoViewSet(viewsets.ModelViewSet):
    """Cadastro de cursos."""

    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class OrientadorViewSet(viewsets.ModelViewSet):
    """Cadastro de orientadores."""

    queryset = Orientador.objects.all()
    serializer_class = OrientadorSerializer


class AutorViewSet(viewsets.ModelViewSet):
    """Cadastro de autores."""

    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

    def perform_destroy(self, instance):
        # remover o único autor de um trabalho deixaria o trabalho sem autor
        unico = instance.trabalhos.annotate(n=Count("autores")).filter(n=1).count()
        if unico:
            raise Conflito(
                f"Não é possível remover: este autor é o único de {unico} trabalho(s)."
            )
        instance.delete()


class PalavraChaveViewSet(viewsets.ModelViewSet):
    """Cadastro de palavras-chave."""

    queryset = PalavraChave.objects.all()
    serializer_class = PalavraChaveSerializer
