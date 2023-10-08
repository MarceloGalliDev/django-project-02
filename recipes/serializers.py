from collections import defaultdict
from rest_framework import serializers
from .models import Category
from django.contrib.auth.models import User
from tag.models import Tag
from  authors.validators import AuthorRecipeValidator


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField()

# # ambos os casos são iguais
# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         # a ordem aqui importa, será mostrada la na views
#         fields = ['id', 'name', 'slug']

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
    
    id = serializers.IntegerField(
        read_only=True,
    )
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    # source usamos para indicar qual o campo que está o model desse public
    public = serializers.BooleanField(
        source="is_published",
        read_only=True,
    )
    # aqui estamos unidando dois campos do model
    # estamos referenciando um method
    preparation = serializers.SerializerMethodField(
        method_name='any_preparation',
        read_only=True,
    )
    # aqui estamos relacioando os campos mais as string apresentadas
    category = serializers.StringRelatedField(
        read_only=True,
    )
    # aqui estamos fazendo a relação de PrimaryKey
    # obrigatório informar o queryset ligado a PK
    # aqui retornamos o ID
    author = serializers.PrimaryKeyRelatedField(
        # queryset=User.objects.all(),
        read_only=True,
    )
    # aqui estamos fazendo a relação de PrimaryKey
    # estamos relacionando ManyToMany, por isso usamos o many
    tags = serializers.PrimaryKeyRelatedField(
        # queryset=Tag.objects.all(),
        many=True,
        read_only=True,
    )
    # aqui usamos uma classe retratando as tags dentro do outro model
    tag_objects = TagSerializer(
        many=True,
        source='tags',
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        # queryset=Tag.objects.all(),
        view_name='recipes:recipes_api_v2_tag',
        # # aqui se eu estiver com read_only=True, eu tenho que retirar queryset
        read_only=True,
    )
    
    
    # aqui recebemos o obj e trabalhamos com ele
    # aqui o padrão é usar get_{nome.obj} mas com o uso do method_name podemos indicar
    def any_preparation(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"

    # usamos para quando um campo depende de outro, ou validação de dois campos ou mais
    def validate(self, attrs):
        # attrs são os dados recebidos
        
        # aqui dentro do validate temos acesso aos dados assim:
        # self.initial_data() = dados iniciais que vem do formulario
        # self.data() = dados ja salvos ou recebidos do cliente
        # self.validated_data() = dados depois de validados
        
        super_validate = super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs, 
            ErrorClass=serializers.ValidationError
        )
        
        # title = attrs.get("title")
        # description = attrs.get("description")
        
        # if title == description:
        #     raise serializers.ValidationError(
        #         {
        #             "title": ["Posso", "ter", "mais de um erro"],
        #             "description": ["Posso", "ter", "mais de um erro"],
        #         }
        #     )
            
        return super_validate



    # # usado para um campo especifico
    # def validate_title(self, value):
    #     title = value
        
    #     if len(title) < 5:
    #         raise serializers.ValidationError("Must have at least 5 char")
    #     return title


# podemos subscrever alguns métodos de validação
# validate() e também o validate_{nome_do_campo}()
# o primeiro a retornar é o validate_campo e depois o validate