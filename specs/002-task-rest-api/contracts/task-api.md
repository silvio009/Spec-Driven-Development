# Contrato da API: Gestão de Tarefas

**Feature**: 002-task-rest-api
**Date**: 2026-05-05
**Base URL**: `http://localhost:8000`
**Formato**: JSON (todas as requisições e respostas)
**Documentação interativa**: `GET /docs`

---

## POST /tasks — Criar tarefa

### Request

```
POST /tasks
Content-Type: application/json
```

**Corpo**:
```json
{
  "title": "string (3–100 chars, obrigatório)",
  "description": "string | null (opcional)",
  "deadline": "YYYY-MM-DD | null (opcional, não pode ser passado)",
  "priority": "baixa | media | alta | null (opcional, padrão: media)"
}
```

### Responses

**201 Created** — tarefa registrada com sucesso:
```json
{
  "id": 1,
  "title": "Preparar relatório",
  "description": null,
  "deadline": "2026-05-10",
  "priority": "media",
  "status": "pendente",
  "created_at": "2026-05-05",
  "is_due_today": false,
  "duplicate_warning": false
}
```

**422 Unprocessable Entity** — erro de validação ou regra de negócio:
```json
{
  "detail": "O título deve ter pelo menos 3 caracteres. Recebido: 2 caractere(s)."
}
```

**Cenários de erro 422**:
- Título com menos de 3 caracteres
- Título com mais de 100 caracteres
- Prazo anterior à data atual
- Corpo malformado ou campo obrigatório ausente

---

## GET /tasks — Listar tarefas

### Request

```
GET /tasks
GET /tasks?status=pendente
GET /tasks?priority=alta
GET /tasks?status=em_andamento&priority=alta
```

**Query parameters** (todos opcionais):

| Parâmetro | Tipo | Valores aceitos |
|---|---|---|
| `status` | string | `pendente`, `em_andamento`, `concluida` |
| `priority` | string | `baixa`, `media`, `alta` |

### Responses

**200 OK** — lista de tarefas (pode ser vazia):
```json
[
  {
    "id": 1,
    "title": "Preparar relatório",
    "description": null,
    "deadline": "2026-05-10",
    "priority": "media",
    "status": "pendente",
    "created_at": "2026-05-05",
    "is_due_today": false
  }
]
```

**422 Unprocessable Entity** — valor de filtro inválido:
```json
{
  "detail": "..."
}
```

---

## PATCH /tasks/{id}/status — Atualizar status

### Request

```
PATCH /tasks/{id}/status
Content-Type: application/json
```

**Path parameter**: `id` — identificador inteiro da tarefa

**Corpo**:
```json
{
  "new_status": "em_andamento"
}
```

Valores aceitos para `new_status`: `pendente`, `em_andamento`, `concluida`

### Responses

**200 OK** — status atualizado:
```json
{
  "id": 1,
  "title": "Preparar relatório",
  "description": null,
  "deadline": "2026-05-10",
  "priority": "media",
  "status": "em_andamento",
  "created_at": "2026-05-05",
  "is_due_today": false
}
```

**404 Not Found** — tarefa não encontrada:
```json
{
  "detail": "Tarefa não encontrada: id=99."
}
```

**422 Unprocessable Entity** — transição inválida ou tarefa concluída:
```json
{
  "detail": "Tarefa concluída não pode ser editada."
}
```

**Cenários de erro 422**:
- Tentar editar tarefa com status `concluida`
- Transição não permitida (ex.: `pendente` → `concluida` direto)
- Valor de `new_status` inválido

---

## DELETE /tasks/{id} — Deletar tarefa

### Request

```
DELETE /tasks/{id}
```

**Path parameter**: `id` — identificador inteiro da tarefa

### Responses

**204 No Content** — tarefa removida com sucesso (sem corpo)

**404 Not Found** — tarefa não encontrada:
```json
{
  "detail": "Tarefa não encontrada: id=99."
}
```

**422 Unprocessable Entity** — tarefa protegida contra exclusão:
```json
{
  "detail": "Não é possível deletar tarefa em andamento."
}
```

**Cenários de erro 422**:
- Tarefa com status `em_andamento`
- Tarefa com status `concluida`

---

## Regras gerais

- Todos os erros retornam `{"detail": "mensagem em português"}`
- Datas são sempre no formato ISO 8601: `YYYY-MM-DD`
- Enums são sempre em minúsculas com underscore: `em_andamento`, não `EM_ANDAMENTO`
- O campo `is_due_today` é calculado dinamicamente (não armazenado)
- O campo `duplicate_warning: true` indica título duplicado no mesmo dia, mas **não bloqueia** a criação
