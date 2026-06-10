from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from produtos.models import Categoria, Produto

class Command(BaseCommand):
    help = 'Inicializa o banco de dados com dados de teste e cria o superusuário admin'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # 1. Criar Superusuário admin se não existir
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superusuário "admin" criado com sucesso (senha: admin123).'))
        else:
            self.stdout.write(self.style.WARNING('Superusuário "admin" já existe.'))

        # 2. Criar Categorias Iniciais
        cat_eletro, _ = Categoria.objects.get_or_create(
            nome='Eletrônicos',
            defaults={'descricao': 'Dispositivos eletrônicos, computadores e smartphones.'}
        )
        cat_eletrodom, _ = Categoria.objects.get_or_create(
            nome='Eletrodomésticos',
            defaults={'descricao': 'Geladeiras, micro-ondas e utensílios domésticos.'}
        )
        self.stdout.write(self.style.SUCCESS('Categorias criadas ou atualizadas.'))

        # 3. Criar Produtos de Exemplo com especificações JSON
        produtos_data = [
            {
                'nome': 'Notebook Dell Inspiron',
                'descricao': 'Notebook Dell de alta performance ideal para trabalho e estudos.',
                'preco': 4500.00,
                'categoria': cat_eletro,
                'especificacoes': {
                    'marca': 'Dell',
                    'ram_gb': 16,
                    'cor': 'preto',
                    'especificacoes': {
                        'cpu': 'i7',
                        'armazenamento': '512GB SSD'
                    }
                }
            },
            {
                'nome': 'MacBook Air M2',
                'descricao': 'Notebook Apple leve, rápido e com excelente duração de bateria.',
                'preco': 8999.00,
                'categoria': cat_eletro,
                'especificacoes': {
                    'marca': 'Apple',
                    'ram_gb': 8,
                    'cor': 'prata',
                    'especificacoes': {
                        'cpu': 'M2',
                        'armazenamento': '256GB SSD'
                    }
                }
            },
            {
                'nome': 'Smartphone Samsung Galaxy S24',
                'descricao': 'Smartphone topo de linha com IA avançada e câmera de 50MP.',
                'preco': 5200.00,
                'categoria': cat_eletro,
                'especificacoes': {
                    'marca': 'Samsung',
                    'ram_gb': 12,
                    'cor': 'cinza',
                    'especificacoes': {
                        'tela': '6.2 polegadas OLED',
                        'bateria': '4000mAh'
                    }
                }
            },
            {
                'nome': 'Geladeira Frost Free Brastemp',
                'descricao': 'Geladeira Brastemp Duplex Inox com painel eletrônico.',
                'preco': 3800.00,
                'categoria': cat_eletrodom,
                'especificacoes': {
                    'marca': 'Brastemp',
                    'cor': 'inox',
                    'especificacoes': {
                        'capacidade': '400L',
                        'voltagem': '110V'
                    }
                }
            }
        ]

        for p_data in produtos_data:
            produto, created = Produto.objects.get_or_create(
                nome=p_data['nome'],
                defaults=p_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Produto "{produto.nome}" criado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Produto "{produto.nome}" já existe.'))
        
        self.stdout.write(self.style.SUCCESS('Bootstrap concluído com sucesso!'))
