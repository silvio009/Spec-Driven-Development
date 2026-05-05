# Contract: TaskService

**Branch**: `001-task-management` | **Date**: 2026-05-04
**Layer**: Camada de serviço (regras de negócio)
**Module**: `src/services/task_service.py`

---

## Visão Geral

`TaskService` é a interface pública da camada de negócio para gestão de tarefas. Toda operação passa por esta camada antes de atingir o repositório. Nenhuma regra de negócio existe fora desta camada.

---

## Funções Públicas

### `create_task`

```python
def create_task(
    title: str,
    description: str | None = None,
    deadline: date | None = None,
    priority: Priority = Priority.MEDIA,
) -> tuple[Task, bool]:
    ...
```

**Descrição**: Cria uma nova tarefa com status inicial `pendente`.

**Retorno**: `(task, duplicate_warning)` onde `duplicate_warning=True` se já existe tarefa com mesmo título no dia atual.

**Pré-condições** (lança `ValueError` se violadas):
- `len(title) >= 3` e `len(title) <= 100`
- `deadline >= date.today()` (se fornecido)

**Efeitos**: Persiste a tarefa no repositório.

---

### `list_tasks`

```python
def list_tasks(
    status: TaskStatus | None = None,
    priority: Priority | None = None,
) -> list[Task]:
    ...
```

**Descrição**: Retorna todas as tarefas, com filtragem opcional por status e/ou prioridade.

**Retorno**: Lista de `Task`. Retorna lista vazia (`[]`) se nenhuma tarefa for encontrada — nunca lança erro por lista vazia.

**Pré-condições**: Nenhuma.

**Efeitos**: Nenhum (somente leitura).

---

### `update_task_status`

```python
def update_task_status(
    task_id: int,
    new_status: TaskStatus,
) -> Task:
    ...
```

**Descrição**: Avança o status de uma tarefa seguindo a máquina de estados.

**Retorno**: `Task` atualizada.

**Pré-condições** (lança `ValueError` se violadas):
- `task_id` deve existir no repositório
- Transição `current_status → new_status` deve ser válida:
  - `pendente → em_andamento` ✅
  - `em_andamento → concluida` ✅
  - Qualquer outra → ❌

**Efeitos**: Persiste o novo status no repositório.

---

### `delete_task`

```python
def delete_task(task_id: int) -> None:
    ...
```

**Descrição**: Remove permanentemente uma tarefa do sistema.

**Retorno**: `None`

**Pré-condições** (lança `ValueError` se violadas):
- `task_id` deve existir no repositório
- `task.status` deve ser `pendente`; qualquer outro status bloqueia a exclusão:
  - `em_andamento` → `ValueError: "Não é possível deletar tarefa em andamento"`
  - `concluida` → `ValueError: "Não é possível deletar tarefa concluída"`

**Efeitos**: Remove a tarefa do repositório permanentemente.

---

## Dependências

```python
# Injetadas via construtor ou parâmetro
task_repository: TaskRepository  # src/repositories/task_repository.py
```

---

## Comportamentos Transversais

| Situação                      | Comportamento                                               |
|-------------------------------|-------------------------------------------------------------|
| `task_id` inexistente         | `ValueError: "Tarefa não encontrada"`                       |
| Lista vazia (sem tarefas)     | Retorna `[]`, não lança exceção                             |
| Título duplicado no mesmo dia | Cria normalmente; `duplicate_warning=True` no retorno       |
| `deadline == date.today()`    | Cria normalmente; `task.is_due_today == True` no retorno    |

---

## Invariantes

- Nenhuma tarefa é criada com status diferente de `pendente`.
- Nenhuma tarefa com status `concluida` é modificada.
- Nenhuma tarefa com status `em_andamento` ou `concluida` é excluída.
- A camada de serviço nunca acessa o banco diretamente — sempre via `TaskRepository`.
