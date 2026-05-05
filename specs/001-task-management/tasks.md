# Tasks: Gestão de Tarefas

**Input**: Design documents from `specs/001-task-management/`
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/task-service.md ✅

**Tests**: Incluídos — obrigatórios conforme `CLAUDE.md` ("Testes obrigatórios para toda função de serviço").

**Organização**: Tarefas agrupadas por User Story para permitir implementação e teste independentes.

## Format: `[ID] [P?] [Story?] Descrição — caminho/do/arquivo.py`

- **[P]**: Pode executar em paralelo (arquivos diferentes, sem dependências entre si)
- **[Story]**: User Story à qual a tarefa pertence (US1, US2, US3, US4)

---

## Phase 1: Setup (Infraestrutura Inicial)

**Objetivo**: Criar estrutura de diretórios e configuração base do projeto Python.

- [x] T001 Criar estrutura de diretórios: `src/models/`, `src/services/`, `src/repositories/`, `tests/unit/`, `tests/integration/`
- [x] T002 [P] Criar `requirements.txt` com `pytest` e `pytest-cov`
- [x] T003 [P] Criar arquivos `__init__.py` em: `src/`, `src/models/`, `src/services/`, `src/repositories/`, `tests/`, `tests/unit/`, `tests/integration/`

---

## Phase 2: Foundational (Pré-requisitos Bloqueantes)

**Objetivo**: Infraestrutura central que DEVE estar completa antes de qualquer User Story.

> **⚠️ CRÍTICO**: Nenhuma User Story pode começar até esta fase estar completa.

- [x] T004 [P] Criar entidade `Task`, enums `Priority` e `TaskStatus`, e propriedade calculada `is_due_today` em `src/models/task.py` — conforme `data-model.md` (campos: id, title, description, deadline, priority, status, created_at)
- [x] T005 [P] Implementar `get_connection(path: str) -> sqlite3.Connection` e `create_schema(conn)` em `src/database.py` — schema SQLite conforme `data-model.md` (tabela `tasks` com colunas e CHECK constraints)
- [x] T006 Implementar `TaskRepository` em `src/repositories/task_repository.py` com métodos: `save(task) -> Task`, `find_all(status, priority) -> list[Task]`, `find_by_id(id) -> Task | None`, `find_by_title_and_date(title, date) -> list[Task]`, `update(task) -> Task`, `delete(id) -> None` — depende de T004

**Checkpoint**: Fundação pronta — implementação das User Stories pode começar.

---

## Phase 3: User Story 1 — Criar Tarefa (Priority: P1) 🎯 MVP

**Goal**: Colaborador cria tarefa válida com título, descrição, prazo e prioridade; sistema aplica todas as regras de validação.

**Independent Test**: Instanciar `TaskService` com repositório em memória, chamar `create_task()` com dados válidos e inválidos, e verificar os 6 cenários de aceite da spec (título curto, prazo passado, duplicata, prazo hoje).

### Testes para User Story 1

> **Escrever ANTES da implementação — garantir que FALHAM antes do T008**

- [x] T007 [P] [US1] Escrever testes unitários para `create_task` em `tests/unit/test_task_service.py`: cobrir os 6 cenários da spec — tarefa válida retorna `status=pendente`; título < 3 chars lança `ValueError`; prazo passado lança `ValueError("Prazo não pode ser data passada")`; título > 100 chars lança `ValueError`; título duplicado no dia retorna `duplicate_warning=True`; prazo hoje retorna `is_due_today=True`

### Implementação para User Story 1

- [x] T008 [US1] Implementar classe `TaskService` com método `create_task(title, description, deadline, priority) -> tuple[Task, bool]` em `src/services/task_service.py` — validar título (3–100 chars), prazo (não passado), verificar duplicata via repositório, registrar com `status=pendente`; docstrings em português, type hints em todas as assinaturas — depende de T006, T007

**Checkpoint**: US1 completa — `pytest tests/unit/ -k test_create` deve passar com 6 testes verdes.

---

## Phase 4: User Story 2 — Listar e Filtrar Tarefas (Priority: P2)

**Goal**: Colaborador lista suas tarefas aplicando filtros opcionais por status e/ou prioridade; lista vazia retorna `[]` sem erro.

**Independent Test**: Criar tarefas com status e prioridades variadas, chamar `list_tasks()` com combinações de filtros, verificar que retorna apenas os registros correspondentes — incluindo o cenário de lista vazia.

### Testes para User Story 2

> **Escrever ANTES da implementação — garantir que FALHAM antes do T010**

- [x] T009 [P] [US2] Escrever testes unitários para `list_tasks` em `tests/unit/test_task_service.py`: cobrir 4 cenários — sem tarefas retorna `[]`; filtro por `status=pendente` retorna somente pendentes; filtro por `priority=alta` retorna somente alta; filtros combinados retornam interseção

### Implementação para User Story 2

- [x] T010 [US2] Adicionar método `list_tasks(status, priority) -> list[Task]` a `TaskService` em `src/services/task_service.py` — delegar filtragem ao repositório; retornar `[]` quando sem resultados (nunca lançar exceção por lista vazia); docstrings em português, type hints — depende de T008, T009

**Checkpoint**: US2 completa — `pytest tests/unit/ -k test_list` deve passar com 4 testes verdes.

---

## Phase 5: User Story 3 — Atualizar Status da Tarefa (Priority: P3)

**Goal**: Colaborador avança o status da tarefa no fluxo unidirecional `pendente → em_andamento → concluida`; sistema bloqueia transições inválidas e edições em tarefas concluídas.

**Independent Test**: Criar tarefa, aplicar transições em sequência válida, tentar transição inválida e tentar editar tarefa concluída — verificar os 3 cenários da spec.

### Testes para User Story 3

> **Escrever ANTES da implementação — garantir que FALHAM antes do T012**

- [x] T011 [P] [US3] Escrever testes unitários para `update_task_status` em `tests/unit/test_task_service.py`: cobrir 3 cenários — `pendente → em_andamento` atualiza com sucesso; `em_andamento → concluida` atualiza com sucesso; qualquer edição em tarefa `concluida` lança `ValueError("Tarefa concluída não pode ser editada")`

### Implementação para User Story 3

- [x] T012 [US3] Adicionar método `update_task_status(task_id, new_status) -> Task` a `TaskService` em `src/services/task_service.py` — implementar dicionário `VALID_TRANSITIONS` para validar transição; bloquear qualquer operação em `concluida`; lançar `ValueError` com mensagem descritiva para transições inválidas; docstrings em português, type hints — depende de T010, T011

**Checkpoint**: US3 completa — `pytest tests/unit/ -k test_update` deve passar com 3 testes verdes.

---

## Phase 6: User Story 4 — Deletar Tarefa (Priority: P4)

**Goal**: Colaborador remove tarefa com status `pendente`; sistema bloqueia exclusão de tarefas `em_andamento` ou `concluida`.

**Independent Test**: Criar tarefas nos 3 status possíveis, tentar deletar cada uma — verificar os 3 cenários da spec.

### Testes para User Story 4

> **Escrever ANTES da implementação — garantir que FALHAM antes do T014**

- [x] T013 [P] [US4] Escrever testes unitários para `delete_task` em `tests/unit/test_task_service.py`: cobrir 3 cenários — tarefa `pendente` é removida com sucesso; tarefa `em_andamento` lança `ValueError("Não é possível deletar tarefa em andamento")`; tarefa `concluida` lança `ValueError`

### Implementação para User Story 4

- [x] T014 [US4] Adicionar método `delete_task(task_id) -> None` a `TaskService` em `src/services/task_service.py` — verificar existência da tarefa; bloquear exclusão se `status != pendente`; lançar `ValueError` com mensagem descritiva; delegar remoção ao repositório; docstrings em português, type hints — depende de T012, T013

**Checkpoint**: US4 completa — `pytest tests/unit/ -k test_delete` deve passar com 3 testes verdes.

---

## Phase 7: Polish & Preocupações Transversais

**Objetivo**: Testes de integração, validação final de qualidade e conformidade com CLAUDE.md.

- [x] T015 [P] Escrever testes de integração para `TaskRepository` em `tests/integration/test_task_repository.py` — usar banco `:memory:` via `get_connection(":memory:")`; cobrir: `save`, `find_all` com filtros, `find_by_id` com id inexistente, `find_by_title_and_date`, `update`, `delete`
- [x] T016 Auditar todos os arquivos em `src/` para conformidade com CLAUDE.md: type hints em todas as funções, docstrings em português em todas as funções, nomes de variáveis e funções em inglês
- [x] T017 Executar suíte completa (`pytest --cov=src tests/`) e validar os cenários do `quickstart.md` manualmente

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sem dependências — pode começar imediatamente
- **Foundational (Phase 2)**: Depende de Phase 1 — **bloqueia todas as User Stories**
- **User Stories (Phases 3–6)**: Dependem da Phase 2; executadas em sequência de prioridade (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depende da conclusão de todas as User Stories desejadas

### User Story Dependencies

- **US1 (P1)**: Pode começar após Phase 2 — sem dependência de outras stories
- **US2 (P2)**: Depende de US1 (adiciona método ao mesmo `TaskService`)
- **US3 (P3)**: Depende de US2 (adiciona método ao mesmo `TaskService`)
- **US4 (P4)**: Depende de US3 (adiciona método ao mesmo `TaskService`)

### Within Each User Story

1. Escrever testes → confirmar que **FALHAM**
2. Implementar a função de serviço
3. Confirmar que todos os testes **PASSAM**
4. Fazer commit antes de passar para a próxima story

### Parallel Opportunities

| Contexto | Tasks Paralelizáveis |
|----------|---------------------|
| Phase 1 | T002, T003 (com T001 em andamento) |
| Phase 2 | T004, T005 simultaneamente |
| Phase 3 | T007 pode começar enquanto T006 termina |
| Phase 7 | T015 pode começar em paralelo com T016 |

---

## Parallel Example: Phase 2

```bash
# Executar T004 e T005 em paralelo (arquivos diferentes, sem dependências):
Task: "Criar Task entity em src/models/task.py"
Task: "Configurar SQLite em src/database.py"

# Após T004 e T005 concluídos, iniciar T006:
Task: "Implementar TaskRepository em src/repositories/task_repository.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Apenas)

1. Completar Phase 1: Setup
2. Completar Phase 2: Foundational (**CRÍTICO — bloqueia todas as stories**)
3. Completar Phase 3: US1 — Criar Tarefa
4. **PARAR E VALIDAR**: `pytest tests/unit/ -k test_create` — todos os 6 cenários verdes
5. Demonstrar/entregar: colaborador já consegue criar tarefas com validação completa

### Incremental Delivery

1. Setup + Foundational → Base pronta
2. US1 (Criar Tarefa) → MVP funcional — validar independentemente
3. US2 (Listar/Filtrar) → adicionar visibilidade — validar independentemente
4. US3 (Atualizar Status) → adicionar fluxo de progresso — validar independentemente
5. US4 (Deletar) → ciclo CRUD completo — validar independentemente
6. Polish → qualidade e cobertura finais

---

## Notes

- **[P]** = arquivos diferentes, sem dependências entre si na mesma fase
- **[Story]** = rastreabilidade entre tarefa e User Story da spec
- Cada User Story deve ser completamente testável antes de passar para a próxima
- Confirmar que testes **FALHAM** antes de implementar (red-green-refactor)
- Commitar após cada fase ou grupo lógico
- Parar em qualquer checkpoint para validar a story independentemente
- Evitar: tarefas vagas, conflito de arquivos entre stories, dependências que quebrem independência

---

## Summary

| Fase | Tasks | User Story |
|------|-------|------------|
| Phase 1: Setup | T001–T003 | — |
| Phase 2: Foundational | T004–T006 | — |
| Phase 3: Criar Tarefa | T007–T008 | US1 (P1) 🎯 |
| Phase 4: Listar/Filtrar | T009–T010 | US2 (P2) |
| Phase 5: Atualizar Status | T011–T012 | US3 (P3) |
| Phase 6: Deletar Tarefa | T013–T014 | US4 (P4) |
| Phase 7: Polish | T015–T017 | — |
| **Total** | **17 tasks** | **4 User Stories** |
