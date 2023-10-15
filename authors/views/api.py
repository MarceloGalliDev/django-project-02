from rest_framework.viewsets import ReadOnlyModelViewSet
from ..serializers import AuthorSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action


class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, ]
    
    # aqui passamos o usuario autenticado para dentro do filter
    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(username=self.request.user.username)
        return qs

    # vamos criar uma url para especificar a api
    # quando queremos um unico objeto usamos o self.get_object()
    # como não temos uma pk usamos o get_queryset()
    @action(
        methods=['GET'],
        detail=False,
    )
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(
            instance=obj
        )
        return Response(serializer.data)