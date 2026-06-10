terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Região AWS para criação dos recursos"
}

variable "projeto_nome" {
  type        = string
  default     = "catalogo-produtos"
  description = "Nome do projeto para prefixo dos recursos"
}

# Gerador de sufixo único para o bucket S3
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Gerador de senha segura para o banco de dados (evita problemas com caracteres especiais)
resource "random_password" "db_password" {
  length  = 16
  special = false
}

# 1. Bucket S3 para Arquivos de Mídia (Produtos)
resource "aws_s3_bucket" "media" {
  bucket        = "${var.projeto_nome}-media-${random_id.bucket_suffix.hex}"
  force_destroy = true # Facilita a destruição após os testes do aluno
}

# Bloqueio de Acesso Público no S3 (Melhor prática moderna da AWS)
# Usaremos URLs pré-assinadas (AWS_QUERYSTRING_AUTH = True) geradas pelo Django
resource "aws_s3_bucket_public_access_block" "media" {
  bucket = aws_s3_bucket.media.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 2. VPC Padrão e Security Group para o RDS
data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "rds_sg" {
  name        = "${var.projeto_nome}-rds-sg"
  description = "Acesso ao banco PostgreSQL do catalogo"
  vpc_id      = data.aws_vpc.default.id

  # Porta do PostgreSQL (5432) liberada para a internet (0.0.0.0/0)
  # para que o aluno possa rodar as migrações de banco da sua própria máquina local.
  ingress {
    description = "Acesso ao PostgreSQL"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

# 3. Instância de Banco de Dados RDS PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier             = "${var.projeto_nome}-db"
  engine                 = "postgres"
  engine_version         = "16"

  instance_class         = "db.t4g.micro" # Econômica e moderna, elegível a Free Tier
  allocated_storage      = 20
  max_allocated_storage  = 100
  db_name                = "catalogodb"
  username               = "postgres"
  password               = random_password.db_password.result
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  publicly_accessible    = true # Importante para rodar makemigrations/migrate do ambiente local
  skip_final_snapshot    = true
}

# OUTPUTS - Configurações e Variáveis prontas para copiar
output "env_variables_eb" {
  description = "Copie estas variáveis nas configurações de ambiente do Elastic Beanstalk"
  value = <<EOT
--------------------------------------------------------------------------------
DB_HOST = ${aws_db_instance.postgres.address}
DB_NAME = ${aws_db_instance.postgres.db_name}
DB_USER = ${aws_db_instance.postgres.username}
DB_PASSWORD = ${random_password.db_password.result}
DB_PORT = 5432
AWS_STORAGE_BUCKET_NAME = ${aws_s3_bucket.media.id}
AWS_S3_REGION_NAME = ${var.aws_region}
USE_S3 = True
--------------------------------------------------------------------------------
EOT
  sensitive = true
}

output "env_variables_local" {
  description = "Comandos para configurar variáveis localmente e rodar migrações para o RDS"
  value = <<EOT
export DB_HOST="${aws_db_instance.postgres.address}"
export DB_NAME="${aws_db_instance.postgres.db_name}"
export DB_USER="${aws_db_instance.postgres.username}"
export DB_PASSWORD="${random_password.db_password.result}"
export DB_PORT="5432"
export AWS_STORAGE_BUCKET_NAME="${aws_s3_bucket.media.id}"
export AWS_S3_REGION_NAME="${var.aws_region}"
export USE_S3="True"
EOT
  sensitive = true
}
