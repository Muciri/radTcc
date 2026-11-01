
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