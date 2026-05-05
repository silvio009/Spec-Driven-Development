# Implementation Plan: Gestão de Tarefas

**Branch**: `001-task-management` | **Date**: 2026-05-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-task-management/spec.md`

---

## Summary

Implementar a camada de serviço de gestão de tarefas com regras de negócio completas: criação com validação, listagem com filtros, transição de status unidirecional e exclusão condicional. A implementação segue a separação obrigatória entre camada de serviço (regras de negócio) e camada de dados (persistência), sem expor rotas de API nesta spec.

---

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI (roteamento, fora do escopo desta spec), SQLite (dev), pydantic (validação de dados)
**Storage**: SQLite (dev) — arquivo local via sqlite3 ou SQLAlchemy Core
**Testing**: pytest
**Target Platform**: Servidor local / ambiente de desenvolvimento
**Project Type**: Serviço interno (camada de negócio) — sem API REST nesta spec
**Performance Goals**: Operações de CRUD instantâneas para uso individual/dev (sem SLA de produção definido)
**Constraints**: Regras de negócio aplicadas 100% na camada de serviço; sem lógica de negócio nas rotas
**Scale/Scope**: Single-user dev; sem requisitos de concorrência nesta spec

---

## Constitution Check

*GATE: Verificação antes do Phase 0. Re-verificado após Phase 1.*

> A constituição do projeto (`.specify/memory/constitution.md`) está no formato de template sem princípios ratificados.
> O documento de governança ativo é o **CLAUDE.md**.

### Gates derivados do CLAUDE.md

| Gate | Status | Observação |
|------|--------|------------|
| Type hints em todas as funções | PENDENTE | A ser aplicado na implementação |
| Docstrings em português em todas as funções | PENDENTE | A ser aplicado na implementação |
| Testes obrigatórios para toda função de serviço | PENDENTE | Coberto pelo plano de tasks |
| Separação de regras de negócio da camada de rota | APROVADO | Esta spec cobre apenas a camada de serviço |
| Nomes de variáveis e funções em inglês | PENDENTE | A ser aplicado na implementação |
| Commits em Conventional Commits | N/A | Responsabilidade do desenvolvedor |

**Resultado**: Nenhuma violação detectada no design. Gates de implementação verificados na fase de tasks.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-task-management/
├── plan.md              # Este arquivo (saída do /speckit-plan)
├── research.md          # Saída Phase 0
├── data-model.md        # Saída Phase 1
├── quickstart.md        # Saída Phase 1
├── contracts/           # Saída Phase 1
│   └── task-service.md
└── tasks.md             # Saída Phase 2 (/speckit-tasks — NÃO criado aqui)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py             # Entidade Task: dataclass/Pydantic model + enums
├── services/
│   └── task_service.py     # Regras de negócio: create, list, update_status, delete
├── repositories/
│   └── task_repository.py  # Acesso ao banco: CRUD sem regras de negócio
└── database.py             # Configuração e conexão SQLite

tests/
├── unit/
│   └── test_task_service.py    # Testes das regras de negócio (mock do repositório)
└── integration/
    └── test_task_repository.py # Testes de persistência (banco em memória)
```

**Structure Decision**: Single project (Option 1). Separação explícita em `models/` → `repositories/` → `services/` para garantir que regras de negócio fiquem exclusivamente na camada de serviço, conforme mandatório no CLAUDE.md.

---

## Complexity Tracking

> Nenhuma violação de constituição identificada. Seção não aplicável.
