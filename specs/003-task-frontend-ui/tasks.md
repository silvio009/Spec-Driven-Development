# Tasks: Interface Visual de Gestão de Tarefas

**Input**: Design documents from `specs/003-task-frontend-ui/`
**Prerequisites**: plan.md ✓ spec.md ✓ research.md ✓ data-model.md ✓ contracts/ui-interactions.md ✓

**Tests**: Validação manual no navegador — sem framework de testes automatizados (projeto estático puro).

**Organization**: Tasks agrupadas por user story. Os três arquivos (`index.html`, `style.css`, `app.js`) são construídos incrementalmente — cada fase adiciona funcionalidade sem quebrar o que já existe.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Pode rodar em paralelo (arquivos diferentes, sem dependências pendentes)
- **[Story]**: User story correspondente da spec.md (US1–US5)
- Caminhos exatos de arquivo incluídos em todas as tasks

---

## Phase 1: Setup

**Purpose**: Criar o diretório da interface

- [x] T001 Create `frontend/` directory with empty placeholder files: `frontend/index.html`, `frontend/style.css`, `frontend/app.js`

---

## Phase 2: Foundational (Estrutura base — bloqueia todas as user stories)

**Purpose**: Esqueleto HTML, variáveis CSS e estado + helper de fetch em JS — DEVEM existir antes de qualquer funcionalidade

**⚠️ CRÍTICO**: Nenhuma user story pode ser implementada antes desta fase estar completa

- [x] T002 Create base `frontend/index.html`: `<head>` com `<link rel="stylesheet" href="style.css">`, `<body>` com seções semânticas vazias — `<header>` com título, `<section id="form-section">`, `<nav id="filter-bar">`, `<main id="task-list">`, `<div id="feedback">`, `<script src="app.js">` ao final do body
- [x] T003 [P] Create base `frontend/style.css`: CSS reset (`box-sizing`, `margin`, `padding`), variáveis de cor (`:root` com `--color-pendente`, `--color-em-andamento`, `--color-concluida`, `--color-due-today`), container centralizado (`max-width: 800px`, `margin: auto`, `padding: 1rem`), tipografia base
- [x] T004 [P] Create `frontend/app.js` skeleton: `const API_BASE = 'http://localhost:8000'`, `let tasks = []`, `let activeFilter = null`; função `apiFetch(path, options)` que envolve `fetch` em `try/catch`, verifica `response.ok`, extrai `response.json()` ou lança erro com `data.detail`; listener `DOMContentLoaded` que chama `loadTasks()`

**Checkpoint**: Abrir `frontend/index.html` no Chrome — página abre sem erros no console (estrutura vazia)

---

## Phase 3: User Story 1 - Visualizar Lista de Tarefas (Priority: P1) 🎯 MVP

**Goal**: Colaborador acessa a página e vê a lista de tarefas com badges coloridos, indicador de prioridade, prazo formatado e destaque para "vence hoje"

**Independent Test**: Com API rodando e tarefas cadastradas, abrir `index.html` → lista exibida com badges corretos; sem tarefas → estado vazio orientativo; API parada → "Serviço temporariamente indisponível"

### Implementação

- [x] T005 [US1] Implement `formatDate(dateStr)` in `frontend/app.js`: use `Intl.DateTimeFormat('pt-BR', {day:'numeric', month:'short', year:'numeric'})` to format ISO date string; return `null` if `dateStr` is null
- [x] T006 [US1] Implement `renderTaskList()` in `frontend/app.js`: clear `#task-list`, show `#empty-state` if `tasks` is empty; for each task generate card HTML with: title, description (if present), `is_due_today` class on card, status badge with CSS class matching `badge--{status}`, priority badge, formatted deadline, action buttons placeholder (empty for now — added in US4/US5)
- [x] T007 [US1] Implement `loadTasks()` in `frontend/app.js`: call `apiFetch('/tasks/' + (activeFilter ? '?status=' + activeFilter : ''))`, assign result to `tasks`, call `renderTaskList()`; on error show "Serviço temporariamente indisponível" in `#feedback`
- [x] T008 [US1] Add task card and badge styles to `frontend/style.css`: `.task-card` (border, padding, margin-bottom, border-radius), `.task-card--due-today` (border-left with `--color-due-today`, background highlight), `.badge` base, `.badge--pendente` (cinza), `.badge--em-andamento` (azul), `.badge--concluida` (verde), `.priority-badge`, `#empty-state` (centered text, muted color)

**Checkpoint**: Lista de tarefas exibida corretamente; badge cinza/azul/verde por status; "vence hoje" destacado; estado vazio com mensagem; erro de rede com mensagem amigável

---

## Phase 4: User Story 2 - Criar Nova Tarefa (Priority: P2)

**Goal**: Colaborador preenche o formulário e a tarefa aparece na lista sem recarregar a página; erros de validação e da API exibidos inline

**Independent Test**: Preencher título válido → tarefa aparece na lista; título com 2 chars → erro inline sem chamada à API; prazo passado → mensagem de erro da API sem fechar formulário

### Implementação

- [x] T009 [US2] Add creation form HTML to `frontend/index.html` inside `<section id="form-section">`: `<input id="title" required>` com `<span id="title-error" class="field-error">`, `<textarea id="description">`, `<input type="date" id="deadline">`, `<select id="priority">` com opções baixa/media/alta, `<button id="btn-save">Salvar</button>`, `<div id="form-feedback" class="feedback-message">` para erros/avisos da API
- [x] T010 [US2] Implement `handleCreateTask()` in `frontend/app.js`: ler valores dos campos; validar `title.length < 3` → mostrar `#title-error`, return sem enviar; chamar `apiFetch('/tasks/', {method:'POST', body: JSON.stringify({title, description, deadline, priority})})` com `Content-Type: application/json`; sucesso → limpar campos, exibir aviso se `duplicate_warning`, chamar `loadTasks()`; erro → exibir `detail` em `#form-feedback` sem fechar formulário
- [x] T011 [US2] Wire `#btn-save` click event to `handleCreateTask()` in `frontend/app.js` inside `DOMContentLoaded`
- [x] T012 [US2] Add form styles to `frontend/style.css`: `#form-section` (padding, background, border-radius), `.form-field` (label + input layout), `.field-error` (vermelho, font-size pequeno), `.feedback-message` (base), `.feedback-message--error` (vermelho), `.feedback-message--warning` (amarelo), `#btn-save` (estilo de botão primário)

**Checkpoint**: Criação com dados válidos → tarefa na lista; título curto → erro inline; prazo passado → mensagem da API preservando campos; duplicidade → aviso + tarefa criada

---

## Phase 5: User Story 3 - Filtrar Tarefas por Status (Priority: P3)

**Goal**: Colaborador clica em um filtro de status e a lista atualiza imediatamente sem recarregar a página

**Independent Test**: Com tarefas de status variados, clicar "Pendente" → apenas pendentes; clicar "Todos" → todas retornam; filtro sem resultados → estado vazio específico

### Implementação

- [x] T013 [US3] Add filter bar HTML to `frontend/index.html` inside `<nav id="filter-bar">`: quatro botões com `data-filter` — `data-filter=""` (Todos), `data-filter="pendente"` (Pendente), `data-filter="em_andamento"` (Em andamento), `data-filter="concluida"` (Concluída)
- [x] T014 [US3] Implement `handleFilterChange(filterValue)` in `frontend/app.js`: set `activeFilter = filterValue || null`, update active class on filter buttons (remove `.filter-btn--active` de todos, add to clicked), call `loadTasks()`
- [x] T015 [US3] Wire filter buttons click events in `frontend/app.js` inside `DOMContentLoaded`: `querySelectorAll('[data-filter]')` → each button adds click listener calling `handleFilterChange(btn.dataset.filter)`
- [x] T016 [US3] Add filter styles to `frontend/style.css`: `#filter-bar` (display flex, gap, margin), `.filter-btn` (base botão secundário), `.filter-btn--active` (cor de destaque, font-weight bold)

**Checkpoint**: Cada filtro exibe somente tarefas do status correspondente; botão ativo destacado; filtro sem resultados exibe estado vazio

---

## Phase 6: User Story 4 - Avançar Status de Tarefa (Priority: P4)

**Goal**: Colaborador clica em "Iniciar" ou "Concluir" no card e o badge de status atualiza imediatamente; botão ausente em tarefas concluídas

**Independent Test**: Tarefa pendente → botão "Iniciar" visível; clicar → badge muda para azul; tarefa em andamento → botão "Concluir"; tarefa concluída → nenhum botão de avanço

### Implementação

- [x] T017 [US4] Add advance-status button to card template in `renderTaskList()` in `frontend/app.js`: for `pendente` render `<button class="btn-advance" data-id="{id}" data-next="em_andamento">Iniciar</button>`; for `em_andamento` render `<button class="btn-advance" data-id="{id}" data-next="concluida">Concluir</button>`; for `concluida` render nothing
- [x] T018 [US4] Implement `handleAdvanceStatus(taskId, nextStatus)` in `frontend/app.js`: call `apiFetch('/tasks/' + taskId + '/status', {method:'PATCH', body: JSON.stringify({new_status: nextStatus})})` with `Content-Type: application/json`; success → call `loadTasks()`; error → show `detail` in `#feedback`
- [x] T019 [US4] Wire `.btn-advance` click events via event delegation on `#task-list` in `frontend/app.js`: `task-list.addEventListener('click', e => { if (e.target.matches('.btn-advance')) handleAdvanceStatus(e.target.dataset.id, e.target.dataset.next) })`
- [x] T020 [US4] Add advance button styles to `frontend/style.css`: `.btn-advance` (botão pequeno, estilo secundário/outline)

**Checkpoint**: "Iniciar" muda badge de cinza para azul; "Concluir" muda de azul para verde; tarefa concluída não exibe botão; erro de API exibido sem alterar lista

---

## Phase 7: User Story 5 - Deletar Tarefa Pendente (Priority: P5)

**Goal**: Colaborador clica em "Deletar" no card de tarefa pendente e a tarefa desaparece imediatamente; botão ausente em tarefas não-pendentes

**Independent Test**: Tarefa pendente → botão "Deletar" visível; clicar → tarefa some da lista; tarefa em andamento/concluída → sem botão deletar

### Implementação

- [x] T021 [US5] Add delete button to card template in `renderTaskList()` in `frontend/app.js`: for `pendente` render `<button class="btn-delete" data-id="{id}">Deletar</button>`; for other statuses render nothing
- [x] T022 [US5] Implement `handleDeleteTask(taskId)` in `frontend/app.js`: call `apiFetch('/tasks/' + taskId, {method:'DELETE'})`; success → call `loadTasks()`; error → show `detail` in `#feedback`
- [x] T023 [US5] Wire `.btn-delete` click via event delegation on `#task-list` in `frontend/app.js`: `if (e.target.matches('.btn-delete')) handleDeleteTask(e.target.dataset.id)`
- [x] T024 [US5] Add delete button styles to `frontend/style.css`: `.btn-delete` (botão pequeno, estilo destrutivo/vermelho outline)

**Checkpoint**: Tarefa pendente deletada → desaparece da lista; tarefa em andamento/concluída sem botão deletar; erro da API exibido sem remover tarefa

---

## Phase 8: Polish & Cross-Cutting

**Purpose**: Validação end-to-end e ajustes finais de UX

- [x] T025 [P] Validate all 5 user stories end-to-end in Chrome following `specs/003-task-frontend-ui/quickstart.md`: criar, listar, filtrar, avançar status, deletar
- [x] T026 [P] Test error scenarios: stop API server → reload page → verify "Serviço temporariamente indisponível"; restart API → verify recovery on next action
- [x] T027 Clear `#feedback` message automatically after 5 seconds on success operations — add `setTimeout(() => { feedback.textContent = '' }, 5000)` after each successful action in `frontend/app.js`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sem dependências — pode iniciar imediatamente
- **Foundational (Phase 2)**: Depende de Phase 1 — **BLOQUEIA todas as user stories**
- **US1 (Phase 3)**: Depende de Foundational — implementar primeiro (é o MVP)
- **US2–US5 (Phases 4–7)**: Dependem de US1 (renderTaskList existe); podem ser sequenciais P2→P3→P4→P5
- **Polish (Phase 8)**: Depende de todas as user stories desejadas

### User Story Dependencies

- **US1 (P1)**: Após Foundational — cria `renderTaskList()` e `loadTasks()` usados por todos
- **US2 (P2)**: Após US1 — adiciona formulário; independente de US3/US4/US5
- **US3 (P3)**: Após US1 — usa `loadTasks()` com filtro; independente de US2/US4/US5
- **US4 (P4)**: Após US1 — adiciona botão ao card em `renderTaskList()`; independente de US2/US3
- **US5 (P5)**: Após US1 — adiciona botão ao card em `renderTaskList()`; independente de US2/US3

> **Nota**: US4 e US5 editam a mesma função `renderTaskList()` em `app.js` — executar sequencialmente para evitar conflito.

### Within Each User Story

- HTML → JS → CSS (estrutura antes da lógica, lógica antes do estilo)
- Cada story é completamente funcional ao final de sua fase

### Parallel Opportunities

- T003, T004 (Phase 2): paralelas entre si (arquivos diferentes: `style.css` e `app.js`)
- T025, T026 (Phase 8): paralelas entre si (validações independentes)

---

## Parallel Example: Foundational (Phase 2)

```
Agente A: T003 — frontend/style.css (estilos base, variáveis)
Agente B: T004 — frontend/app.js (skeleton, apiFetch, state)

→ Após ambos concluírem: T002 — frontend/index.html (estrutura HTML)
```

---

## Implementation Strategy

### MVP (User Story 1 apenas)

1. Concluir Phase 1: Setup
2. Concluir Phase 2: Foundational (HTML base + CSS base + app.js skeleton)
3. Concluir Phase 3: US1 — lista de tarefas funcionando
4. **PARAR e VALIDAR**: abrir `index.html` → lista exibida corretamente com badges
5. Demo/validação antes de continuar

### Entrega Incremental

1. Setup + Foundational → página abre sem erros
2. US1 → lista de tarefas visível → MVP!
3. US2 → criação via formulário
4. US3 → filtro por status
5. US4 → avançar status inline
6. US5 → deletar tarefa inline
7. Polish → validação end-to-end e mensagens de feedback com auto-clear

---

## Notes

- [P] tasks = arquivos diferentes, sem dependências pendentes entre si
- [Story] label conecta cada task à user story da spec.md
- `app.js` cresce incrementalmente — cada phase adiciona funções novas (exceto US4/US5 que editam `renderTaskList()`)
- `style.css` cresce incrementalmente — cada phase adiciona classes novas sem conflito
- Event delegation em `#task-list` (US4/US5) é necessário porque os cards são renderizados dinamicamente
- CORS: como o frontend abre como arquivo local (`file://`) e a API está em `localhost:8000`, o FastAPI precisa ter CORS habilitado para `*` ou `null` origin — verificar se necessário durante Phase 3
