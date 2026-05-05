# CLAUDE.md — Contexto Corporativo

## Projeto
Time Manager — sistema de gestão de tempo e tarefas.
Stack: Python 3, FastAPI, SQLite (dev), pytest.

## Regras obrigatórias
- NUNCA escreva código sem ler a spec em specs/
- SEMPRE proponha o plano técnico antes de implementar
- Aguarde aprovação humana antes de prosseguir
- Nomes de variáveis e funções em inglês
- Comentários e docstrings em português
- Commits seguem Conventional Commits (feat:, fix:, docs:)

## Padrões de código
- Python com type hints em todas as funções
- Sem funções sem docstring
- Testes obrigatórios para toda função de serviço
- Separar regras de negócio da camada de rota

## O que NÃO fazer
- Não instale pacotes sem listar antes para aprovação
- Não crie rotas sem spec aprovada
- Não altere o banco sem documentar a mudança

## O que já existe — não recriar
- src/models/task.py — entidade Task, enums Priority e TaskStatus
- src/database.py — conexão SQLite
- src/repositories/task_repository.py — CRUD completo
- src/services/task_service.py — regras de negócio
- src/api/main.py — app FastAPI configurado
- src/api/routes/tasks.py — endpoints POST, GET, PATCH, DELETE
- src/api/schemas/task.py — schemas Pydantic
- src/api/dependencies.py — injeção de dependência

<!-- SPECKIT START -->
## Plano de Implementação Ativo

Feature: Interface Visual de Gestão de Tarefas
Branch: `003-task-frontend-ui`
Plano: `specs/003-task-frontend-ui/plan.md`
Spec: `specs/003-task-frontend-ui/spec.md`
Contrato de UI: `specs/003-task-frontend-ui/contracts/ui-interactions.md`
Modelo de dados: `specs/003-task-frontend-ui/data-model.md`
Modelo de dados: `specs/001-task-management/data-model.md`
<!-- SPECKIT END -->