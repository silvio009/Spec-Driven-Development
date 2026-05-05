# Contrato de Interações da Interface: Gestão de Tarefas

**Feature**: 003-task-frontend-ui
**Date**: 2026-05-05
**Tipo**: Contrato UI — define interações do usuário, chamadas à API e efeitos visuais esperados

---

## Fluxo 1: Carregar página

**Trigger**: Usuário acessa `index.html` no navegador

**Ação da interface**:
1. Chamar `GET http://localhost:8000/tasks/` (sem filtro)
2. Renderizar lista de cards de tarefas

**Efeitos visuais**:
- Sucesso: lista de cards exibida (ou estado vazio se `[]`)
- Erro de rede/API: mensagem "Serviço temporariamente indisponível"

---

## Fluxo 2: Criar tarefa

**Trigger**: Usuário clica no botão "Salvar" no formulário de criação

**Validação pré-envio** (frontend, sem chamada à API):
- `title.length < 3` → exibir erro inline no campo título, não enviar

**Ação da interface** (se validação passou):
1. Chamar `POST http://localhost:8000/tasks/` com payload `{title, description, deadline, priority}`
2. Se sucesso (201):
   - Verificar `duplicate_warning` → exibir aviso se `true`
   - Limpar campos do formulário
   - Re-chamar `GET /tasks/` com filtro ativo e re-renderizar lista
3. Se erro (422/400): exibir `response.detail` como mensagem de erro; manter formulário aberto com dados preenchidos
4. Se erro de rede: exibir "Serviço temporariamente indisponível"

---

## Fluxo 3: Filtrar por status

**Trigger**: Usuário clica em botão/opção de filtro ("Todos", "Pendente", "Em andamento", "Concluída")

**Ação da interface**:
1. Atualizar `activeFilter`
2. Chamar `GET http://localhost:8000/tasks/` com `?status=<valor>` (ou sem parâmetro se "Todos")
3. Re-renderizar lista

**Efeitos visuais**:
- Filtro ativo destacado visualmente
- Lista re-renderizada imediatamente
- Estado vazio específico se resultado for `[]`

---

## Fluxo 4: Avançar status

**Trigger**: Usuário clica no botão "Iniciar" (pendente → em_andamento) ou "Concluir" (em_andamento → concluida) em um card

**Ação da interface**:
1. Calcular `nextStatus` com base no `status` atual do card
2. Chamar `PATCH http://localhost:8000/tasks/{id}/status` com `{new_status: nextStatus}`
3. Se sucesso (200):
   - Re-chamar `GET /tasks/` com filtro ativo e re-renderizar lista
4. Se erro (422/404): exibir `response.detail`; lista permanece inalterada
5. Se erro de rede: exibir "Serviço temporariamente indisponível"

---

## Fluxo 5: Deletar tarefa

**Trigger**: Usuário clica no botão "Deletar" em um card de tarefa pendente

**Ação da interface**:
1. Chamar `DELETE http://localhost:8000/tasks/{id}`
2. Se sucesso (204):
   - Re-chamar `GET /tasks/` com filtro ativo e re-renderizar lista
3. Se erro (422/404): exibir `response.detail`; lista permanece inalterada
4. Se erro de rede: exibir "Serviço temporariamente indisponível"

---

## Componentes visuais e seus estados

### Card de tarefa

```
┌──────────────────────────────────────┐
│ [Badge Status]  [Badge Prioridade]   │
│ Título da tarefa                     │  ← destaque se is_due_today
│ Descrição (se houver)                │
│ Prazo: 10 mai. 2026  [Vence hoje!]   │  ← apenas se is_due_today
│                                      │
│ [Iniciar / Concluir]   [Deletar]     │  ← conforme status
└──────────────────────────────────────┘
```

### Formulário de criação

```
┌──────────────────────────────────────┐
│ Título *  [___________________________] ← erro inline se < 3 chars
│ Descrição [___________________________]
│ Prazo     [____-__-__]
│ Prioridade [Baixa ▼]
│                          [Salvar]
│ [Área de feedback: erro / aviso]
└──────────────────────────────────────┘
```

### Área de mensagem de feedback

- Erro da API: texto em vermelho com `detail` da resposta
- Aviso de duplicidade: texto em amarelo
- Invisível quando não há mensagem ativa

### Estado vazio

```
┌──────────────────────────────────────┐
│  📋 Nenhuma tarefa encontrada.       │
│  Crie sua primeira tarefa acima.     │  ← sem filtro ativo
│  — ou —                              │
│  Nenhuma tarefa com este status.     │  ← com filtro ativo
└──────────────────────────────────────┘
```

---

## Chamadas à API — resumo

| Fluxo | Método | Endpoint | Corpo | Sucesso | Erro tratado |
|---|---|---|---|---|---|
| Carregar | GET | `/tasks/` | — | 200 | Rede |
| Filtrar | GET | `/tasks/?status=X` | — | 200 | Rede |
| Criar | POST | `/tasks/` | TaskCreate | 201 | 422, Rede |
| Avançar | PATCH | `/tasks/{id}/status` | `{new_status}` | 200 | 422, 404, Rede |
| Deletar | DELETE | `/tasks/{id}` | — | 204 | 422, 404, Rede |
