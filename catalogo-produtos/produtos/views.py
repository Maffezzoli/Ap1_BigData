from rest_framework import viewsets
from .models import Produto, Categoria, Pedido
from .serializers import ProdutoSerializer, CategoriaSerializer, PedidoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro relacional: categoria
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
            
        # Filtro no JSONField: marca
        marca = self.request.query_params.get('marca', None)
        if marca:
            queryset = queryset.filter(especificacoes__marca__iexact=marca)
            
        # Filtro no JSONField: ram_gb (suporta número ou texto)
        ram_gb = self.request.query_params.get('ram_gb', None)
        if ram_gb:
            try:
                queryset = queryset.filter(especificacoes__ram_gb=int(ram_gb))
            except ValueError:
                queryset = queryset.filter(especificacoes__ram_gb=ram_gb)
                
        # Filtro no JSONField: cor
        cor = self.request.query_params.get('cor', None)
        if cor:
            queryset = queryset.filter(especificacoes__cor__iexact=cor)
            
        return queryset


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer