# Data Model: Interface Visual de Gestão de Tarefas

**Feature**: 003-task-frontend-ui
**Date**: 2026-05-05
**Depende de**: `002-task-rest-api` — TaskResponse, TaskCreateResponse

---

## Dados recebidos da API (leitura)

### TaskResponse (mapeado de `GET /tasks` e `PATCH /tasks/{id}/status`)

| Campo | Tipo JS | Uso na interface |
|---|---|---|
| `id` | `number` | Identificador para ações (avançar, deletar) |
| `title` | `string` | Exibido no card da tarefa |
| `description` | `string \| null` | Exibido abaixo do título (se presente) |
| `deadline` | `string \| null` | Formatado em português via `Intl.DateTimeFormat` |
| `priority` | `"baixa" \| "media" \| "alta"` | Badge/ícone de prioridade |
| `status` | `"pendente" \| "em_andamento" \| "concluida"` | Badge colorido + visibilidade dos botões |
| `created_at` | `string` | Não exibido (usado internamente se necessário) |
| `is_due_today` | `boolean` | Classe CSS de destaque quando `true` |

### TaskCreateResponse (mapeado de `POST /tasks`)

Herda todos os campos de `TaskResponse` e adiciona:

| Campo | Tipo JS | Uso na interface |
|---|---|---|
| `duplicate_warning` | `boolean` | Exibe aviso de duplicidade quando `true` |

---

## Dados enviados à API (escrita)

### Payload de criação (`POST /tasks`)

| Campo | Campo do formulário | Tipo | Obrigatório |
|---|---|---|---|
| `title` | Input texto | `string` | Sim (min 3 chars — validado no frontend antes do envio) |
| `description` | Textarea | `string \| null` | Não |
| `deadline` | Input date | `string (YYYY-MM-DD) \| null` | Não |
| `priority` | Select | `"baixa" \| "media" \| "alta" \| null` | Não |

### Payload de atualização de status (`PATCH /tasks/{id}/status`)

| Campo | Valor | Observação |
|---|---|---|
| `new_status` | Próximo status calculado | `pendente` → `em_andamento` → `concluida` |

---

## Estado local (em memória — `app.js`)

| Variável | Tipo | Descrição |
|---|---|---|
| `tasks` | `TaskResponse[]` | Lista atual de tarefas (sincronizada com a API) |
| `activeFilter` | `string \| null` | Filtro de status ativo (`null` = todos) |

---

## Mapeamento visual de status

| Valor da API | Texto exibido | Classe CSS | Cor |
|---|---|---|---|
| `pendente` | Pendente | `.badge--pendente` | Cinza |
| `em_andamento` | Em andamento | `.badge--em-andamento` | Azul |
| `concluida` | Concluída | `.badge--concluida` | Verde |

## Mapeamento visual de prioridade

| Valor da API | Texto/ícone |
|---|---|
| `baixa` | ↓ Baixa |
| `media` | → Média |
| `alta` | ↑ Alta |

## Lógica de exibição de botões por status

| Status | Botão "Avançar" | Botão "Deletar" |
|---|---|---|
| `pendente` | Exibido ("Iniciar") | Exibido |
| `em_andamento` | Exibido ("Concluir") | Oculto |
| `concluida` | Oculto | Oculto |

## Próximo status por transição

| Status atual | Próximo status enviado à API |
|---|---|
| `pendente` | `em_andamento` |
| `em_andamento` | `concluida` |
