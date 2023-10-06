from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..models import Recipe
from ..serializers import RecipeSerializer

@api_view(http_method_names=['GET',])
def recipe_api_list(request):
    # estou pegando os dados de recipe
    recipe = Recipe.objects.get_published()[:10]
    # serializando eles para se tornar um arquivo do tipo json
    # quando temos uma queryset igual vindo de uma query temos que usar o many=True
    serializer = RecipeSerializer(instance=recipe, many=True)
    # o serializer.data é um método do serializer para retornar os dados serializados
    return Response(serializer.data)

@api_view(http_method_names=['GET',])
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.filter(pk=pk).)
    serializer = RecipeSerializer(instance=recipe, many=False)
    # o serializer.data é um método do serializer para retornar os dados serializados
    return Response(serializer.data)
    # recipe = Recipe.objects.get_published().filter(pk=pk).first()
    
    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe, many=False)
    #     return Response(serializer.data)
    # else:
    #     return Response({
    #         "detail": "teste"
    #     }, status=status.HTTP_418_IM_A_TEAPOT)