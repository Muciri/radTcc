from django.db import IntegrityError
from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.exceptions import APIException, Throttled
from rest_framework.response import Response
from rest_framework.views import exception_handler


class Conflito(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "A operação conflita com o estado atual dos dados."
    default_code = "conflito"


def tratar_excecao(exc, context):
    if isinstance(exc, ProtectedError):
        detalhe = (
            f"Não é possível remover: {len(exc.protected_objects)} "
            "trabalho(s) ainda dependem deste registro."
        )
        return Response({"detail": detalhe}, status=status.HTTP_409_CONFLICT)
    if isinstance(exc, IntegrityError):
        return Response(
            {"detail": "A operação viola uma restrição de integridade dos dados."},
            status=status.HTTP_409_CONFLICT,
        )
    resposta = exception_handler(exc, context)
    if isinstance(exc, Throttled) and resposta is not None:
        # o cabeçalho Retry-After já foi preenchido pelo handler padrão
        espera = int(exc.wait) if exc.wait else 60
        resposta.data = {
            "detail": f"Limite de requisições excedido. Tente novamente em {espera} segundos."
        }
    return resposta
