
from rest_framework import serializers

from catalogo.models import Trabalho

class TrabalhoPublicoSerializer(serializers.ModelSerializer):
    curso = serializers.StringRelatedField()
    orientador = serializers.StringRelatedField()
    coorientador = serializers.StringRelatedField()
    autores = serializers.StringRelatedField(many=True)

    class Meta:
        model = Trabalho
        fields = [
            "id",
            "titulo",
            "ano",
            "data_defesa",
            "arquivo_pdf",
            "curso",
            "orientador",
            "coorientador",
            "autores",
        ]
        read_only_fields = fields

from rest_framework import serializers

from catalogo.models import Trabalho

class TrabalhoPublicoDetalheSerializer(serializers.ModelSerializer):
    curso = serializers.StringRelatedField()
    orientador = serializers.StringRelatedField()
    coorientador = serializers.StringRelatedField()
    autores = serializers.StringRelatedField(many=True)
    palavras_chave = serializers.StringRelatedField(many=True)

    class Meta:
        model = Trabalho
        fields = [
            "id",
            "titulo",
            "resumo",
            "ano",
            "data_defesa",
            "arquivo_pdf",
            "curso",
            "orientador",
            "coorientador",
            "autores",
            "palavras_chave",
        ]
        read_only_fields = fields

class OrientadorEstatisticaSerializer(serializers.Serializer):
    nome = serializers.CharField()
    total = serializers.IntegerField()


class EstatisticasSerializer(serializers.Serializer):
    trabalhos_por_ano = serializers.DictField(
        child=serializers.IntegerField()
    )

    trabalhos_por_curso = serializers.DictField(
        child=serializers.IntegerField()
    )

    orientadores_com_mais_trabalhos = OrientadorEstatisticaSerializer(
        many=True
    )