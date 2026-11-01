from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count

from catalogo.models import Trabalho
from catalogo.serializers.publico import TrabalhoPublicoSerializer,TrabalhoPublicoDetalheSerializer, OrientadorEstatisticaSerializer, EstatisticasSerializer

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiExample,
    inline_serializer,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

class TrabalhoPublicoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

@extend_schema_view(
    list=extend_schema(
        tags=["Trabalhos públicos"],
        summary="Listar trabalhos publicados",
        description="""
        Retorna uma lista paginada de trabalhos acadêmicos publicados.

        **Busca (RF5):**
        Permite pesquisar por título, resumo, nome dos autores
        e nome do orientador utilizando o parâmetro `search`.

        **Filtros (RF6):**
        Permite filtrar os resultados por ano, curso e palavra-chave.
        Os filtros podem ser combinados entre si e com a busca.

        **Ordenação (RF7):**
        Permite ordenar os resultados por ano ou título.
        Utilize o sinal `-` para indicar ordem decrescente.

        **Paginação (RF7):**
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

    lookup_field = "id"
    lookup_url_kwarg = "id_trabalho"

    search_fields = ["titulo", "resumo", "orientador__nome", "autores__nome",]
    filterset_fields = ["ano", "curso", "palavras_chave",]
    ordering_fields = ["ano", "titulo",]
    ordering = ["-ano", "titulo"]

    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]

    pagination_class = TrabalhoPublicoPagination

    def get_queryset(self):
        return Trabalho.objects.filter(
            situacao=Trabalho.Situacao.PUBLICADO
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
                            "2023": 15,
                            "2024": 28,
                            "2025": 42,
                        },
                        "trabalhos_por_curso": {
                            "ADS": 35,
                            "SI": 28,
                            "GTI": 22,
                        },
                        "orientadores_com_mais_trabalhos": [
                            {
                                "nome": "João da Silva",
                                "total": 12,
                            },
                            {
                                "nome": "Maria Oliveira",
                                "total": 9,
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