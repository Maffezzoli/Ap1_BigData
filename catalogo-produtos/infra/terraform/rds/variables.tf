variable "aws_region" {
  description = "Regiao AWS para os recursos"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Prefixo para nomear recursos"
  type        = string
  default     = "catalogo-produtos"
}

variable "vpc_id" {
  description = "VPC alvo. Se vazio, usa a VPC default"
  type        = string
  default     = ""
}

variable "subnet_ids" {
  description = "Subnets para o RDS. Se vazio, usa subnets da VPC selecionada"
  type        = list(string)
  default     = []
}

variable "db_name" {
  description = "Nome do banco PostgreSQL"
  type        = string
  default     = "catalogodb"
}

variable "db_username" {
  description = "Usuario master do banco"
  type        = string
  default     = "catalogo_admin"
}

variable "db_password" {
  description = "Senha do usuario master do banco"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "Classe da instancia RDS"
  type        = string
  default     = "db.t3.micro"
}

variable "allocated_storage" {
  description = "Tamanho inicial de armazenamento (GB)"
  type        = number
  default     = 20
}

variable "publicly_accessible" {
  description = "Se true, RDS pode ter endpoint publico"
  type        = bool
  default     = false
}

variable "eb_security_group_id" {
  description = "Security Group do Elastic Beanstalk para liberar acesso ao banco"
  type        = string
  default     = ""
}

variable "allowed_cidr_blocks" {
  description = "CIDRs autorizados a conectar no PostgreSQL (use apenas se nao usar SG do EB)"
  type        = list(string)
  default     = []

  validation {
    condition     = length(var.allowed_cidr_blocks) > 0 || var.eb_security_group_id != ""
    error_message = "Informe eb_security_group_id ou pelo menos um CIDR em allowed_cidr_blocks."
  }
}

variable "skip_final_snapshot" {
  description = "Se true, nao gera snapshot final ao destruir"
  type        = bool
  default     = true
}

variable "deletion_protection" {
  description = "Protecao contra delecao acidental"
  type        = bool
  default     = false
}

variable "backup_retention_period" {
  description = "Dias de retencao de backup automatico do RDS"
  type        = number
  default     = 0
}
