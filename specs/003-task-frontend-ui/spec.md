# Feature Specification: Interface Visual de Gestão de Tarefas

**Feature Branch**: `003-task-frontend-ui`
**Created**: 2026-05-05
**Status**: Draft
**Depende de**: `002-task-rest-api`
**Input**: Fornecer uma interface visual simples para que colaboradores gerenciem suas tarefas diretamente no navegador, consumindo a API REST já existente.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visualizar Lista de Tarefas (Priority: P1)

O colaborador acessa a página e visualiza todas as tarefas cadastradas em uma lista clara. Cada tarefa exibe título, status com badge colorido, prioridade e prazo. Tarefas que vencem hoje são destacadas visualmente. Quando não há tarefas cadastradas, a interface exibe uma mensagem orientativa para criação da primeira tarefa.

**Why this priority**: É a tela principal — sem a listagem, nenhuma outra interação faz sentido. É o ponto de entrada de todos os fluxos.

**Independent Test**: Pode ser testado acessando a página com tarefas cadastradas na API e verificando que a lista é exibida com os badges corretos por status e o destaque para tarefas que vencem hoje.

**Acceptance Scenarios**:

1. **Given** existem tarefas cadastradas na API, **When** o colaborador acessa a página, **Then** a lista de tarefas é exibida com título, badge de status colorido (cinza=pendente, azul=em andamento, verde=concluída), indicador de prioridade e prazo formatado em português.
2. **Given** não há tarefas cadastradas, **When** o colaborador acessa a página, **Then** a interface exibe estado vazio com mensagem orientando a criação da primeira tarefa.
3. **Given** existe uma tarefa cujo prazo é hoje, **When** a lista é exibida, **Then** essa tarefa recebe um destaque visual diferenciado das demais.
4. **Given** a API está indisponível, **When** o colaborador acessa a página, **Then** a interface exibe a mensagem "Serviço temporariamente indisponível" sem quebrar a página.

---

### User Story 2 - Criar Nova Tarefa (Priority: P2)

O colaborador preenche um formulário com título (obrigatório), descrição, prazo e prioridade para registrar uma nova tarefa. O formulário valida o comprimento mínimo do título antes do envio. Após criação bem-sucedida, a tarefa aparece na lista sem recarregar a página. Erros da API são exibidos inline sem fechar o formulário.

**Why this priority**: A criação é a operação que alimenta a lista — sem ela, a visualização permanece vazia.

**Independent Test**: Pode ser testado preenchendo o formulário com dados válidos e verificando que a nova tarefa aparece na lista imediatamente após a confirmação.

**Acceptance Scenarios**:

1. **Given** o formulário está preenchido com título válido (mínimo 3 caracteres), **When** o colaborador clica em salvar, **Then** a tarefa é criada e aparece no topo da lista sem recarregar a página.
2. **Given** o campo título está com menos de 3 caracteres, **When** o colaborador tenta salvar, **Then** a interface exibe um erro inline no campo título sem enviar a requisição à API.
3. **Given** a API retorna erro de negócio (ex.: prazo no passado), **When** o colaborador tenta salvar, **Then** a mensagem de erro da API é exibida de forma clara sem fechar o formulário.
4. **Given** o campo título está com aviso de duplicidade retornado pela API, **When** a tarefa é criada, **Then** a interface exibe o aviso de duplicidade e ainda assim adiciona a tarefa à lista.
5. **Given** o formulário foi salvo com sucesso, **When** a tarefa aparece na lista, **Then** os campos do formulário são limpos para permitir nova entrada.

---

### User Story 3 - Filtrar Tarefas por Status (Priority: P3)

O colaborador filtra a lista de tarefas por status (pendente, em andamento, concluída) para focar nas atividades relevantes ao momento. A filtragem é imediata, sem recarregar a página.

**Why this priority**: Essencial para usabilidade quando há muitas tarefas — sem filtro, a lista se torna difícil de navegar. Depende de P1.

**Independent Test**: Pode ser testado com tarefas de status variados, aplicando cada filtro e verificando que apenas as tarefas correspondentes são exibidas.

**Acceptance Scenarios**:

1. **Given** existem tarefas com status variados, **When** o colaborador seleciona o filtro "Pendente", **Then** apenas as tarefas com status pendente são exibidas.
2. **Given** o filtro "Em andamento" está ativo, **When** o colaborador seleciona "Todos", **Then** todas as tarefas voltam a ser exibidas.
3. **Given** o filtro está ativo e não há tarefas com aquele status, **When** a lista é exibida, **Then** aparece o estado vazio específico para o filtro selecionado.

---

### User Story 4 - Avançar Status de Tarefa (Priority: P4)

O colaborador avança o status de uma tarefa diretamente na lista, usando um botão de ação. O botão só é exibido para tarefas que ainda podem avançar (pendente e em andamento). Após a atualização, o badge de status é atualizado na lista sem recarregar a página.

**Why this priority**: Permite acompanhar o progresso das tarefas. Depende de P1 para existência de tarefas.

**Independent Test**: Pode ser testado clicando no botão de avanço de uma tarefa pendente e verificando que o badge muda para "em andamento" sem recarregar.

**Acceptance Scenarios**:

1. **Given** uma tarefa com status pendente, **When** o colaborador clica no botão de avançar status, **Then** o badge da tarefa muda para "em andamento" imediatamente.
2. **Given** uma tarefa com status em andamento, **When** o colaborador clica no botão de avançar status, **Then** o badge muda para "concluída".
3. **Given** uma tarefa com status concluída, **When** a lista é exibida, **Then** o botão de avançar status não é exibido para essa tarefa.
4. **Given** a API retorna erro ao tentar avançar o status, **When** o colaborador clica no botão, **Then** a mensagem de erro é exibida e o badge permanece inalterado.

---

### User Story 5 - Deletar Tarefa Pendente (Priority: P5)

O colaborador remove uma tarefa pendente diretamente da lista. O botão de deletar só é visível para tarefas com status pendente. Após exclusão, a tarefa desaparece da lista sem recarregar a página. Erros da API são exibidos sem remover a tarefa da lista.

**Why this priority**: Completa o ciclo de gerenciamento. Depende de P1.

**Independent Test**: Pode ser testado clicando no botão deletar de uma tarefa pendente e verificando que ela desaparece da lista imediatamente.

**Acceptance Scenarios**:

1. **Given** uma tarefa com status pendente, **When** o colaborador clica no botão deletar, **Then** a tarefa é removida da lista imediatamente sem recarregar a página.
2. **Given** uma tarefa com status em andamento ou concluída, **When** a lista é exibida, **Then** o botão deletar não é exibido para essa tarefa.
3. **Given** a API retorna erro ao tentar deletar, **When** o colaborador clica no botão, **Then** a mensagem de erro é exibida e a tarefa permanece na lista.

---

### Edge Cases

- O que acontece quando a API está indisponível ao carregar a página? → Exibe mensagem "Serviço temporariamente indisponível" sem quebrar a interface.
- O que acontece quando a lista está vazia (sem filtro)? → Exibe estado vazio com orientação para criar a primeira tarefa.
- O que acontece quando o filtro ativo não retorna nenhuma tarefa? → Exibe estado vazio específico para o filtro selecionado.
- O que acontece ao tentar criar com título abaixo de 3 caracteres? → Erro inline no campo, requisição não enviada à API.
- O que acontece quando a API retorna erro durante criação, avanço de status ou exclusão? → Mensagem de erro visível; estado da lista permanece inalterado.
- O que acontece com aviso de duplicidade na criação? → Tarefa é criada e exibida; aviso é mostrado ao colaborador.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE exibir a lista de tarefas ao carregar a página, consumindo os dados da API de gestão de tarefas.
- **FR-002**: O sistema DEVE exibir cada tarefa com título, badge de status colorido, indicador de prioridade e prazo formatado em português.
- **FR-003**: O sistema DEVE aplicar destaque visual diferenciado em tarefas cujo prazo é o dia atual.
- **FR-004**: O sistema DEVE exibir estado vazio orientativo quando não há tarefas (sem filtro ativo) ou quando o filtro não retorna resultados.
- **FR-005**: O sistema DEVE exibir mensagem "Serviço temporariamente indisponível" quando a API não responde.
- **FR-006**: O sistema DEVE oferecer formulário para criação de tarefa com campos: título (obrigatório), descrição (opcional), prazo (opcional) e prioridade (opcional).
- **FR-007**: O sistema DEVE validar que o título tem pelo menos 3 caracteres antes de enviar à API, exibindo erro inline no campo.
- **FR-008**: O sistema DEVE atualizar a lista automaticamente após cada operação bem-sucedida (criar, avançar status, deletar) sem recarregar a página completa.
- **FR-009**: O sistema DEVE exibir erros retornados pela API de forma visível ao colaborador sem fechar formulários ou remover itens da lista.
- **FR-010**: O sistema DEVE exibir aviso de duplicidade de título quando a API sinalizar, mantendo a tarefa na lista.
- **FR-011**: O sistema DEVE oferecer filtro por status (todos, pendente, em andamento, concluída) aplicado imediatamente, sem recarregar a página.
- **FR-012**: O sistema DEVE exibir botão de avançar status apenas para tarefas com status pendente ou em andamento.
- **FR-013**: O sistema DEVE exibir botão de deletar apenas para tarefas com status pendente.
- **FR-014**: O sistema DEVE limpar os campos do formulário após criação bem-sucedida.

### Key Entities

- **Tarefa (exibida)**: título, status (com badge colorido: cinza=pendente, azul=em andamento, verde=concluída), prioridade (indicador visual), prazo (formatado em português, ex.: "10 mai. 2026"), destaque quando vence hoje.
- **Formulário de criação**: título (campo texto, validação mínimo 3 chars), descrição (campo texto livre), prazo (seletor de data), prioridade (seletor: baixa / média / alta).
- **Filtro de status**: seletor com opções "Todos", "Pendente", "Em andamento", "Concluída".
- **Mensagem de feedback**: área visível para erros da API, avisos (duplicidade) e confirmações.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O colaborador visualiza a lista completa de tarefas em menos de 2 segundos após acessar a página em condições normais de rede.
- **SC-002**: 100% das operações (criar, filtrar, avançar status, deletar) são concluídas sem recarregar a página.
- **SC-003**: 100% dos erros retornados pela API são exibidos de forma legível ao colaborador, sem mensagens técnicas ou tela em branco.
- **SC-004**: O colaborador consegue criar uma tarefa e vê-la aparecer na lista em menos de 3 segundos após clicar em salvar.
- **SC-005**: A interface funciona corretamente nos navegadores Chrome e Edge (versões atuais).
- **SC-006**: Tarefas que vencem hoje são identificadas visualmente pelo colaborador sem necessidade de leitura do prazo.

---

## Assumptions

- A API REST (`002-task-rest-api`) está disponível em `http://localhost:8000` durante o uso da interface.
- A interface será entregue como arquivo(s) estáticos acessíveis via navegador — sem servidor de aplicação adicional.
- Compatibilidade limitada a navegadores modernos (Chrome e Edge atuais); navegadores legados estão fora do escopo.
- Versão mobile responsiva está fora do escopo; a interface é projetada para telas de desktop.
- Autenticação e controle de acesso estão fora do escopo desta versão.
- A ordenação das tarefas na lista segue a ordem retornada pela API, sem ordenação adicional na interface.
- O formulário de criação fica sempre visível na página (não é um modal ou página separada).
- "Avançar status" realiza sempre o próximo passo do fluxo (`pendente` → `em andamento` → `concluída`); a interface não expõe escolha do status destino.
- O prazo é exibido no formato abreviado em português (ex.: "10 mai. 2026").
