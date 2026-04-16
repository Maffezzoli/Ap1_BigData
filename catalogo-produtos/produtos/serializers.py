from rest_framework import serializers
from .models import Produto, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    produtos_count = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'data_criacao', 'produtos_count']
        read_only_fields = ['data_criacao']

    def get_produtos_count(self, obj):
        return obj.produtos.count()

class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'categoria', 'categoria_nome', 'imagem', 'data_criacao']
        read_only_fields = ['data_criacao']