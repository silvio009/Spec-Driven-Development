# CLAUDE.md — Contexto Corporativo

## Projeto
Time Manager — sistema de gestão de tempo e tarefas.
Stack: Python 3, FastAPI, SQLite (dev), pytest.

## Regras obrigatórias
- NUNCA escreva código sem ler a spec em .github/specs/
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

<!-- SPECKIT START -->
## Plano de Implementação Ativo

Feature: Gestão de Tarefas
Branch: `001-task-management`
Plano: `specs/001-task-management/plan.md`
Spec: `specs/001-task-management/spec.md`
Contrato de serviço: `specs/001-task-management/contracts/task-service.md`
Modelo de dados: `specs/001-task-management/data-model.md`
<!-- SPECKIT END -->