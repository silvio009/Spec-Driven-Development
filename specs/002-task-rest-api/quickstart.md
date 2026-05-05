# Quickstart: API de Gestão de Tarefas

**Feature**: 002-task-rest-api
**Date**: 2026-05-05

---

## Pré-requisitos

- Python 3.12+
- Ambiente virtual ativo (`venv/` ou `.venv/`)

## Instalação das dependências novas

```bash
pip install fastapi uvicorn
```

> Adicionar ao `requirements.txt` após aprovação.

## Iniciar o servidor

```bash
uvicorn src.api.main:app --reload
```

Servidor disponível em: `http://localhost:8000`
Documentação interativa: `http://localhost:8000/docs`

## Exemplos rápidos

**Criar uma tarefa:**
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Revisar documentação", "priority": "alta"}'
```

**Listar tarefas pendentes:**
```bash
curl "http://localhost:8000/tasks?status=pendente"
```

**Avançar status:**
```bash
curl -X PATCH http://localhost:8000/tasks/1/status \
  -H "Content-Type: application/json" \
  -d '{"new_status": "em_andamento"}'
```

**Deletar tarefa:**
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Executar testes

```bash
pytest tests/ -v
```
