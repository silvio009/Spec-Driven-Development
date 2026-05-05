# Research: Gestão de Tarefas

**Branch**: `001-task-management` | **Date**: 2026-05-04
**Phase**: 0 — Resolução de incógnitas e decisões de design

---

## Resultado

Nenhuma incógnita crítica identificada na spec. O `CLAUDE.md` define o stack completo. Todas as decisões abaixo foram tomadas com base na spec, nas regras do CLAUDE.md e em padrões consolidados para projetos Python.

---

## Decisões de Design

### D-001: Modelo de dados da Tarefa

**Decisão**: Usar `dataclass` Python com campos tipados para representar a entidade `Task`. Enums do módulo `enum` para `Priority` e `TaskStatus`.

**Racional**: Garante type hints nativos (exigência do CLAUDE.md), sem dependência extra. Pydantic pode ser adicionado na camada de API (fora do escopo desta spec).

**Alternativas consideradas**:
- Pydantic BaseModel → adequado para API/validação HTTP, mas excesso para camada de serviço puro
- TypedDict → sem suporte a métodos, menos expressivo para um modelo com comportamento

---

### D-002: Estratégia de persistência

**Decisão**: Repositório SQLite via `sqlite3` padrão da biblioteca Python, com banco em memória (`:memory:`) para testes.

**Racional**: CLAUDE.md especifica SQLite para dev. Evitar ORM reduz dependências e mantém o código mais simples para o escopo atual.

**Alternativas consideradas**:
- SQLAlchemy Core → mais poder, mas complexidade desnecessária para dev/single-user
- SQLAlchemy ORM → adiciona abstração não justificada neste escopo

---

### D-003: Padrão de erro para violações de negócio

**Decisão**: Usar `ValueError` com mensagem descritiva em português para todas as violações de regra de negócio.

**Racional**: A spec define explicitamente `ValueError` como o tipo de exceção esperado nos cenários de aceite ("lança ValueError com mensagem clara"). Manter consistência com a spec.

**Alternativas consideradas**:
- Exceções customizadas (ex: `InvalidTaskError`) → adequadas para APIs públicas, mas sobrecarga desnecessária para serviço interno

---

### D-004: Máquina de estados de status

**Decisão**: Transições válidas verificadas na camada de serviço via dicionário de transições permitidas:
```
VALID_TRANSITIONS = {
    "pendente": ["em_andamento"],
    "em_andamento": ["concluida"],
    "concluida": []
}
```

**Racional**: A spec define fluxo estritamente linear e unidirecional. O dicionário de transições torna a regra explícita e testável.

**Alternativas consideradas**:
- Verificação por if/elif → funcional, mas menos extensível e menos legível

---

### D-005: Detecção de título duplicado no mesmo dia

**Decisão**: A camada de serviço consulta o repositório por tarefas com o mesmo título e data de criação igual à data atual. Se encontrado, cria normalmente e retorna um flag `duplicate_warning=True` no resultado ou loga o aviso.

**Racional**: A spec define "permitir com aviso" — não é um erro, é uma informação adicional. Retornar um flag no resultado da criação é mais limpo do que efeitos colaterais.

**Alternativas consideradas**:
- Lançar exceção → incorreto, a spec permite a criação
- Warning via `warnings.warn()` → aceitável, mas menos testável que um flag explícito

---

### D-006: Sinalização "vence hoje"

**Decisão**: Campo calculado `is_due_today: bool` na entidade `Task`, calculado no momento da leitura comparando `deadline` com `date.today()`.

**Racional**: Propriedade derivada, não armazenada. Mantém o banco simples e a lógica na camada de serviço/modelo.

**Alternativas consideradas**:
- Coluna `is_due_today` no banco → dado calculável não deve ser armazenado

---

## Conclusão

Todas as decisões resolvidas. Nenhum NEEDS CLARIFICATION remanescente. Pronto para Phase 1.
