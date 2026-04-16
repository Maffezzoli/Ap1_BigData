from django.contrib import admin
from .models import Categoria, Produto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'data_criacao']
    search_fields = ['nome', 'descricao']
    list_filter = ['data_criacao']
    ordering = ['nome']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'data_criacao']
    search_fields = ['nome', 'descricao']
    list_filter = ['categoria', 'data_criacao']
    ordering = ['-data_criacao']
    autocomplete_fields = ['categoria']
