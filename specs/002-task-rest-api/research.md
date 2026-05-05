# Research: API de Gestão de Tarefas

**Feature**: 002-task-rest-api
**Date**: 2026-05-05
**Status**: Complete — sem NEEDS CLARIFICATION pendentes

---

## Decisão 1: Framework HTTP

**Decision**: FastAPI
**Rationale**: Alinhamento total com o stack Python existente. Suporte nativo a type hints e Pydantic, geração automática de documentação interativa (/docs), validação de entrada declarativa, e padrão consolidado para serviços REST em Python.
**Alternatives considered**:
- Flask: mais simples, mas sem validação automática de schema e sem documentação embutida — exigiria código manual para o que FastAPI oferece nativamente.
- Django REST Framework: overhead excessivo para um serviço pequeno sem ORM, admin ou multi-app.

---

## Decisão 2: Validação de request e serialização de response

**Decision**: Pydantic v2 (via FastAPI)
**Rationale**: Já é a dependência transitiva do FastAPI. Permite declarar schemas de entrada (request body) e saída (response) como classes Python com type hints — consistente com o estilo do código existente (dataclasses, type hints em todas as funções).
**Alternatives considered**:
- Marshmallow: biblioteca externa adicional sem ganho relevante dado que Pydantic já vem com FastAPI.
- Validação manual: viola a separação de responsabilidades e duplica esforço.

---

## Decisão 3: Mapeamento de erros de negócio para respostas HTTP

**Decision**: Exception handler global para `ValueError` → HTTP 422; `KeyError`/not found → HTTP 404; erros de validação Pydantic → HTTP 422 automático do FastAPI.
**Rationale**:
- `TaskService` já lança `ValueError` com mensagens em português para todas as violações de negócio. Um handler centralizado evita repetição de try/except em cada rota.
- Tarefa não encontrada também é `ValueError` no serviço atual — o handler distingue pelo conteúdo "não encontrada" ou trata via sentinela.
- Corpo malformado é tratado automaticamente pelo FastAPI via Pydantic (HTTP 400/422).
**Alternatives considered**:
- Exceções customizadas (`TaskNotFoundError`, `BusinessRuleError`): mais explícito, mas requer modificar o TaskService existente — a spec proíbe modificar a camada de serviço.
- Try/except em cada rota: duplicação de código, propenso a inconsistências.

**Mapeamento final**:
| Situação | HTTP |
|---|---|
| Tarefa não encontrada (ValueError "não encontrada") | 404 |
| Violação de regra de negócio (ValueError) | 422 |
| Corpo da requisição malformado (Pydantic) | 422 |
| Status inválido no path/query (Pydantic enum) | 422 |

---

## Decisão 4: Injeção de dependência do TaskService

**Decision**: FastAPI `Depends()` com factory function
**Rationale**: Mantém o `TaskService` desacoplado da camada de rota. Permite substituição por mock em testes de integração sem modificar as rotas. Padrão idiomático do FastAPI.
**Alternatives considered**:
- Instância global: cria acoplamento e dificulta testes isolados.
- Parâmetro manual em cada rota: verboso e propenso a inconsistências.

---

## Decisão 5: Ciclo de vida do banco de dados

**Decision**: `lifespan` context manager do FastAPI — abre conexão na inicialização, fecha no shutdown.
**Rationale**: A `get_connection` e `create_schema` já existem em `src/database.py`. O `lifespan` é o padrão atual do FastAPI (superior ao `@app.on_event` deprecated).
**Alternatives considered**:
- Conexão por request: overhead desnecessário para SQLite em desenvolvimento local.
- Conexão global em módulo: dificulta testes e cleanup.

---

## Decisão 6: Estrutura de diretórios

**Decision**: Adicionar `src/api/` com `main.py`, `routes/tasks.py` e `schemas/task.py`
**Rationale**: Segue a separação de camadas já estabelecida (`models/`, `repositories/`, `services/`). A camada `api/` é responsável exclusivamente pela tradução HTTP ↔ domínio — sem lógica de negócio.
**Alternatives considered**:
- Tudo em `src/main.py`: inviável para manutenção à medida que endpoints crescem.
- `src/routers/`: nomenclatura válida, mas `api/` é mais descritiva da responsabilidade da camada.

---

## Conclusão

Todos os pontos de NEEDS CLARIFICATION foram resolvidos por análise do código existente e padrões de mercado. Nenhuma informação adicional do usuário é necessária.

Pronto para Phase 1 (design).
