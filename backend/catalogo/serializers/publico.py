
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