# Feature Specification: API de Gestão de Tarefas

**Feature Branch**: `002-task-rest-api`
**Created**: 2026-05-05
**Status**: Draft
**Depende de**: `001-task-management`
**Input**: Expor o serviço de gestão de tarefas via interface remota para que frontends e clientes externos possam consumir as funcionalidades sem acesso direto ao sistema interno.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Registrar Nova Tarefa Remotamente (Priority: P1)

Um cliente externo (frontend ou sistema integrado) envia os dados de uma nova tarefa e recebe a confirmação do registro com os dados completos da tarefa criada. Todas as regras de negócio da gestão de tarefas são aplicadas da mesma forma que no sistema interno.

**Why this priority**: É a operação fundacional da integração — sem a capacidade de criar tarefas remotamente, todas as demais operações perdem sentido. Entrega valor imediato ao frontend e a sistemas integrados.

**Independent Test**: Pode ser testado isoladamente enviando dados válidos de uma tarefa e verificando o retorno com os dados da tarefa registrada e confirmação de sucesso.

**Acceptance Scenarios**:

1. **Given** um cliente externo com dados válidos (título com 3–100 caracteres e prazo futuro), **When** solicita o registro de uma nova tarefa, **Then** o sistema registra a tarefa com status `pendente` e retorna os dados completos da tarefa criada com confirmação de sucesso.
2. **Given** um cliente externo com título de 2 caracteres, **When** solicita o registro, **Then** o sistema rejeita a operação e retorna mensagem de erro em português indicando o problema de validação do título.
3. **Given** um cliente externo com prazo anterior à data atual, **When** solicita o registro, **Then** o sistema rejeita a operação e retorna a mensagem "Prazo não pode ser data passada".
4. **Given** um cliente externo com título de mais de 100 caracteres, **When** solicita o registro, **Then** o sistema rejeita a operação com mensagem de erro sobre o limite máximo do título.
5. **Given** um cliente externo com dados malformados (estrutura inválida), **When** solicita o registro, **Then** o sistema rejeita a operação indicando que o formato dos dados enviados é inválido.
6. **Given** um cliente externo com título já utilizado por outra tarefa no mesmo dia, **When** solicita o registro, **Then** o sistema registra a tarefa e retorna os dados da tarefa criada junto com um aviso de duplicidade.

---

### User Story 2 - Consultar e Filtrar Tarefas Remotamente (Priority: P2)

Um cliente externo consulta a lista de tarefas registradas, podendo filtrar por status e/ou prioridade para obter apenas as informações relevantes para exibição ou processamento.

**Why this priority**: Sem consulta remota, o frontend não consegue exibir as tarefas ao usuário. Depende de P1 para ter dados a consultar.

**Independent Test**: Pode ser testado criando tarefas com diferentes combinações de status e prioridade e verificando que os filtros retornam apenas os registros correspondentes.

**Acceptance Scenarios**:

1. **Given** um cliente externo sem nenhuma tarefa cadastrada no sistema, **When** solicita a listagem, **Then** o sistema retorna uma lista vazia com confirmação de sucesso (sem erro).
2. **Given** um cliente externo com tarefas de status variados, **When** solicita a listagem filtrando por `pendente`, **Then** o sistema retorna apenas as tarefas com status `pendente`.
3. **Given** um cliente externo com tarefas de prioridades variadas, **When** solicita a listagem filtrando por `alta`, **Then** o sistema retorna apenas as tarefas com prioridade `alta`.
4. **Given** um cliente externo aplicando filtros combinados de status e prioridade, **When** solicita a listagem, **Then** o sistema retorna apenas as tarefas que atendem a ambos os critérios simultaneamente.
5. **Given** um cliente externo com valor de status inválido no filtro, **When** solicita a listagem, **Then** o sistema rejeita a operação com mensagem de erro indicando os valores aceitos.

---

### User Story 3 - Avançar Status de Tarefa Remotamente (Priority: P3)

Um cliente externo atualiza o status de uma tarefa específica, avançando-a no fluxo linear `pendente` → `em_andamento` → `concluida`. O sistema impede transições inválidas e protege tarefas concluídas.

**Why this priority**: Permite que o frontend reflita o progresso real das tarefas. Depende de P1 para existência de tarefas.

**Independent Test**: Pode ser testado criando uma tarefa e aplicando as transições de status em sequência via interface remota, verificando os bloqueios nos casos indevidos.

**Acceptance Scenarios**:

1. **Given** uma tarefa com status `pendente` identificada pelo seu código único, **When** o cliente externo solicita a atualização para `em_andamento`, **Then** o sistema registra o novo status e retorna os dados atualizados da tarefa.
2. **Given** uma tarefa com status `em_andamento`, **When** o cliente externo solicita a atualização para `concluida`, **Then** o sistema registra o novo status e retorna os dados atualizados.
3. **Given** uma tarefa com status `concluida`, **When** o cliente externo solicita qualquer atualização de status, **Then** o sistema rejeita a operação informando que tarefas concluídas não podem ser editadas.
4. **Given** um código de tarefa que não existe no sistema, **When** o cliente externo solicita a atualização de status, **Then** o sistema retorna indicação de que o recurso não foi encontrado.
5. **Given** um valor de status inválido (fora dos permitidos), **When** o cliente externo solicita a atualização, **Then** o sistema rejeita a operação com mensagem de erro indicando os valores aceitos.

---

### User Story 4 - Remover Tarefa Remotamente (Priority: P4)

Um cliente externo solicita a remoção de uma tarefa específica. A exclusão só é permitida para tarefas com status `pendente`; tarefas em andamento ou concluídas são protegidas.

**Why this priority**: Completa o ciclo de operações remotas. Depende de P1 e P3 para os cenários de bloqueio.

**Independent Test**: Pode ser testado criando tarefas em diferentes status e tentando removê-las via interface remota, verificando os bloqueios esperados.

**Acceptance Scenarios**:

1. **Given** uma tarefa com status `pendente` identificada pelo seu código único, **When** o cliente externo solicita a remoção, **Then** o sistema remove a tarefa e confirma o sucesso da operação.
2. **Given** uma tarefa com status `em_andamento`, **When** o cliente externo solicita a remoção, **Then** o sistema rejeita a operação com a mensagem "Não é possível deletar tarefa em andamento".
3. **Given** uma tarefa com status `concluida`, **When** o cliente externo solicita a remoção, **Then** o sistema rejeita a operação.
4. **Given** um código de tarefa que não existe no sistema, **When** o cliente externo solicita a remoção, **Then** o sistema retorna indicação de que o recurso não foi encontrado.

---

### Edge Cases

- O que acontece quando o identificador da tarefa não existe? → Operação rejeitada com indicação de recurso não encontrado.
- O que acontece quando os dados enviados têm formato inválido (estrutura quebrada)? → Operação rejeitada com indicação de dados inválidos.
- O que acontece quando um valor de status inválido é enviado no filtro ou na atualização? → Operação rejeitada com mensagem listando os valores aceitos.
- O que acontece ao tentar remover tarefa em andamento? → Operação bloqueada com mensagem de erro descritiva.
- O que acontece ao solicitar listagem sem nenhuma tarefa cadastrada? → Retorna lista vazia sem erro.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE expor uma operação remota para registrar novas tarefas, aceitando título (obrigatório), descrição (opcional), prazo (opcional) e prioridade (opcional, padrão `media`).
- **FR-002**: O sistema DEVE aplicar todas as regras de negócio de criação de tarefa (validação de título, prazo, duplicidade) ao receber solicitações remotas.
- **FR-003**: O sistema DEVE retornar os dados completos da tarefa criada após um registro bem-sucedido.
- **FR-004**: O sistema DEVE expor uma operação remota para listar tarefas com filtro opcional por status e/ou prioridade.
- **FR-005**: O sistema DEVE retornar lista vazia (sem erro) quando não houver tarefas cadastradas.
- **FR-006**: O sistema DEVE expor uma operação remota para atualizar o status de uma tarefa específica, respeitando o fluxo `pendente` → `em_andamento` → `concluida`.
- **FR-007**: O sistema DEVE expor uma operação remota para remover tarefas, permitindo exclusão apenas de tarefas com status `pendente`.
- **FR-008**: O sistema DEVE retornar indicação de recurso não encontrado quando o identificador da tarefa não existir.
- **FR-009**: O sistema DEVE retornar indicação de erro de negócio com mensagem em português quando uma regra de negócio for violada.
- **FR-010**: O sistema DEVE retornar indicação de dados inválidos quando o formato da solicitação for malformado.
- **FR-011**: O sistema DEVE retornar todas as respostas em formato estruturado legível por máquina.
- **FR-012**: O sistema DEVE expor documentação interativa das operações disponíveis acessível via navegador.

### Key Entities

- **Tarefa**: Unidade central de trabalho exposta remotamente. Atributos: identificador único, título (3–100 caracteres), descrição (opcional), prazo (opcional, não pode ser passado), prioridade (`baixa` | `media` | `alta`), status (`pendente` | `em_andamento` | `concluida`).
- **Resposta de Erro**: Estrutura retornada em caso de falha. Contém mensagem descritiva em português e identificação do tipo de erro (negócio, não encontrado, dados inválidos).

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% das operações de gestão de tarefas são acessíveis remotamente sem necessidade de acesso direto ao sistema interno.
- **SC-002**: 100% das regras de negócio da gestão de tarefas (validações, fluxo de status, restrições de exclusão) são preservadas quando acessadas remotamente, sem exceções.
- **SC-003**: Clientes externos recebem mensagens de erro em português que identificam claramente o motivo da falha em 100% dos casos de erro.
- **SC-004**: Nenhuma tarefa em andamento ou concluída é removida acidentalmente via interface remota.
- **SC-005**: Qualquer cliente capaz de fazer requisições HTTP consegue consumir todas as operações sem conhecimento da implementação interna do sistema.
- **SC-006**: A documentação interativa das operações está disponível e acessível sem configuração adicional.

---

## Assumptions

- Não há autenticação ou controle de acesso nesta versão; qualquer cliente pode consumir as operações.
- Paginação da listagem está fora do escopo desta spec; todos os registros são retornados na consulta.
- Interface visual está fora do escopo; apenas a interface de integração remota é especificada.
- As regras de negócio já implementadas em `001-task-management` são reutilizadas sem modificação.
- O identificador único da tarefa é gerado automaticamente pelo sistema no momento do registro.
- Filtros de listagem são opcionais e independentes; podem ser usados individualmente ou combinados.
- A transição de status via interface remota segue o mesmo fluxo unidirecional definido em `001-task-management`.
- "Dados malformados" refere-se a qualquer estrutura de requisição que não corresponda ao formato esperado, independentemente do conteúdo dos campos.
