from django.urls import include, path
from .views import ProdutoViewSet, CategoriaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'produtos', ProdutoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]