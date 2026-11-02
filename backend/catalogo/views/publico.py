from django.db.models import Count
from django_filters import rest_framework as filters
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from catalogo.models import Trabalho
from catalogo.serializers.publico import (
    EstatisticasSerializer,
    TrabalhoPublicoDetalheSerializer,
    TrabalhoPublicoSerializer,
)


class TrabalhoPublicoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class TrabalhoFilter(filters.FilterSet):
    curso = filters.CharFilter(
        field_name="curso__sigla",
        lookup_expr="iexact",
        help_text="Sigla do curso, por exemplo `TSI`.",
    )
    palavra_chave = filters.CharFilter(
        field_name="palavras_chave__termo",
        lookup_expr="iexact",
        distinct=True,
        help_text="Termo exato da palavra-chave.",
    )

    class Meta:
        model = Trabalho
        fields = ["ano"]


@extend_schema_view(
    list=extend_schema(
        tags=["Trabalhos públicos"],
        summary="Listar trabalhos publicados",
        description="""
        Retorna uma lista paginada de trabalhos acadêmicos publicados.

        **Busca:**
        Permite pesquisar por título, resumo, nome dos autores
        e nome do orientador utilizando o parâmetro `search`.

        **Filtros:**
        Permite filtrar os resultados por `ano`, `curso` (sigla) e
        `palavra_chave` (termo). Os filtros podem ser combinados entre si
        e com a busca.

        **Ordenação:**
        Permite ordenar os resultados por ano ou título com o parâmetro
        `ordering`. Utilize o sinal `-` para indicar ordem decrescente.

        **Paginação:**
        Retorna 10 registros por página por padrão.
        O tamanho pode ser alterado pelo parâmetro `page_size`.
        """,
    ),
    retrieve=extend_schema(
        tags=["Trabalhos públicos"],
        summary="Consultar detalhes de um trabalho",
        description="""
        Retorna os dados detalhados de um trabalho acadêmico
        publicado, identificado pelo seu ID.

        Somente trabalhos com situação PUBLICADO podem ser consultados.
        Caso o trabalho não exista ou não esteja publicado,
        será retornado HTTP 404.
        """,
    ),
)
class TrabalhoPublicoViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    search_fields = ["titulo", "resumo", "orientador__nome", "autores__nome"]
    filterset_class = TrabalhoFilter
    ordering_fields = ["ano", "titulo"]
    ordering = ["-ano", "titulo"]

    filter_backends = [
        SearchFilter,
        filters.DjangoFilterBackend,
        OrderingFilter,
    ]

    pagination_class = TrabalhoPublicoPagination

    def get_queryset(self):
        return (
            Trabalho.objects.filter(situacao=Trabalho.Situacao.PUBLICADO)
            .select_related("curso", "orientador", "coorientador")
            .prefetch_related("autores", "palavras_chave")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TrabalhoPublicoDetalheSerializer

        return TrabalhoPublicoSerializer

@extend_schema(
    tags=["Estatísticas públicas"],
    summary="Consultar estatísticas dos trabalhos",
    description="""
    Retorna estatísticas quantitativas dos trabalhos acadêmicos publicados.
    """,
    responses={
        200: OpenApiResponse(
            response=EstatisticasSerializer,
            description="Estatísticas dos trabalhos publicados.",
            examples=[
                OpenApiExample(
                    "Exemplo de resposta",
                    value={
                        "trabalhos_por_ano": {
                            "2025": 4,
                            "2024": 5,
                            "2023": 6,
                        },
                        "trabalhos_por_curso": {
                            "TSI": 9,
                            "LMAT": 5,
                        },
                        "orientadores_com_mais_trabalhos": [
                            {
                                "nome": "Mariana Cavalcanti Rocha",
                                "total": 4,
                            },
                            {
                                "nome": "Renata Albuquerque Lima",
                                "total": 3,
                            },
                        ],
                    },
                    response_only=True,
                ),
            ],
        ),
    },
)
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def estatisticas(request, **kwargs):
    trabalhos = Trabalho.objects.filter(
        situacao=Trabalho.Situacao.PUBLICADO
    )

    por_ano = trabalhos.values("ano").annotate(
        total=Count("id")
    ).order_by("-ano")

    por_curso = trabalhos.values(
        "curso__sigla"
    ).annotate(
        total=Count("id")
    ).order_by("-total")

    por_orientador = trabalhos.values(
        "orientador__nome"
    ).annotate(
        total=Count("id")
    ).order_by("-total")[:10]

    return Response({
        "trabalhos_por_ano": {
            item["ano"]: item["total"] for item in por_ano
        },
        "trabalhos_por_curso": {
            item["curso__sigla"]: item["total"] for item in por_curso
        },
        "orientadores_com_mais_trabalhos": [
            {
                "nome": item["orientador__nome"],
                "total": item["total"],
            }
            for item in por_orientador
        ],
    })