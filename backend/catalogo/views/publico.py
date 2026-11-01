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
from catalogo.serializers.publico import TrabalhoPublicoSerializer,TrabalhoPublicoDetalheSerializer

class TrabalhoPublicoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

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