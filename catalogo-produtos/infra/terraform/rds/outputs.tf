output "rds_endpoint" {
  description = "Endpoint do RDS"
  value       = aws_db_instance.postgres.address
}

output "rds_port" {
  description = "Porta do RDS"
  value       = aws_db_instance.postgres.port
}

output "rds_db_name" {
  description = "Nome do banco"
  value       = aws_db_instance.postgres.db_name
}

output "rds_username" {
  description = "Usuario master"
  value       = aws_db_instance.postgres.username
}

output "eb_env_vars" {
  description = "Valores para copiar em Environment properties do Elastic Beanstalk"
  value = {
    USE_RDS      = "True"
    RDS_HOSTNAME = aws_db_instance.postgres.address
    RDS_PORT     = tostring(aws_db_instance.postgres.port)
    RDS_DB_NAME  = aws_db_instance.postgres.db_name
    RDS_USERNAME = aws_db_instance.postgres.username
  }
}
