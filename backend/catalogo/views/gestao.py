from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken

from catalogo.excecoes import Conflito
from catalogo.models import Autor, Curso, Orientador, PalavraChave, Trabalho
from catalogo.serializers.gestao import (
    AutorSerializer,
    CursoSerializer,
    OrientadorSerializer,
    PalavraChaveSerializer,
    TrabalhoGestaoSerializer,
)


@extend_schema(
    tags=["Autenticação"],
    summary="Obter token da coordenação",
    description=(
        "Troca usuário e senha por um token. Nas demais rotas da gestão, envie o "
        "cabeçalho `Authorization: Token <token>`. Credenciais inválidas "
        "respondem 400."
    ),
    auth=[],
)
class ObterTokenView(ObtainAuthToken):
    pass


@extend_schema_view(
    list=extend_schema(
        summary="Listar trabalhos",
        description=(
            "Lista paginada de trabalhos em qualquer situação, com nota. "
            "Aceita os filtros `situacao`, `ano` e `curso` (id)."
        ),
    ),
    retrieve=extend_schema(summary="Consultar um trabalho"),
    create=extend_schema(
        summary="Cadastrar trabalho",
        description=(
            "Regras validadas: o ano não pode ser maior que o ano corrente, "
            "o trabalho precisa de um ou dois autores, não pode haver outro com o "
            "mesmo título no mesmo curso e ano, e só vai para `publicado` com nota "
            "e data de defesa. O campo `cadastrado_por` é definido pelo token e "
            "qualquer valor enviado é ignorado. Violações respondem 400 com a "
            "descrição do erro por campo."
        ),
    ),
    update=extend_schema(summary="Substituir trabalho"),
    partial_update=extend_schema(
        summary="Alterar trabalho",
        description=(
            "Para publicar, envie `situacao: publicado` com nota e data de defesa "
            "já cadastradas ou informadas na mesma requisição."
        ),
    ),
    destroy=extend_schema(summary="Excluir trabalho"),
)
@extend_schema(tags=["Gestão: trabalhos"])
class TrabalhoGestaoViewSet(viewsets.ModelViewSet):
    """Cadastro e manutenção de trabalhos, em qualquer situação."""

    serializer_class = TrabalhoGestaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["situacao", "ano", "curso"]

    def get_queryset(self):
        return Trabalho.objects.select_related(
            "curso", "orientador", "coorientador", "cadastrado_por"
        ).prefetch_related("autores", "palavras_chave")

    def perform_create(self, serializer):
        serializer.save(cadastrado_por=self.request.user)


@extend_schema_view(
    destroy=extend_schema(
        description="Responde 409 se houver trabalhos vinculados ao curso."
    )
)
@extend_schema(tags=["Gestão: cursos"])
class CursoViewSet(viewsets.ModelViewSet):
    """Cadastro de cursos."""

    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


@extend_schema_view(
    destroy=extend_schema(
        description="Responde 409 se o orientador estiver em algum trabalho."
    )
)
@extend_schema(tags=["Gestão: orientadores"])
class OrientadorViewSet(viewsets.ModelViewSet):
    """Cadastro de orientadores."""

    queryset = Orientador.objects.all()
    serializer_class = OrientadorSerializer


@extend_schema_view(
    destroy=extend_schema(
        description="Responde 409 se o autor for o único autor de algum trabalho."
    )
)
@extend_schema(tags=["Gestão: autores"])
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


@extend_schema(tags=["Gestão: palavras-chave"])
class PalavraChaveViewSet(viewsets.ModelViewSet):
    """Cadastro de palavras-chave."""

    queryset = PalavraChave.objects.all()
    serializer_class = PalavraChaveSerializer
