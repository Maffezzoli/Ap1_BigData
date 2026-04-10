# Terraform - RDS para catalogo-produtos

Este diretório cria o RDS PostgreSQL para substituir o SQLite da Parte 5 do tutorial.

## 1) Pre-requisitos

- Terraform >= 1.6
- AWS CLI autenticado (`aws configure`) com permissao de criar RDS, SG e subnet group

## 2) Como aplicar

1. Ajuste o arquivo `terraform.tfvars` com os valores corretos.
2. Garanta que `aws_region` seja a mesma regiao do ambiente Elastic Beanstalk.
3. Em contas com restricao de backup, use `backup_retention_period = 0`.
4. No terminal, rode:

~~~bash
terraform init
terraform plan
terraform apply
~~~

## 3) Pegar valores para o Elastic Beanstalk

Após o apply, rode:

~~~bash
terraform output
~~~

Use estes valores em Elastic Beanstalk > Configuration > Environment properties:

- USE_RDS = True
- RDS_HOSTNAME = valor de `rds_endpoint`
- RDS_PORT = valor de `rds_port`
- RDS_DB_NAME = valor de `rds_db_name`
- RDS_USERNAME = valor de `rds_username`
- RDS_PASSWORD = a senha definida no `terraform.tfvars`

## 4) Migrar aplicação

Depois de salvar as variáveis no EB:

1. Reimplante a aplicação (ou Restart app server).
2. Execute migrações no ambiente (via EB deploy, container command, ou acesso SSH):

~~~bash
python manage.py migrate --noinput
~~~

## 5) Destruir recursos

Para parar cobrança do RDS:

~~~bash
terraform destroy
~~~

Se `deletion_protection = true`, ajuste para false antes do destroy.
