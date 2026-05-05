# SPEC: API REST — Gestão de Tarefas

**Status:** aprovada  
**Autor:** dev-requisitos  
**Revisado por:** dev-senior  
**Data:** 2026-05-04  
**Depende de:** 001-task-management  

## Propósito
Expor o TaskService via HTTP para que um frontend
ou cliente externo consiga consumir as funcionalidades
de gestão de tarefas.

## Usuários afetados
- Frontend web que vai exibir as tarefas
- Desenvolvedores que vão integrar com a API

## Requisitos funcionais
1. POST /tasks — criar nova tarefa
2. GET /tasks — listar tarefas com filtro opcional por status
3. PATCH /tasks/{id}/status — atualizar status da tarefa
4. DELETE /tasks/{id} — deletar tarefa

## Regras de negócio
- Reutilizar TaskService existente sem modificar
- Erros de negócio (ValueError) retornam HTTP 422
- Respostas sempre em JSON
- Documentação automática disponível em /docs

## Edge cases
- ID inexistente: retornar HTTP 404
- Status inválido: retornar HTTP 422 com mensagem clara
- Corpo da requisição inválido: retornar HTTP 400

## Critérios de aceite (Given/When/Then)

**Cenário 1 — Criar tarefa via API**  
Given payload JSON com título válido e prazo futuro  
When POST /tasks  
Then retorna HTTP 201 com tarefa criada em JSON  

**Cenário 2 — Erro de negócio via API**  
Given payload com título de 2 caracteres  
When POST /tasks  
Then retorna HTTP 422 com mensagem de erro em português  

**Cenário 3 — Listar tarefas**  
Given tarefas cadastradas no banco  
When GET /tasks  
Then retorna HTTP 200 com lista em JSON  

**Cenário 4 — ID inexistente**  
Given ID que não existe no banco  
When DELETE /tasks/{id}  
Then retorna HTTP 404  

## Fora do escopo desta spec
- Autenticação e autorização
- Paginação
- Interface visual