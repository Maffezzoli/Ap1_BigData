#!/bin/bash
echo "Gerando pacote app.zip para o Elastic Beanstalk..."

# Remove zip antigo se existir
rm -f app.zip

# Compacta os arquivos necessarios
zip -r app.zip catalogo produtos .ebextensions manage.py requirements.txt Procfile

echo "Pacote app.zip gerado com sucesso!"
