# Time Manager — Documentação

## O projeto

Um gerenciador de tarefas construído para aprender **SDD na prática**.

O objetivo não era só o software funcionando — era aprender a trabalhar com especificação antes do código.

---

## O fluxo SDD aplicado

Cada feature seguiu o mesmo ciclo:

```
/speckit-specify   → escrever O QUÊ antes de pensar em COMO
/speckit-plan      → decidir arquitetura, contratos e modelo de dados
/speckit-tasks     → quebrar em tasks executáveis com dependências claras
/speckit-implement → código guiado pelas tasks (sem improvisar)
```

Três features foram desenvolvidas nessa ordem:

| # | Feature | O que entrega |
|---|---------|---------------|
| 001 | task-management | Modelo de domínio: `Task`, regras de negócio, repositório |
| 002 | task-rest-api | API REST em FastAPI expondo o domínio via HTTP |
| 003 | task-frontend-ui | Interface visual em HTML/CSS/JS consumindo a API |

Cada feature tem seus artefatos em `specs/NNN-nome/`:
- `spec.md` — especificação funcional (linguagem de negócio, sem código)
- `plan.md` — decisões técnicas e arquitetura
- `contracts/` — contratos de interface (endpoints, schemas)
- `tasks.md` — lista de tasks executadas

---

## Como rodar

```bash
# 1. Ativar ambiente
venv\Scripts\activate

# 2. Subir a API
uvicorn src.api.main:app --reload

# 3. Abrir o frontend
# Abrir frontend/index.html no Chrome

# 4. Rodar os testes
pytest tests/ -v
```

---

## O que o SDD mudou na prática

Sem SDD, você começa a codar e descobre os problemas no meio do caminho.

Com SDD:
- A `spec.md` forçou pensar nas **regras de negócio** antes da implementação
- Os **contratos de API** foram definidos antes de escrever um endpoint
- As **tasks** tornaram a implementação previsível — sem decisões surpresa no código
- Cada feature foi entregue em incrementos validáveis
