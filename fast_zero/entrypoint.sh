#!/bin/sh

# Faz as migrações
poetry run alembic upgrade head

# Executa a aplicação
poetry run uvicorn --host 0.0.0.0 fast_zero.app:app