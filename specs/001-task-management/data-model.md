# Data Model: Gestão de Tarefas

**Branch**: `001-task-management` | **Date**: 2026-05-04
**Phase**: 1 — Modelo de dados e regras de validação

---

## Entidade: Task

Representa uma unidade de trabalho criada e gerenciada por um colaborador.

### Campos

| Campo          | Tipo           | Obrigatório | Padrão    | Descrição                                                    |
|----------------|----------------|-------------|-----------|--------------------------------------------------------------|
| `id`           | `int`          | Gerado      | Auto      | Identificador único da tarefa (gerado pelo banco)            |
| `title`        | `str`          | Sim         | —         | Título da tarefa. Mínimo 3, máximo 100 caracteres            |
| `description`  | `str \| None`  | Não         | `None`    | Descrição detalhada. Sem restrição de tamanho                |
| `deadline`     | `date \| None` | Não         | `None`    | Prazo de conclusão. Não pode ser data anterior à atual       |
| `priority`     | `Priority`     | Não         | `media`   | Prioridade da tarefa: `baixa`, `media` ou `alta`             |
| `status`       | `TaskStatus`   | Gerado      | `pendente`| Status atual. Controlado pela máquina de estados             |
| `created_at`   | `date`         | Gerado      | hoje      | Data de criação (usada para detecção de título duplicado)    |
| `is_due_today` | `bool`         | Calculado   | —         | `True` se `deadline == date.today()`. Campo derivado         |

---

## Enums

### Priority

```
baixa   → Prioridade baixa
media   → Prioridade média (padrão)
alta    → Prioridade alta
```

### TaskStatus

```
pendente      → Estado inicial de toda tarefa criada
em_andamento  → Tarefa em execução ativa
concluida     → Tarefa finalizada (imutável após esta transição)
```

---

## Máquina de Estados: TaskStatus

```
[pendente] ──────────→ [em_andamento] ──────────→ [concluida]
               única transição válida       única transição válida
```

**Regras**:
- Toda tarefa nasce com status `pendente`
- Transições permitidas: `pendente → em_andamento`, `em_andamento → concluida`
- Nenhuma transição reversa é permitida
- Tarefa com status `concluida` não aceita nenhuma atualização de campo

---

## Regras de Validação

| Regra          | Campo      | Condição de Rejeição                                          | Erro                                             |
|----------------|------------|---------------------------------------------------------------|--------------------------------------------------|
| Título mínimo  | `title`    | `len(title) < 3`                                              | `ValueError: "Título deve ter pelo menos 3 caracteres"` |
| Título máximo  | `title`    | `len(title) > 100`                                            | `ValueError: "Título deve ter no máximo 100 caracteres"` |
| Prazo passado  | `deadline` | `deadline < date.today()`                                     | `ValueError: "Prazo não pode ser data passada"`  |
| Exclusão negada| `status`   | `status in ("em_andamento", "concluida")` ao deletar          | `ValueError: "Não é possível deletar tarefa em andamento"` |
| Edição negada  | `status`   | `status == "concluida"` ao editar                             | `ValueError: "Tarefa concluída não pode ser editada"` |

---

## Regras de Aviso (sem rejeição)

| Situação                  | Condição                                                          | Comportamento                                    |
|---------------------------|-------------------------------------------------------------------|--------------------------------------------------|
| Título duplicado no dia   | Existe outra tarefa com mesmo `title` e `created_at == today()`  | Cria normalmente; retorna `duplicate_warning=True` |
| Prazo é hoje              | `deadline == date.today()`                                        | Cria normalmente; `is_due_today=True`            |

---

## Esquema SQLite (dev)

```sql
CREATE TABLE tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL CHECK(length(title) >= 3 AND length(title) <= 100),
    description TEXT,
    deadline    TEXT,   -- ISO 8601: YYYY-MM-DD
    priority    TEXT    NOT NULL DEFAULT 'media'
                        CHECK(priority IN ('baixa', 'media', 'alta')),
    status      TEXT    NOT NULL DEFAULT 'pendente'
                        CHECK(status IN ('pendente', 'em_andamento', 'concluida')),
    created_at  TEXT    NOT NULL  -- ISO 8601: YYYY-MM-DD
);
```

> Nota: As validações de negócio (prazo no passado, transições de status, exclusão condicional) são aplicadas exclusivamente na camada de serviço, não via constraints do banco.
