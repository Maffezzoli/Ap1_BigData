# Catalogo de Produtos - Django REST

Projeto Django REST para catalogo de produtos, com suporte a:
- Execucao local com SQLite
- Deploy no Elastic Beanstalk (Python 3.12)
- Banco PostgreSQL no RDS provisionado com Terraform

## Estrutura

- catalogo-produtos: aplicacao Django
- catalogo-produtos/infra/terraform/rds: infraestrutura do RDS via Terraform
- tutorial.md: roteiro base usado no projeto

## Requisitos

- Python 3.12+
- Pip
- (Opcional) Terraform, para criar RDS

## Como rodar localmente (SQLite)

1. Entrar na pasta da aplicacao:

~~~powershell
cd catalogo-produtos
~~~

2. Criar e ativar ambiente virtual:

~~~powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
~~~

3. Instalar dependencias:

~~~powershell
pip install -r requirements.txt
~~~

4. Aplicar migracoes:

~~~powershell
python manage.py migrate
~~~

5. Subir servidor:

~~~powershell
python manage.py runserver
~~~

6. Acessar:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/api/produtos/

## Banco de dados: como o projeto decide entre SQLite e RDS

O arquivo catalogo-produtos/catalogo/settings.py usa esta regra:
- Se USE_RDS=True e RDS_HOSTNAME estiver definido, usa PostgreSQL
- Caso contrario, usa SQLite local (db.sqlite3)

## Variaveis de ambiente para RDS

Defina estas variaveis no ambiente de execucao (exemplo: Elastic Beanstalk):

- USE_RDS=True
- RDS_HOSTNAME=<endpoint do RDS>
- RDS_PORT=5432
- RDS_DB_NAME=catalogodb
- RDS_USERNAME=catalogo_admin
- RDS_PASSWORD=<senha do banco>
- DJANGO_DEBUG=False
- DJANGO_ALLOWED_HOSTS=<seu-dominio-eb>,.elasticbeanstalk.com

## Deploy no Elastic Beanstalk

Arquivos de deploy ja presentes em catalogo-produtos:
- .ebextensions/detection.config
- .ebextensions/django.config
- .elasticbeanstalk/config.yml
- Procfile

Fluxo resumido:

1. Gerar zip com os arquivos na raiz de catalogo-produtos
2. Nao incluir .venv, .git, db.sqlite3, __pycache__, .env
3. Criar/atualizar ambiente EB em Python 3.12
4. Definir variaveis de ambiente no console do EB
5. Aguardar status do ambiente voltar para Ok

## Provisionar RDS com Terraform

Pasta de infraestrutura:
- catalogo-produtos/infra/terraform/rds

1. Entrar na pasta:

~~~powershell
cd catalogo-produtos\infra\terraform\rds
~~~

2. Ajustar terraform.tfvars (regiao, usuario, SG do EB, etc.)

3. Definir senha fora do arquivo (recomendado):

~~~powershell
$env:TF_VAR_db_password="SUA_SENHA_FORTE"
~~~

4. Executar:

~~~powershell
terraform init
terraform plan
terraform apply
~~~

Se terraform nao estiver no PATH, execute pelo caminho completo do executavel.

5. Obter saidas:

~~~powershell
terraform output
~~~

6. Copiar valores para as variaveis de ambiente do Elastic Beanstalk.

## Comandos uteis

Criar superusuario:

~~~powershell
python manage.py createsuperuser
~~~

Checagem do projeto:

~~~powershell
python manage.py check
~~~

## Seguranca

- Nunca versionar arquivos de chave privada (pem, ppk)
- Nunca versionar terraform.tfvars e arquivos tfstate
- Nunca expor Access Key e Secret Key em chat, commit ou screenshot
- Em caso de exposicao, revogar chave imediatamente no IAM

## Parar custos na AWS

- Elastic Beanstalk: Terminate environment
- Terraform RDS: terraform destroy

Observacao: destruir recursos remove infraestrutura. Se precisar preservar dados do banco, ajustar estrategia de snapshot antes do destroy.
