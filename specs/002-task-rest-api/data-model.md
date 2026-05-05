# Data Model: API de Gestão de Tarefas

**Feature**: 002-task-rest-api
**Date**: 2026-05-05
**Depende de**: `001-task-management` — entidade `Task` e enums `Priority`, `TaskStatus`

---

## Entidades de domínio reutilizadas (sem modificação)

### Task (`src/models/task.py`)

| Campo | Tipo | Obrigatório | Regras |
|---|---|---|---|
| `id` | `int \| None` | Gerado | Autoincrement, None antes de persistir |
| `title` | `str` | Sim | 3–100 caracteres |
| `description` | `str \| None` | Não | Sem limite de tamanho |
| `deadline` | `date \| None` | Não | Não pode ser data passada |
| `priority` | `Priority` | Não | Padrão: `media` |
| `status` | `TaskStatus` | Gerado | Padrão inicial: `pendente` |
| `created_at` | `date` | Gerado | Data do sistema no momento da criação |

### Priority (enum)
`baixa` | `media` | `alta`

### TaskStatus (enum)
`pendente` → `em_andamento` → `concluida` (unidirecional)

---

## Schemas de API (Pydantic — novos)

### TaskCreateRequest — corpo do POST /tasks

| Campo | Tipo | Obrigatório | Validação |
|---|---|---|---|
| `title` | `str` | Sim | min_length=3, max_length=100 |
| `description` | `str \| None` | Não | — |
| `deadline` | `date \| None` | Não | Validação de data passada: responsabilidade do TaskService |
| `priority` | `Priority \| None` | Não | Enum; padrão `media` se ausente |

### StatusUpdateRequest — corpo do PATCH /tasks/{id}/status

| Campo | Tipo | Obrigatório | Validação |
|---|---|---|---|
| `new_status` | `TaskStatus` | Sim | Enum; valor inválido → 422 automático |

### TaskResponse — resposta de criação e atualização

| Campo | Tipo | Sempre presente |
|---|---|---|
| `id` | `int` | Sim |
| `title` | `str` | Sim |
| `description` | `str \| None` | Sim |
| `deadline` | `date \| None` | Sim |
| `priority` | `Priority` | Sim |
| `status` | `TaskStatus` | Sim |
| `created_at` | `date` | Sim |
| `is_due_today` | `bool` | Sim |

### TaskCreateResponse — resposta específica do POST /tasks

Herda `TaskResponse` e adiciona:

| Campo | Tipo | Sempre presente |
|---|---|---|
| `duplicate_warning` | `bool` | Sim |

### ErrorResponse — resposta de erro (422, 404)

| Campo | Tipo |
|---|---|
| `detail` | `str` |

---

## Mapeamento domínio → HTTP

| Operação de domínio | Método HTTP | Path | Sucesso | Erro negócio | Não encontrado | Dados inválidos |
|---|---|---|---|---|---|---|
| `create_task()` | POST | `/tasks` | 201 + TaskCreateResponse | 422 + ErrorResponse | — | 422 |
| `list_tasks()` | GET | `/tasks` | 200 + list[TaskResponse] | — | — | 422 |
| `update_task_status()` | PATCH | `/tasks/{id}/status` | 200 + TaskResponse | 422 + ErrorResponse | 404 + ErrorResponse | 422 |
| `delete_task()` | DELETE | `/tasks/{id}` | 204 (sem corpo) | 422 + ErrorResponse | 404 + ErrorResponse | — |

---

## Transições de estado (herdadas do domínio)

```
pendente ──► em_andamento ──► concluida
```

- Retroceder não é permitido
- Tarefas `concluida` são imutáveis
- Exclusão permitida apenas para `pendente`
