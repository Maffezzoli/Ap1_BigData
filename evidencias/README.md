# Pasta de Evidências (Prints - AP2)

Esta pasta deve conter os prints de tela (ou GIFs) solicitados pelas instruções da disciplina para a entrega da AP2.

## Lista de Prints Obrigatórios

1.  **console_rds.png**
    *   *O que printar:* Console da AWS RDS mostrando a instância PostgreSQL ativa (`catalogo-produtos-db`).
2.  **console_s3.png**
    *   *O que printar:* Console da AWS S3 mostrando os arquivos de mídia (imagens dos produtos) salvos dentro do bucket criado.
3.  **requisicao_api_midia.png**
    *   *O que printar:* Requisição HTTP (feita via Postman, Insomnia ou similar) criando ou atualizando um produto enviando um arquivo de imagem (mídia) e obtendo resposta de sucesso.
4.  **django_admin.png**
    *   *O que printar:* Tela da interface administrativa do Django (`/admin/`) logado com o usuário administrador (`admin`).

## Lista de Prints da Extensão Opcional (JSONB - Bônus)

Como implementamos as consultas JSONB do PostgreSQL com sucesso no projeto, você deve incluir os seguintes prints para garantir os pontos de bônus:

5.  **json_registro_salvo.png**
    *   *O que printar:* Registro de produto salvo e exibido na API ou no banco contendo o campo `especificacoes` preenchido com o objeto JSON.
6.  **consulta_json_1.png**
    *   *O que printar:* Consulta na API filtrando por marca (ex: `GET /api/produtos/?marca=Dell`).
7.  **consulta_json_2.png**
    *   *O que printar:* Consulta na API filtrando por memória RAM (ex: `GET /api/produtos/?ram_gb=16`) ou filtro combinado (ex: `GET /api/produtos/?categoria=1&marca=Apple`).
