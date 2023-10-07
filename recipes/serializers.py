from rest_framework import serializers
from .models import Category


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    # source usamos para indicar qual o campo que está o model desse public
    public = serializers.BooleanField(source="is_published")
    # aqui estamos unidando dois campos do model
    # estamos referenciando um method
    preparation = serializers.SerializerMethodField(method_name='any_preparation')
    # aqui estamos relacioando os campos mais as string apresentadas
    category_name = serializers.StringRelatedField(
        source='category'
    )
    # aqui estamos fazendo a relação de PrimaryKey
    # obrigatório informar o queryset ligado a PK
    # aqui retornamos o ID
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )
    
    
    # aqui recebemos o obj e trabalhamos com ele
    # aqui o padrão é usar get_{nome.obj} mas com o uso do method_name podemos indicar
    def any_preparation(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"
    