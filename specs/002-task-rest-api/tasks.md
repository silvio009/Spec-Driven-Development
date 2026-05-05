# Tasks: API de Gestão de Tarefas

**Input**: Design documents from `specs/002-task-rest-api/`
**Prerequisites**: plan.md ✓ spec.md ✓ research.md ✓ data-model.md ✓ contracts/task-api.md ✓

**Tests**: Testes de integração incluídos — plan.md define `tests/api/test_tasks_routes.py` como entregável.

**Organization**: Tasks agrupadas por user story para entrega incremental e teste independente.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Pode rodar em paralelo (arquivos diferentes, sem dependências pendentes)
- **[Story]**: User story correspondente da spec.md (US1–US4)
- Caminhos exatos de arquivo incluídos em todas as tasks

---

## Phase 1: Setup (Estrutura inicial)

**Purpose**: Criar a estrutura de diretórios e declarar dependências novas

- [x] T001 Create directory structure: `src/api/__init__.py`, `src/api/routes/__init__.py`, `src/api/schemas/__init__.py`
- [x] T002 [P] Add `fastapi>=0.100` and `uvicorn` to `requirements.txt` and install in venv
- [x] T003 [P] Create `tests/api/__init__.py` to register test module

---

## Phase 2: Foundational (Pré-requisitos bloqueantes)

**Purpose**: Schemas, injeção de dependência e app FastAPI — DEVEM estar prontos antes de qualquer endpoint

**⚠️ CRÍTICO**: Nenhuma user story pode ser implementada antes desta fase estar completa

- [x] T004 Create Pydantic schemas in `src/api/schemas/task.py`: `TaskCreateRequest`, `StatusUpdateRequest`, `TaskResponse`, `TaskCreateResponse` (with `duplicate_warning`), `ErrorResponse`
- [x] T005 [P] Create dependency factory in `src/api/dependencies.py`: `get_task_service()` opens SQLite connection to `tasks.db`, runs `create_schema`, builds `TaskRepository` and `TaskService`, yields service, closes connection on teardown
- [x] T006 Create FastAPI app in `src/api/main.py`: `lifespan` context manager (open DB, create schema, close on shutdown); global exception handler (`ValueError` with "não encontrada" → HTTP 404, other `ValueError` → HTTP 422); include router from `src/api/routes/tasks.py`; set `docs_url="/docs"`
- [x] T007 [P] Create `tests/api/conftest.py`: `TestClient` fixture with in-memory SQLite (`":memory:"`), override `get_task_service` dependency, run `create_schema` on startup

**Checkpoint**: `uvicorn src.api.main:app --reload` sobe sem erro e `/docs` está acessível

---

## Phase 3: User Story 1 - Registrar Nova Tarefa (Priority: P1) 🎯 MVP

**Goal**: Cliente externo consegue criar tarefa via `POST /tasks` e receber confirmação com dados completos

**Independent Test**: `POST /tasks` com `{"title": "Minha tarefa"}` retorna HTTP 201 com `id`, `status: "pendente"` e `duplicate_warning: false`

### Implementação

- [x] T008 [US1] Implement `POST /tasks` in `src/api/routes/tasks.py`: receive `TaskCreateRequest`, call `service.create_task(title, description, deadline, priority)`, return HTTP 201 with `TaskCreateResponse` (includes `duplicate_warning`)

### Testes de integração

- [x] T009 [US1] Write tests for `POST /tasks` in `tests/api/test_tasks_routes.py`:
  - Valid payload → 201 + TaskCreateResponse with `status="pendente"`
  - Title with 2 chars → 422 + `detail` in Portuguese
  - Past deadline → 422 + `"Prazo não pode ser data passada"`
  - Title > 100 chars → 422
  - Malformed body (missing `title`) → 422
  - Duplicate title same day → 201 + `duplicate_warning=true`

**Checkpoint**: `pytest tests/api/test_tasks_routes.py -k "post"` passa com 100%

---

## Phase 4: User Story 2 - Consultar e Filtrar Tarefas (Priority: P2)

**Goal**: Cliente externo consegue listar tarefas com filtro por status e/ou prioridade via `GET /tasks`

**Independent Test**: `GET /tasks` retorna HTTP 200 com lista (incluindo lista vazia); `GET /tasks?status=pendente` retorna apenas tarefas pendentes

### Implementação

- [x] T010 [US2] Implement `GET /tasks` in `src/api/routes/tasks.py`: optional query params `status: TaskStatus | None` and `priority: Priority | None` (Pydantic enum validation → 422 automático), call `service.list_tasks(status, priority)`, return HTTP 200 with `list[TaskResponse]`

### Testes de integração

- [x] T011 [US2] Write tests for `GET /tasks` in `tests/api/test_tasks_routes.py`:
  - No tasks → 200 + `[]`
  - Filter by `status=pendente` → returns only pending tasks
  - Filter by `priority=alta` → returns only high-priority tasks
  - Combined filters `status=pendente&priority=alta` → intersection
  - Invalid status value → 422

**Checkpoint**: `pytest tests/api/test_tasks_routes.py -k "get"` passa com 100%

---

## Phase 5: User Story 3 - Avançar Status de Tarefa (Priority: P3)

**Goal**: Cliente externo consegue avançar status de uma tarefa via `PATCH /tasks/{id}/status`, respeitando o fluxo `pendente → em_andamento → concluida`

**Independent Test**: Criar tarefa via `POST /tasks`, depois `PATCH /tasks/1/status` com `{"new_status": "em_andamento"}` retorna HTTP 200 com `status: "em_andamento"`

### Implementação

- [x] T012 [US3] Implement `PATCH /tasks/{id}/status` in `src/api/routes/tasks.py`: receive `task_id: int` path param and `StatusUpdateRequest` body, call `service.update_task_status(task_id, new_status)`, return HTTP 200 with `TaskResponse`; `ValueError` "não encontrada" → 404 (handled by global exception handler); other `ValueError` → 422

### Testes de integração

- [x] T013 [US3] Write tests for `PATCH /tasks/{id}/status` in `tests/api/test_tasks_routes.py`:
  - `pendente` → `em_andamento` → 200 with updated status
  - `em_andamento` → `concluida` → 200
  - Non-existent ID → 404
  - Task already `concluida` → 422 + `"Tarefa concluída não pode ser editada."`
  - Invalid transition (e.g. `pendente` → `concluida` directly) → 422
  - Invalid `new_status` value → 422

**Checkpoint**: `pytest tests/api/test_tasks_routes.py -k "patch"` passa com 100%

---

## Phase 6: User Story 4 - Remover Tarefa (Priority: P4)

**Goal**: Cliente externo consegue remover tarefa pendente via `DELETE /tasks/{id}`, com proteção de tarefas em andamento e concluídas

**Independent Test**: Criar tarefa via `POST /tasks`, depois `DELETE /tasks/1` retorna HTTP 204 sem corpo

### Implementação

- [x] T014 [US4] Implement `DELETE /tasks/{id}` in `src/api/routes/tasks.py`: receive `task_id: int` path param, call `service.delete_task(task_id)`, return HTTP 204 (no body); `ValueError` "não encontrada" → 404; other `ValueError` → 422

### Testes de integração

- [x] T015 [US4] Write tests for `DELETE /tasks/{id}` in `tests/api/test_tasks_routes.py`:
  - Pending task → 204 (no body)
  - Non-existent ID → 404
  - In-progress task → 422 + `"Não é possível deletar tarefa em andamento."`
  - Completed task → 422

**Checkpoint**: `pytest tests/api/test_tasks_routes.py` passa com 100% (todos os 4 endpoints cobertos)

---

## Phase 7: Polish & Cross-Cutting

**Purpose**: Validação final, ajustes e documentação

- [x] T016 [P] Verify `/docs` endpoint: start server with `uvicorn src.api.main:app --reload`, open `http://localhost:8000/docs`, confirm all 4 endpoints appear with correct schemas and examples
- [x] T017 Run quickstart.md validation: execute all `curl` examples from `specs/002-task-rest-api/quickstart.md` and verify expected responses
- [x] T018 [P] Run full test suite `pytest tests/ -v --cov=src` and confirm no regressions in existing tests from `001-task-management`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sem dependências — pode iniciar imediatamente
- **Foundational (Phase 2)**: Depende da conclusão do Setup — **BLOQUEIA todas as user stories**
- **User Stories (Phases 3–6)**: Todas dependem do Foundational; podem ser executadas sequencialmente em ordem de prioridade
- **Polish (Phase 7)**: Depende de todas as user stories desejadas estarem completas

### User Story Dependencies

- **US1 (P1)**: Inicia após Foundational — sem dependência de outras stories
- **US2 (P2)**: Inicia após Foundational — independente de US1 (mesmo endpoint `GET /tasks`, arquivo diferente do POST)
- **US3 (P3)**: Inicia após Foundational — independente de US1/US2
- **US4 (P4)**: Inicia após Foundational — independente das demais

> **Nota**: US2, US3 e US4 adicionam endpoints ao mesmo arquivo `src/api/routes/tasks.py`. Para evitar conflito de edição simultânea, recomenda-se execução sequencial (P1 → P2 → P3 → P4), mesmo que logicamente independentes.

### Within Each User Story

- Implementação antes dos testes de integração (sem TDD explicitamente solicitado)
- Endpoint implementado → testes escritos → checkpoint validado → próxima story

### Parallel Opportunities

- T002, T003 (Phase 1): paralelas entre si
- T005, T007 (Phase 2): paralelas entre si e com T004
- T016, T018 (Phase 7): paralelas entre si

---

## Parallel Example: Foundational (Phase 2)

```
Agente A: T004 — src/api/schemas/task.py (schemas Pydantic)
Agente B: T005 — src/api/dependencies.py (factory get_task_service)
Agente C: T007 — tests/api/conftest.py (fixture TestClient)

→ Todos concluem → Agente único: T006 — src/api/main.py (app + handlers + include router)
```

---

## Implementation Strategy

### MVP (User Story 1 apenas)

1. Concluir Phase 1: Setup
2. Concluir Phase 2: Foundational (**crítico — bloqueia tudo**)
3. Concluir Phase 3: US1 — `POST /tasks`
4. **PARAR e VALIDAR**: `POST /tasks` funciona de ponta a ponta
5. Demonstrar/validar com o usuário antes de continuar

### Entrega Incremental

1. Setup + Foundational → servidor sobe, `/docs` acessível
2. US1 → `POST /tasks` funcionando → MVP!
3. US2 → `GET /tasks` com filtros → Consulta disponível
4. US3 → `PATCH /tasks/{id}/status` → Ciclo de vida completo
5. US4 → `DELETE /tasks/{id}` → CRUD completo

---

## Notes

- [P] tasks = arquivos diferentes, sem dependências pendentes entre si
- [Story] label conecta cada task à user story da spec.md
- O arquivo `src/api/routes/tasks.py` cresce incrementalmente a cada user story — evitar edição simultânea
- Cada checkpoint é independentemente demonstrável
- Todos os erros retornam `{"detail": "mensagem em português"}` via handler global em `main.py`
- O handler global em `main.py` deve distinguir "não encontrada" (→ 404) de outros `ValueError` (→ 422) pelo conteúdo da mensagem
