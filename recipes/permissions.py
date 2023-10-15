from rest_framework import permissions

# aqui vamos verificar se o author é dono da recipe
class IsOwner(permissions.BasePermission):
    
    # este checa o objeto em si
    # o objeto é vindo do recipe models
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
    
    # este checa coisas aleatoris
    def has_permission(self, request, view):
        return super().has_permission(request, view)