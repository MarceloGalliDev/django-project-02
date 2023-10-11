from django.urls import path, include
from recipes import views
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'recipes'

recipe_api_v2_router = SimpleRouter(
    # isso indica que teremos uma '/' no final das urls
    trailing_slash=True
)

recipe_api_v2_router.register(
    prefix='recipes/api/v2',
    viewset=views.RecipeAPIv2ViewSet,
    # esse aqui é o app_name
    basename='recipes-api',
)

# 1 forma
# urls para api diretas
# urlpatterns = recipe_api_v2_router.urls

# 2 forma
# concatenando url patterns, vai no final das urls
# urlpatterns += recipe_api_v2_router.url

urlpatterns = [
    path(
        '',
        views.RecipeListViewHome.as_view(),
        name="home"
    ),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(),
        name="search"
    ),
    path(
        'recipes/tags/<slug:slug>/',
        views.RecipeListViewTag.as_view(),
        name="tag"
    ),
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(),
        name="category"
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetail.as_view(),
        name="recipe"
    ),
    path(
        'recipes/api/v1/',
        views.RecipeListViewHomeApi.as_view(),
        name="recipes_api_v1",
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailAPI.as_view(),
        name="recipes_api_v1_detail",
    ),
    path(
        'recipes/theory/',
        views.theory,
        name='theory',
    ),
    # path(
    #     "recipes/api/v2/",
    #     views.RecipeAPIv2ViewSet.as_view({
    #         'get': 'list',
    #         'post': 'create',
    #     }),
    #     name='recipe_api_v2'
    # ),
    # path(
    #     "recipes/api/v2/<int:pk>/",
    #     views.RecipeAPIv2ViewSet.as_view({
    #         'get': 'retrieve',
    #         'patch': 'partial_update',
    #         'delete': 'destroy',
    #     }),
    #     name='recipe_api_v2_detail'
    # ),
    path(
        "recipes/api/v2/tag/<int:pk>/",
        views.tag_api_detail,
        name='recipes_api_v2_tag'
    ),
    
    # token JWT
    path(
        'recipes/api/token/', 
        TokenObtainPairView.as_view(), 
        name='token_obtain_pair'
    ),
    path(
        'recipes/api/token/refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh'
    ),
    path(
        'recipes/api/token/verify/', 
        TokenVerifyView.as_view(), 
        name='token_verify'
    ),
    
    # router
    path('', include(recipe_api_v2_router.urls)),
]

# necessario fazer a indicação do método para router do DRF
# o as_view() do DRF temos os: list, create, retrieve, update ...
# router cria rotas para list, create, retrieve, update e delete automaticamente