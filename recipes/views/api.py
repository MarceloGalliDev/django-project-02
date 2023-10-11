from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

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

# ----------------------------------------------------------------
# usando ClassBasedViews
# class RecipeAPIv2List(APIView):
#     def get(self, request):
#         # recipe = Recipe.objects.get_published()[:10]
#         recipe = Recipe.objects.all()
#         serializer = RecipeSerializer(
#             instance=recipe, 
#             many=True,
#             context={'request': request},
#         )
#         return Response(
#             serializer.data
#         )
    
#     def post(self, request):
#         serializer = RecipeSerializer(
#             data=request.data
#         )
#         serializer.is_valid(
#             raise_exception=True
#         )
#         serializer.save()
#         return Response(
#             serializer.data, 
#             status=status.HTTP_201_CREATED
#         )

# class RecipeAPIv2Detail(APIView):
#     def get_recipe(self, pk):
#         recipe = get_object_or_404(
#             Recipe.objects.all(),
#             # Recipe.objects.get_published(),
#             pk=pk
#         )
#         return recipe
        
#     def get(self, request, pk):
#         recipe = self.get_recipe(pk)
#         serializer = RecipeSerializer(
#             instance=recipe, 
#             many=False,
#             context={'request': request},
#         )
#         return Response(
#             serializer.data
#         )
        
#     def patch(self, request, pk):
#         recipe = self.get_recipe(pk)
#         serializer = RecipeSerializer(
#             instance=recipe,
#             data=request.data,
#             many=False,
#             context={'request': request},
#             partial=True,
#         )
#         serializer.is_valid(
#             raise_exception=True
#         )
#         serializer.save()
#         return Response(
#             serializer.data
#         )

#     def delete(self, request, pk):
#         recipe = self.get_recipe(pk)
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# ----------------------------------------------------------------

# Classe de paginação
class RecipeAPIv2Pagination(PageNumberPagination):
    # subscrevendo o método page_size da classe PageNumberPagination
    page_size = 10

# # essa class faz a mesma coisa que a de cima
# class RecipeAPIv2List(ListCreateAPIView):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer
#     pagination_class = PageNumberPagination

# class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeAPIv2Pagination
    
#     # para subscrever os métodos temos que usar o mesmo nome e argumentos
#     # por exemplo partial_update(self, request, *args, **kwargs)
#     # ai o PK do recipe será recebido através de kwargs
#     # pk = kwargs.get('pk')
#     # queryset = self.get_queryset().filter(pk=pk).first()

# essa class faz a mesma coisa que as de cima
class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination

    def get_queryset(self):
        qs = super().get_queryset()
        
        print('Parâmetros', self.kwargs)
        print('Query Parâmetros', self.request.query_params)
        category_id = self.request.query_params.get('category_id', '')
        
        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)
        
        return qs
    

    # estamos subscrevendo o método como exemplo
    # esse método vem dos mixins dentro do ModelViewSet
    # verificar o método
    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')        
        recipe = self.get_queryset().filter(pk=pk).first()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()
        return Response(
            serializer.data
        )

# ----------------------------------------------------------------
# sempre no DRF é necessario uma quyeryset e um serializer

# views Generic
# ClassBasedViews
#   - CreateAPIView = para fazer um post
#   - ListAPIView = para get de listar varios (many)
#   - RetrieveAPIView = para get de um unico list (pk)
#   - DestroyAPIView = delete
#   - UpdateAPIView = Tanto patch quanto put

# Mixins
# usamos para complementar classes

# ViewSet
# usada para junção de classes
# vamos fazer um viewset de um model

# kwargs são parametros dentro dos métodos
# para pegar um método dentro do kwargs usamos:
# qs.filter(pk=self.kwargs.get('pk'))
# print('parametros', self.kwargs)

# as query strings são os parametros vindo da url
# um dicionario com os paramêtros da query