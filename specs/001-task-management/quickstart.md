# Quickstart: Gestão de Tarefas

**Branch**: `001-task-management` | **Date**: 2026-05-04

---

## Pré-requisitos

- Python 3.11+
- pip

---

## Instalação

```bash
# Clone / entre no projeto
cd time-manager

# Crie o ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# Instale as dependências (quando o requirements.txt for criado)
pip install -r requirements.txt
```

> Dependências previstas: `pytest`, `pytest-cov`
> O módulo `sqlite3` é padrão da biblioteca Python — sem instalação necessária.

---

## Estrutura de diretórios esperada

```
time-manager/
├── src/
│   ├── models/
│   │   └── task.py             # Entidade Task e enums
│   ├── services/
│   │   └── task_service.py     # Regras de negócio
│   ├── repositories/
│   │   └── task_repository.py  # Acesso ao SQLite
│   └── database.py             # Configuração do banco
└── tests/
    ├── unit/
    │   └── test_task_service.py
    └── integration/
        └── test_task_repository.py
```

---

## Executar os testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src tests/

# Apenas unit tests
pytest tests/unit/

# Apenas integration tests
pytest tests/integration/
```

---

## Uso básico da camada de serviço

```python
from datetime import date, timedelta
from src.models.task import Priority
from src.services.task_service import TaskService
from src.repositories.task_repository import TaskRepository
from src.database import get_connection

# Configurar
conn = get_connection(":memory:")  # banco em memória para teste rápido
repo = TaskRepository(conn)
service = TaskService(repo)

# Criar tarefa
task, warning = service.create_task(
    title="Revisar relatório",
    deadline=date.today() + timedelta(days=3),
    priority=Priority.ALTA,
)
print(task.status)  # pendente
print(warning)      # False (sem duplicata)

# Listar tarefas
tasks = service.list_tasks(status=None, priority=None)
print(len(tasks))  # 1

# Avançar status
task = service.update_task_status(task.id, TaskStatus.EM_ANDAMENTO)
print(task.status)  # em_andamento

# Tentar deletar tarefa em andamento → ValueError
try:
    service.delete_task(task.id)
except ValueError as e:
    print(e)  # Não é possível deletar tarefa em andamento
```

---

## Cenários de teste recomendados

Veja os critérios de aceite completos em [`spec.md`](./spec.md). Os cenários principais:

| Cenário                         | Método                                | Resultado Esperado                     |
|---------------------------------|---------------------------------------|----------------------------------------|
| Criar tarefa válida             | `create_task("Título ok", ...)`       | `task.status == "pendente"`            |
| Título muito curto              | `create_task("AB")`                   | `ValueError`                           |
| Prazo no passado                | `create_task(..., deadline=ontem)`    | `ValueError: "Prazo não pode..."`      |
| Deletar tarefa em andamento     | `delete_task(id_em_andamento)`        | `ValueError: "Não é possível..."`      |
| Listar sem tarefas              | `list_tasks()`                        | `[]` (sem erro)                        |
| Título duplicado no mesmo dia   | `create_task("Mesmo título", ...)`×2  | 2ª chamada: `duplicate_warning=True`   |
