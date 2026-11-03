from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from catalogo.models import Autor, Curso, Orientador, PalavraChave, Trabalho


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ["id", "nome", "sigla"]


class OrientadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientador
        fields = ["id", "nome", "titulacao", "email"]


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ["id", "nome", "email"]


class PalavraChaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalavraChave
        fields = ["id", "termo"]


class TrabalhoGestaoSerializer(serializers.ModelSerializer):
    cadastrado_por = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Trabalho
        fields = [
            "id",
            "titulo",
            "resumo",
            "ano",
            "data_defesa",
            "nota",
            "situacao",
            "arquivo_pdf",
            "curso",
            "orientador",
            "coorientador",
            "autores",
            "palavras_chave",
            "cadastrado_por",
        ]
        # lista vazia chega ao validate_autores, que devolve a mensagem da regra
        extra_kwargs = {"autores": {"allow_empty": True}}
        validators = [
            UniqueTogetherValidator(
                queryset=Trabalho.objects.all(),
                fields=["titulo", "curso", "ano"],
                message="Já existe um trabalho com este título no mesmo curso e ano.",
            )
        ]

    def validate_autores(self, autores):
        # o vínculo M2M só existe depois do save, por isso a contagem é feita aqui
        if not 1 <= len(set(autores)) <= 2:
            raise serializers.ValidationError(
                "Informe no mínimo um e no máximo dois autores distintos."
            )
        return autores

    def validate(self, attrs):
        # em PATCH os campos ausentes vêm da instância
        def atual(campo):
            if campo in attrs:
                return attrs[campo]
            return getattr(self.instance, campo, None)

        if atual("situacao") == Trabalho.Situacao.PUBLICADO:
            faltando = [
                rotulo
                for campo, rotulo in (("nota", "nota"), ("data_defesa", "data de defesa"))
                if atual(campo) is None
            ]
            if faltando:
                raise serializers.ValidationError(
                    {
                        "situacao": "Um trabalho só pode ser publicado com "
                        + " e ".join(faltando)
                        + "."
                    }
                )

        orientador = atual("orientador")
        coorientador = atual("coorientador")
        if coorientador is not None and coorientador == orientador:
            raise serializers.ValidationError(
                {"coorientador": "O coorientador deve ser diferente do orientador."}
            )
        return attrs
