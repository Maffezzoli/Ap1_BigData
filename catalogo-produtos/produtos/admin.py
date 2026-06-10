from django.contrib import admin
from .models import Categoria, Produto, Pedido, ItemPedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'data_criacao']
    search_fields = ['nome', 'descricao']
    list_filter = ['data_criacao']
    ordering = ['nome']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'especificacoes', 'data_criacao']
    search_fields = ['nome', 'descricao']
    list_filter = ['categoria', 'data_criacao']
    ordering = ['-data_criacao']
    autocomplete_fields = ['categoria']

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente_nome', 'cliente_email', 'status', 'total', 'data_criacao']
    search_fields = ['cliente_nome', 'cliente_email']
    list_filter = ['status', 'data_criacao']
    inlines = [ItemPedidoInline]

