# Quickstart: Interface Visual de Gestão de Tarefas

**Feature**: 003-task-frontend-ui
**Date**: 2026-05-05

---

## Pré-requisitos

1. A API `002-task-rest-api` está rodando em `http://localhost:8000`:
   ```bash
   uvicorn src.api.main:app --reload
   ```

2. Um navegador moderno (Chrome ou Edge)

## Como abrir a interface

Abrir o arquivo diretamente no navegador:

```
frontend/index.html
```

Ou via duplo clique no explorador de arquivos.

> **Nota**: Como a interface faz chamadas para `localhost:8000`, não é necessário um servidor web — abrir o arquivo diretamente funciona para desenvolvimento local.

## Validação rápida

1. Abrir `frontend/index.html` no Chrome
2. A lista de tarefas deve aparecer (ou estado vazio se não houver tarefas)
3. Criar uma tarefa pelo formulário → deve aparecer na lista
4. Clicar em "Iniciar" → badge muda para azul "Em andamento"
5. Clicar em "Concluir" → badge muda para verde "Concluída"
6. Criar outra tarefa pendente e clicar em "Deletar" → tarefa desaparece
7. Usar os filtros de status → lista filtra corretamente

## Testar API indisponível

1. Parar o servidor da API (`Ctrl+C`)
2. Recarregar a página → deve aparecer "Serviço temporariamente indisponível"
