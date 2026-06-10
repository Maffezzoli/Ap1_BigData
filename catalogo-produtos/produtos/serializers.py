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
        fields = ['id', 'nome', 'descricao', 'preco', 'categoria', 'categoria_nome', 'imagem', 'especificacoes', 'data_criacao']
        read_only_fields = ['data_criacao']


from .models import Pedido, ItemPedido

class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    preco_unitario = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario', 'subtotal']


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente_nome', 'cliente_email', 'status', 'itens', 'total', 'data_criacao', 'data_atualizacao']
        read_only_fields = ['data_criacao', 'data_atualizacao']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        for item_data in itens_data:
            produto = item_data['produto']
            preco_unitario = item_data.get('preco_unitario', produto.preco)
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=item_data.get('quantidade', 1),
                preco_unitario=preco_unitario
            )
        return pedido

    def update(self, instance, validated_data):
        itens_data = validated_data.pop('itens', None)
        
        instance.cliente_nome = validated_data.get('cliente_nome', instance.cliente_nome)
        instance.cliente_email = validated_data.get('cliente_email', instance.cliente_email)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if itens_data is not None:
            instance.itens.all().delete()
            for item_data in itens_data:
                produto = item_data['produto']
                preco_unitario = item_data.get('preco_unitario', produto.preco)
                ItemPedido.objects.create(
                    pedido=instance,
                    produto=produto,
                    quantidade=item_data.get('quantidade', 1),
                    preco_unitario=preco_unitario
                )

        return instance