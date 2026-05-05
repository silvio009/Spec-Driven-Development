# Implementation Plan: API de Gestão de Tarefas

**Branch**: `002-task-rest-api` | **Date**: 2026-05-05 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/002-task-rest-api/spec.md`

## Summary

Expor o `TaskService` existente via 4 endpoints HTTP REST, sem modificar a camada de domínio. A camada de API é responsável exclusivamente pela tradução HTTP ↔ domínio: validação de entrada via Pydantic, mapeamento de `ValueError` para respostas de erro com mensagem em português, e serialização das respostas. Documentação interativa gerada automaticamente.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: FastAPI, uvicorn, Pydantic v2 (a adicionar); pytest ≥ 8.0, pytest-cov ≥ 5.0 (existentes)
**Storage**: SQLite via `src/database.py` (existente, sem modificação)
**Testing**: pytest
**Target Platform**: Servidor local / Linux server
**Project Type**: web-service
**Performance Goals**: Padrão para serviço web de uso individual/small team
**Constraints**: `TaskService` e camadas inferiores não devem ser modificados
**Scale/Scope**: CRUD de tarefas, uso pessoal/equipe pequena

## Constitution Check

A constituição do projeto está no formato template (não preenchida). Sem princípios formalizados para verificar. Adotando as regras do `CLAUDE.md`:

- Separação de responsabilidades: camada `api/` apenas traduz HTTP ↔ domínio ✓
- Nenhuma regra de negócio nas rotas ✓
- Testes obrigatórios para toda função de serviço ✓ (as rotas são a interface, não serviço — mas cobertura de integração será provida)
- Nomes de variáveis/funções em inglês, comentários em português ✓

**Resultado**: Sem violações.

## Project Structure

### Documentation (this feature)

```text
specs/002-task-rest-api/
├── plan.md              ← Este arquivo
├── research.md          ← Phase 0: decisões técnicas
├── data-model.md        ← Phase 1: schemas e mapeamento HTTP
├── quickstart.md        ← Phase 1: como rodar
├── contracts/
│   └── task-api.md      ← Phase 1: contrato completo dos 4 endpoints
└── tasks.md             ← Phase 2: gerado por /speckit-tasks
```

### Source Code

```text
src/
├── api/                          ← NOVO
│   ├── __init__.py
│   ├── main.py                   ← App FastAPI + lifespan + exception handlers
│   ├── dependencies.py           ← Factory de TaskService via Depends()
│   ├── routes/
│   │   ├── __init__.py
│   │   └── tasks.py              ← 4 endpoints: POST, GET, PATCH, DELETE
│   └── schemas/
│       ├── __init__.py
│       └── task.py               ← TaskCreateRequest, StatusUpdateRequest,
│                                    TaskResponse, TaskCreateResponse, ErrorResponse
├── models/task.py                ← EXISTENTE — sem modificação
├── repositories/task_repository.py  ← EXISTENTE — sem modificação
├── services/task_service.py      ← EXISTENTE — sem modificação
└── database.py                   ← EXISTENTE — sem modificação

tests/
├── api/                          ← NOVO
│   ├── __init__.py
│   └── test_tasks_routes.py      ← Testes de integração dos 4 endpoints
└── [testes existentes]           ← EXISTENTES — sem modificação
```

**Structure Decision**: Single project com nova camada `src/api/`. Nenhuma nova pasta de nível superior. Testes de integração em `tests/api/` espelham a estrutura de `src/api/`.

## Complexity Tracking

Sem violações — tabela não aplicável.
