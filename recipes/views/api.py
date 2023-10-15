from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..permissions import IsOwner
from django.shortcuts import get_object_or_404
from tag.models import Tag
from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer
from rest_framework import status


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 2


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    http_method_names = ['GET', 'OPTIONS', 'HEAD', 'POST', 'PATCH', 'DELETE']

    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["example"] = 'this is in context now'
        return context

    # vamos subscrever o get_object()
    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk
        )
        
        # esse método é uma subscrição
        # para garantir que quando buscarmos uma recipe, vamos checar as permissoes de objetos
        # a checagem é vinda do método has_object_permission()
        self.check_object_permissions(
            self.request,
            obj
        )
        
        return obj
    
    # aqui vamos subscrever o método get_permissions()
    # para que não seja necessario estar logado para ler uma recipe
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    # vamos subscrever o metodo create para não deixar sem um author a recipe
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        recipe = self.get_object()
        # recipe = self.get_queryset().filter(pk=pk).first()

        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)


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

# para capturar os métodos usamos request.method
# para capturar os dados da requisição usamos request.data
# o erro retornado é baseado nos models e os campos situados no serializador
# no método validate() temos acesso ao self.instance

# para subscrever os métodos temos que usar o mesmo nome e argumentos
#     # por exemplo partial_update(self, request, *args, **kwargs)
#     # ai o PK do recipe será recebido através de kwargs
#     # pk = kwargs.get('pk')
#     # queryset = self.get_queryset().filter(pk=pk).first()

# a permissão será personalizada
# pois para deletar ou criar tem que ser o dono da recipe e estar autenticado

# verificar o browsable api do django verificar documentação
