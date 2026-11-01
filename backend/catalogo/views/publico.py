from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny

from catalogo.models import Trabalho
from catalogo.serializers.publico import TrabalhoPublicoSerializer,TrabalhoPublicoDetalheSerializer

class TrabalhoPublicoViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    lookup_field = "id"
    lookup_url_kwarg = "id_trabalho"

    def get_queryset(self):
        return Trabalho.objects.filter(
            situacao=Trabalho.Situacao.PUBLICADO
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TrabalhoPublicoDetalheSerializer

        return TrabalhoPublicoSerializer