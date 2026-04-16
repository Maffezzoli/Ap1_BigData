# Catalogo de Produtos - Django REST API

API REST desenvolvida com Django e Django REST Framework para gerenciamento de produtos e categorias, com deploy na AWS Elastic Beanstalk.

## Integrantes do Grupo

- Daniel Maffezzoli

## Link da API Deployada

**URL da API na AWS:** http://catalogo-produtos-env.eba-z8mu8yce.us-east-2.elasticbeanstalk.com/

Endpoints disponiveis:
- `GET /api/categorias/` - Lista todas as categorias
- `POST /api/categorias/` - Cria nova categoria
- `GET /api/categorias/{id}/` - Detalhes de uma categoria
- `PUT /api/categorias/{id}/` - Atualiza categoria
- `DELETE /api/categorias/{id}/` - Remove categoria
- `GET /api/produtos/` - Lista todos os produtos
- `POST /api/produtos/` - Cria novo produto
- `GET /api/produtos/{id}/` - Detalhes de um produto
- `PUT /api/produtos/{id}/` - Atualiza produto
- `DELETE /api/produtos/{id}/` - Remove produto
- `GET /admin/` - Interface administrativa Django

## Descricao do Projeto

Este projeto e uma API REST para gerenciamento de catalogo de produtos, desenvolvida como parte da disciplina de Big Data. O sistema permite:

- **Gerenciamento de Categorias**: Criar, listar, atualizar e deletar categorias de produtos
- **Gerenciamento de Produtos**: CRUD completo de produtos com relacionamento a categorias
- **Interface Administrativa**: Django Admin para gerenciamento via interface web
- **API RESTful**: Endpoints completos seguindo padroes REST
- **Deploy na AWS**: Aplicacao deployada no Elastic Beanstalk

### Alteracoes Realizadas

1. **Nova Classe Categoria**: Adicionada classe `Categoria` com os campos:
   - `nome`: Nome unico da categoria
   - `descricao`: Descricao opcional da categoria
   - `data_criacao`: Data de criacao automatica

2. **Relacionamento**: Produto agora possui relacionamento ForeignKey com Categoria (opcional)

3. **APIs Completas**: Implementados serializers, views e URLs para ambas as classes

4. **Configuracao Simplificada**: Removida infraestrutura Terraform, usando SQLite como banco principal

## Tecnologias Utilizadas

- **Python 3.12**
- **Django 6.0.4**
- **Django REST Framework 3.17.1**
- **SQLite** (banco de dados)
- **Gunicorn** (servidor WSGI)
- **Pillow** (processamento de imagens)
- **AWS Elastic Beanstalk** (deploy)

## Estrutura do Projeto

```
catalogo-produtos/
├── catalogo/                 # Configuracoes do projeto Django
│   ├── settings.py          # Configuracoes principais
│   ├── urls.py              # URLs principais
│   └── wsgi.py              # Configuracao WSGI
├── produtos/                 # App de produtos e categorias
│   ├── models.py            # Modelos Categoria e Produto
│   ├── serializers.py       # Serializers DRF
│   ├── views.py             # ViewSets da API
│   ├── urls.py              # URLs da API
│   ├── admin.py             # Configuracao Django Admin
│   └── migrations/          # Migracoes do banco
├── .ebextensions/           # Configuracoes Elastic Beanstalk
│   ├── django.config        # Comandos de deploy
│   └── detection.config     # Deteccao de plataforma
├── manage.py                # Utilitario Django
├── requirements.txt         # Dependencias Python
├── Procfile                 # Configuracao Gunicorn
└── db.sqlite3              # Banco de dados SQLite
```

## Como Configurar e Executar Localmente

### Pre-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo 1: Clonar o Repositorio

```bash
git clone [URL_DO_REPOSITORIO]
cd Ap1_BigData/catalogo-produtos
```

### Passo 2: Criar Ambiente Virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Passo 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Passo 4: Executar Migracoes

```bash
python manage.py makemigrations
python manage.py migrate
```

### Passo 5: Criar Superusuario (Admin)

```bash
python manage.py createsuperuser
```

Siga as instrucoes para criar usuario, email e senha do administrador.

### Passo 6: Coletar Arquivos Estaticos

```bash
python manage.py collectstatic --noinput
```

### Passo 7: Executar Servidor de Desenvolvimento

```bash
python manage.py runserver
```

### Passo 8: Acessar a Aplicacao

- **API Root**: http://127.0.0.1:8000/api/
- **Categorias**: http://127.0.0.1:8000/api/categorias/
- **Produtos**: http://127.0.0.1:8000/api/produtos/
- **Admin**: http://127.0.0.1:8000/admin/

## Deploy na AWS Elastic Beanstalk

### Pre-requisitos para Deploy

- Conta AWS ativa
- AWS CLI instalado e configurado
- EB CLI instalado (opcional, mas recomendado)

### Passo 1: Preparar Arquivo app.zip

Na pasta `catalogo-produtos`, criar arquivo ZIP com os seguintes arquivos:

```bash
# Incluir:
- catalogo/
- produtos/
- .ebextensions/
- manage.py
- requirements.txt
- Procfile
- db.sqlite3 (opcional, para dados iniciais)

# NAO incluir:
- .venv/
- .git/
- __pycache__/
- *.pyc
- .env
- media/ (se houver uploads locais)
```

**Comando para criar ZIP (Linux/macOS):**
```bash
zip -r app.zip . -x "*.git*" "*__pycache__*" "*.pyc" ".venv/*" "*.env"
```

**Windows (PowerShell):**
```powershell
Compress-Archive -Path * -DestinationPath app.zip -Force
```

### Passo 2: Criar Ambiente no Elastic Beanstalk

1. Acesse o Console AWS
2. Navegue para Elastic Beanstalk
3. Clique em "Create Application"
4. Configure:
   - **Application name**: catalogo-produtos
   - **Platform**: Python
   - **Platform branch**: Python 3.12
   - **Application code**: Upload your code
   - Faca upload do arquivo `app.zip`

### Passo 3: Configurar Variaveis de Ambiente

No console do Elastic Beanstalk, va em Configuration > Software > Environment properties:

```
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.elasticbeanstalk.com
DJANGO_SETTINGS_MODULE=catalogo.settings
```

### Passo 4: Criar Superusuario no Ambiente de Producao

Apos o deploy, conecte-se via SSH ao ambiente EB e execute:

```bash
# Conectar via SSH (usando EB CLI)
eb ssh

# Ou via console AWS > EC2 > Connect

# No servidor, executar:
cd /var/app/current
source /var/app/venv/*/bin/activate
python manage.py createsuperuser
```

**Alternativa: Criar via container_commands**

Adicione ao arquivo `.ebextensions/django.config`:

```yaml
container_commands:
  06_create_superuser:
    command: "echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'senha_forte_aqui')\" | python manage.py shell"
    leader_only: true
```

### Passo 5: Verificar Deploy

1. Aguarde o ambiente ficar com status "Ok" (verde)
2. Acesse a URL fornecida pelo Elastic Beanstalk
3. Teste os endpoints da API
4. Acesse `/admin/` e faca login com o superusuario criado

## Comandos Uteis

### Desenvolvimento Local

```bash
# Criar novas migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Verificar problemas no projeto
python manage.py check

# Executar testes
python manage.py test

# Shell interativo do Django
python manage.py shell
```

### Deploy e Atualização

```bash
# Instalar EB CLI
pip install awsebcli

# Inicializar EB no projeto
eb init

# Criar ambiente
eb create catalogo-produtos-env

# Deploy de atualizações
eb deploy

# Ver logs
eb logs

# Abrir aplicação no navegador
eb open

# SSH no servidor
eb ssh

# Status do ambiente
eb status
```

## Modelos de Dados

### Categoria

```python
class Categoria(models.Model):
    nome = CharField(max_length=100, unique=True)
    descricao = TextField(blank=True)
    data_criacao = DateTimeField(auto_now_add=True)
```

### Produto

```python
class Produto(models.Model):
    nome = CharField(max_length=200)
    descricao = TextField()
    preco = DecimalField(max_digits=10, decimal_places=2)
    categoria = ForeignKey(Categoria, on_delete=SET_NULL, null=True, blank=True)
    imagem = ImageField(upload_to='produtos/', blank=True, null=True)
    data_criacao = DateTimeField(auto_now_add=True)
```

## Seguranca

- SECRET_KEY deve ser alterada em producao
- DEBUG=False em producao
- ALLOWED_HOSTS configurado corretamente
- Nunca versionar credenciais ou chaves privadas
- Usar variaveis de ambiente para dados sensiveis
- Manter dependencias atualizadas

## Documentacao das Etapas Realizadas

### 1. Remocao da Infraestrutura Terraform
- Removido diretorio `infra/terraform/` completo
- Simplificada configuracao para usar apenas SQLite

### 2. Atualizacao do settings.py
- Removida logica condicional de banco de dados (RDS/PostgreSQL)
- Configurado SQLite como banco principal
- Mantidas configuracoes de seguranca e deploy

### 3. Criacao da Classe Categoria
- Implementado modelo `Categoria` em `produtos/models.py`
- Adicionados campos: nome, descricao, data_criacao
- Configuradas Meta options para ordenacao e verbose names

### 4. Relacionamento Produto-Categoria
- Adicionado campo ForeignKey em Produto
- Configurado `on_delete=SET_NULL` para preservar produtos se categoria for deletada
- Adicionado `related_name='produtos'` para acesso reverso

### 5. Implementacao dos Serializers
- Criado `CategoriaSerializer` com campo calculado `produtos_count`
- Atualizado `ProdutoSerializer` com campo `categoria_nome` read-only
- Configurados campos read-only apropriados

### 6. Implementacao das Views
- Criado `CategoriaViewSet` com operacoes CRUD completas
- Mantido `ProdutoViewSet` existente
- Ambos usando `ModelViewSet` do DRF

### 7. Configuracao de URLs
- Registrada rota `/api/categorias/` no router
- Mantida rota `/api/produtos/` existente
- URLs seguindo padrao RESTful

### 8. Configuracao do Django Admin
- Registradas ambas as classes no admin
- Configurados list_display, search_fields, list_filter
- Adicionado autocomplete para categoria em produtos

### 9. Preparacao para Deploy
- Mantidos arquivos `.ebextensions/` para configuracao EB
- Atualizado `django.config` com comandos de migracao
- Configurado Procfile para Gunicorn
- Documentadas instrucoes de criacao de superusuario

## Troubleshooting

### Erro: "No module named 'django'"
```bash
# Certifique-se de que o ambiente virtual esta ativado
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\Activate.ps1  # Windows

# Reinstale as dependencias
pip install -r requirements.txt
```

### Erro: "Database is locked"
```bash
# Certifique-se de que nao ha multiplas instancias rodando
# Reinicie o servidor
```

### Erro no Deploy EB: "502 Bad Gateway"
```bash
# Verifique os logs
eb logs

# Comum: problemas com migracoes ou collectstatic
# Solucao: verificar .ebextensions/django.config
```

## Referencias

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [AWS Elastic Beanstalk Python](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)
- [Deploying Django to Elastic Beanstalk](https://realpython.com/deploying-a-django-app-to-aws-elastic-beanstalk/)

## Licenca

Este projeto foi desenvolvido para fins educacionais como parte da disciplina de Big Data.

---

**Ultima atualizacao:** Abril 2026
