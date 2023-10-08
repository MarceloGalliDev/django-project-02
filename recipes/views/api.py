from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer
from tag.models import Tag

@api_view(http_method_names=['GET', 'POST'])
def recipe_api_list(request):
    if request.method == 'GET':
        # estou pegando os dados de recipe
        # recipe = Recipe.objects.get_published()[:10]
        recipe = Recipe.objects.all()
        # serializando eles para se tornar um arquivo do tipo json
        # quando temos uma queryset igual vindo de uma query temos que usar o many=True
        # estamos passando um context para poder acessar links nas apis
        serializer = RecipeSerializer(
            instance=recipe, 
            many=True,
            context={'request': request},
        )
        # o serializer.data é um método do serializer para retornar os dados serializados
        return Response(serializer.data)
    elif request.method == 'POST':
        # recebemos os dados vindo do POST
        # serializamos e validamos
        serializer = RecipeSerializer(data=request.data)
        # método simplificado para is_valid()
        serializer.is_valid(raise_exception=True)
        # o método save comporta kwargs caso necessario
        serializer.save()
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )
        
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(
        #         serializer.validated_data, 
        #         status=status.HTTP_201_CREATED
        #     )
        # return Response(
        #     serializer.errors,
        #     status=status.HTTP_400_BAD_REQUEST
        # )

@api_view(http_method_names=['GET', 'PATCH', 'DELETE'])
def recipe_api_detail(request, pk):
    # aqui já selecionamos a PK desejada, caso != já encerra aqui
    # recipe = Recipe.objects.get_published().filter(pk=pk).first()
    recipe = get_object_or_404(
        Recipe.objects.all(),
        # Recipe.objects.get_published(),
        pk=pk
    )
    if request.method == 'GET':
        serializer = RecipeSerializer(
            instance=recipe, 
            many=False,
            context={'request': request},
        )
        # o serializer.data é um método do serializer para retornar os dados serializados
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = RecipeSerializer(
            # aqui eu leio e insiro dados
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            # necessario informar que é uma atualização parcial
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data
        )
    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe, many=False)
    #     return Response(serializer.data)
    # else:
    #     return Response({
    #         "detail": "teste"
    #     }, status=status.HTTP_418_IM_A_TEAPOT)
    
@api_view(http_method_names=['GET',])
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(), 
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request}
    )
    return Response(serializer.data)

# para capturar os métodos usamos request.method
# para capturar os dados da requisição usamos request.data
# o erro retornado é baseado nos models e os campos situados no serializador
# no método validate() temos acesso ao self.instance