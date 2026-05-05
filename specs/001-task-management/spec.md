# Feature Specification: Gestão de Tarefas

**Feature Branch**: `001-task-management`
**Created**: 2026-05-04
**Status**: Draft
**Input**: Permitir que colaboradores criem, organizem e acompanhem suas tarefas diárias com controle de tempo dedicado.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Criar Tarefa (Priority: P1)

O colaborador cria uma nova tarefa informando título (obrigatório), descrição opcional, prazo e prioridade. O sistema valida as regras de negócio e registra a tarefa com status inicial `pendente`.

**Why this priority**: É a ação fundacional do sistema — sem criação de tarefas, nenhum outro fluxo pode ser exercitado. Entrega valor imediato ao colaborador.

**Independent Test**: Pode ser testado isoladamente fornecendo dados válidos e verificando que a tarefa é registrada com status `pendente`.

**Acceptance Scenarios**:

1. **Given** um título com pelo menos 3 caracteres e prazo futuro, **When** o colaborador cria a tarefa, **Then** o sistema registra a tarefa com status `pendente` e prioridade `media` como padrão.
2. **Given** um título com menos de 3 caracteres, **When** o colaborador tenta criar a tarefa, **Then** o sistema rejeita a operação com mensagem de erro clara sobre o comprimento mínimo do título.
3. **Given** um prazo com data anterior à data atual, **When** o colaborador tenta criar a tarefa, **Then** o sistema rejeita a operação com a mensagem "Prazo não pode ser data passada".
4. **Given** um título com mais de 100 caracteres, **When** o colaborador tenta criar a tarefa, **Then** o sistema rejeita a operação com mensagem de erro sobre o limite máximo do título.
5. **Given** um título já utilizado por outra tarefa no mesmo dia, **When** o colaborador cria a tarefa, **Then** o sistema registra a tarefa normalmente e exibe um aviso informando a duplicidade.
6. **Given** um prazo igual à data de hoje, **When** o colaborador cria a tarefa, **Then** o sistema registra a tarefa e a sinaliza como "vence hoje".

---

### User Story 2 - Listar e Filtrar Tarefas (Priority: P2)

O colaborador visualiza suas tarefas com a possibilidade de filtrar por status e/ou prioridade, facilitando o foco nas atividades mais relevantes.

**Why this priority**: Sem listagem eficiente, o colaborador perde visibilidade sobre suas tarefas, comprometendo a organização. Depende de P1 (existência de tarefas).

**Independent Test**: Pode ser testado criando tarefas com diferentes status e prioridades e verificando que os filtros retornam apenas os registros correspondentes.

**Acceptance Scenarios**:

1. **Given** um colaborador sem nenhuma tarefa cadastrada, **When** solicita a listagem, **Then** o sistema retorna uma lista vazia sem erro.
2. **Given** tarefas com status variados, **When** o colaborador filtra por `pendente`, **Then** o sistema retorna apenas as tarefas com status `pendente`.
3. **Given** tarefas com prioridades variadas, **When** o colaborador filtra por `alta`, **Then** o sistema retorna apenas as tarefas com prioridade `alta`.
4. **Given** filtros combinados de status e prioridade, **When** o colaborador aplica ambos, **Then** o sistema retorna apenas as tarefas que atendem aos dois critérios.

---

### User Story 3 - Atualizar Status da Tarefa (Priority: P3)

O colaborador avança o status de uma tarefa seguindo o fluxo linear: `pendente` → `em_andamento` → `concluida`. O sistema impede transições inválidas e edições em tarefas concluídas.

**Why this priority**: Permite acompanhar o progresso das tarefas. Depende de P1 (existência de tarefas).

**Independent Test**: Pode ser testado criando uma tarefa e aplicando transições de status em sequência, verificando bloqueios nos casos indevidos.

**Acceptance Scenarios**:

1. **Given** uma tarefa com status `pendente`, **When** o colaborador atualiza para `em_andamento`, **Then** o sistema registra o novo status com sucesso.
2. **Given** uma tarefa com status `em_andamento`, **When** o colaborador atualiza para `concluida`, **Then** o sistema registra o novo status com sucesso.
3. **Given** uma tarefa com status `concluida`, **When** o colaborador tenta editar qualquer campo, **Then** o sistema rejeita a operação informando que tarefas concluídas não podem ser editadas.

---

### User Story 4 - Deletar Tarefa (Priority: P4)

O colaborador remove uma tarefa do sistema. A exclusão só é permitida para tarefas com status `pendente`; tarefas em andamento ou concluídas são protegidas contra exclusão.

**Why this priority**: Completa o ciclo CRUD. Depende de P1 e P3 para os cenários de bloqueio.

**Independent Test**: Pode ser testado criando tarefas em diferentes status e tentando deletar cada uma, verificando os bloqueios esperados.

**Acceptance Scenarios**:

1. **Given** uma tarefa com status `pendente`, **When** o colaborador solicita a exclusão, **Then** o sistema remove a tarefa com sucesso.
2. **Given** uma tarefa com status `em_andamento`, **When** o colaborador solicita a exclusão, **Then** o sistema rejeita a operação com a mensagem "Não é possível deletar tarefa em andamento".
3. **Given** uma tarefa com status `concluida`, **When** o colaborador solicita a exclusão, **Then** o sistema rejeita a operação.

---

### Edge Cases

- O que acontece quando o título é duplicado no mesmo dia? → Permitido com exibição de aviso ao colaborador.
- O que acontece quando o prazo é exatamente hoje? → Permitido; tarefa é sinalizada como "vence hoje".
- O que acontece quando o colaborador não tem tarefas? → Retorna lista vazia sem erro.
- O que acontece com prazo no passado? → Criação é bloqueada com mensagem de erro.
- O que acontece ao tentar deletar tarefa em andamento? → Operação bloqueada com mensagem de erro.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE permitir a criação de tarefas com título (obrigatório), descrição (opcional), prazo (opcional) e prioridade (opcional, padrão `media`).
- **FR-002**: O sistema DEVE validar que o título da tarefa tenha entre 3 e 100 caracteres.
- **FR-003**: O sistema DEVE rejeitar tarefas com prazo anterior à data atual.
- **FR-004**: O sistema DEVE registrar toda tarefa criada com status inicial `pendente`.
- **FR-005**: O sistema DEVE suportar três níveis de prioridade: `baixa`, `media` e `alta`.
- **FR-006**: O sistema DEVE permitir a listagem de tarefas com filtro por status e/ou prioridade.
- **FR-007**: O sistema DEVE retornar lista vazia (sem erro) quando o colaborador não possuir tarefas.
- **FR-008**: O sistema DEVE permitir a atualização de status seguindo o fluxo: `pendente` → `em_andamento` → `concluida`.
- **FR-009**: O sistema DEVE impedir qualquer edição em tarefas com status `concluida`.
- **FR-010**: O sistema DEVE permitir a exclusão somente de tarefas com status `pendente`.
- **FR-011**: O sistema DEVE bloquear a exclusão de tarefas com status `em_andamento` com mensagem de erro descritiva.
- **FR-012**: O sistema DEVE emitir aviso (sem bloquear) quando o título da nova tarefa já existir em outra tarefa registrada no mesmo dia.
- **FR-013**: O sistema DEVE sinalizar como "vence hoje" tarefas cujo prazo seja igual à data atual.

### Key Entities

- **Tarefa**: Unidade central de trabalho. Atributos: título (texto, 3–100 caracteres), descrição (texto, opcional), prazo (data, opcional, não pode ser passado), prioridade (`baixa` | `media` | `alta`), status (`pendente` | `em_andamento` | `concluida`).

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O colaborador consegue criar uma tarefa válida em menos de 1 minuto do início ao registro confirmado.
- **SC-002**: 100% das regras de negócio (validações de título, prazo, fluxo de status e permissões de exclusão) são aplicadas automaticamente pelo sistema, sem intervenção manual.
- **SC-003**: A aplicação de filtros por status e/ou prioridade retorna apenas os registros correspondentes, com 0% de falsos positivos.
- **SC-004**: Nenhuma tarefa com status `em_andamento` ou `concluida` é excluída acidentalmente pelo sistema.
- **SC-005**: O sistema responde a todas as operações de criação, listagem, atualização e exclusão de forma perceptivelmente instantânea para o colaborador em condições normais de uso.

---

## Assumptions

- O sistema não inclui autenticação ou controle de usuários nesta versão; o escopo é a lógica de negócio de tarefas.
- Notificações e lembretes de prazo estão fora do escopo desta spec.
- Interface web ou API REST estão fora do escopo desta spec; apenas a camada de serviço/negócio é especificada.
- O gestor tem acesso somente leitura às tarefas do time; a implementação do perfil do gestor não é parte desta spec.
- "Mesmo dia" para detecção de título duplicado refere-se à data de criação da tarefa (sem considerar hora).
- A transição de status é estritamente linear e unidirecional; retroceder status não é permitido.
- A data de referência para validação de prazo é sempre a data atual do sistema no momento da operação.
