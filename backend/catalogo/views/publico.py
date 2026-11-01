from rest_framework.decorators import (api_view, permission_classes, authentication_classes)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from catalogo.models import Trabalho
from catalogo.serializers.publico import TrabalhoPublicoSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def listar_trabalhos_publicos(request, **kwargs):
    trabalhos = Trabalho.objects.filter(situacao = Trabalho.Situacao.PUBLICADO)
    serializer = TrabalhoPublicoSerializer(trabalhos, many=True)

    return Response(serializer.data)