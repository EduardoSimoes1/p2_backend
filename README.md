# API de Gerenciamento de Produtos - Atividade Avaliativa

Este projeto implementa uma API REST funcional utilizando FastAPI e SQLAlchemy, integrada a uma suíte de testes automatizados com Pytest executados contra um banco de dados PostgreSQL real via Docker.

## Como subir o banco de testes

Para rodar os testes, precisamos subir o container exclusivo de testes (configurado na porta `5433`). Certifique-se de que o Docker está rodando e execute:

```bash
docker-compose up -d db_test