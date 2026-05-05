# Research: Interface Visual de Gestão de Tarefas

**Feature**: 003-task-frontend-ui
**Date**: 2026-05-05
**Status**: Complete — sem NEEDS CLARIFICATION pendentes

---

## Decisão 1: Stack e ausência de framework

**Decision**: HTML5 + CSS3 + JavaScript ES6+ puro (Vanilla JS). Nenhuma biblioteca externa.
**Rationale**: Explicitamente definido na spec da feature (`feature-task-frontend.md`: "HTML + CSS + JavaScript puro — sem framework"). Elimina etapas de build, dependências npm e complexidade desnecessária para o escopo (CRUD de tarefas, tela única).
**Alternatives considered**:
- React/Vue: overhead de build e conceitos desnecessários para uma interface de uma tela.
- jQuery: dependência externa sem ganho real com ES6+ disponível nativamente.

---

## Decisão 2: Estrutura de arquivos

**Decision**: Diretório `frontend/` na raiz do projeto com três arquivos separados: `index.html`, `style.css`, `app.js`.
**Rationale**: Separação de responsabilidades mesmo em projeto simples. Um arquivo HTML único com CSS/JS inline dificulta manutenção e leitura à medida que o código cresce.
**Alternatives considered**:
- Arquivo único (`index.html` com tudo inline): mais simples de entregar mas dificulta leitura e manutenção.
- Subdivisão em múltiplos JS: desnecessário para o escopo atual.

---

## Decisão 3: Comunicação com a API

**Decision**: `fetch()` nativo do browser com `async/await`. Sem biblioteca HTTP.
**Rationale**: Fetch é padrão moderno suportado pelo Chrome e Edge atuais. Compatível com a constraint de "sem framework". `async/await` torna o fluxo legível.
**Alternatives considered**:
- XMLHttpRequest: API legada, verbosa, sem necessidade.
- axios: dependência externa desnecessária dado suporte nativo ao `fetch`.

**Padrão de tratamento de erro**: Todo `fetch` é envolvido em `try/catch`. Respostas com status ≥ 400 disparam leitura de `response.json()` para extrair `detail` e exibir ao usuário.

---

## Decisão 4: Gerenciamento de estado

**Decision**: Array de tarefas em memória (`let tasks = []`) no módulo `app.js`. Re-renderização total da lista após cada operação bem-sucedida.
**Rationale**: Para o escopo de uma tela com CRUD simples, gerenciamento de estado complexo (Redux, Signals etc.) seria over-engineering. Re-buscar ou re-renderizar a lista após cada operação garante consistência sem complexidade.
**Alternatives considered**:
- Re-fetch da API após cada operação: mais simples e garante dados frescos — adotado como padrão (atualização da lista via novo GET após cada mutação).
- Atualização local do array sem re-fetch: mais rápido mas pode dessincronizar com o estado do servidor.

**Padrão adotado**: Após cada operação de mutação (criar, avançar status, deletar), realizar novo `GET /tasks` com o filtro ativo e re-renderizar a lista.

---

## Decisão 5: Formatação de data em português

**Decision**: `Intl.DateTimeFormat('pt-BR', { day: 'numeric', month: 'short', year: 'numeric' })`.
**Rationale**: API nativa do browser, sem dependência, produz saída localizada corretamente (ex.: "10 de mai. de 2026"). Suportado pelo Chrome e Edge atuais.
**Alternatives considered**:
- date-fns com locale pt-BR: dependência desnecessária dado suporte nativo.
- Formatação manual: propensa a erro e não localizada.

---

## Decisão 6: Filtro de status

**Decision**: Botões de filtro (ou `<select>`) que mantêm o filtro ativo em variável de estado local. Ao mudar o filtro, realiza novo `GET /tasks?status=<valor>` e re-renderiza.
**Rationale**: Consistente com o padrão de re-fetch após cada operação. O servidor é a fonte da verdade do filtro, evitando lógica de filtragem duplicada no frontend.
**Alternatives considered**:
- Filtragem no frontend sobre o array local: mais rápida mas duplica lógica de negócio.

---

## Decisão 7: Destaque visual "vence hoje"

**Decision**: Verificar campo `is_due_today` retornado pela API (já calculado no backend). Aplicar classe CSS específica ao card da tarefa quando `is_due_today === true`.
**Rationale**: O campo `is_due_today` já existe no `TaskResponse` da API. Não há necessidade de calcular no frontend.
**Alternatives considered**:
- Calcular no frontend comparando `deadline` com `new Date()`: redundante e sujeito a diferença de timezone.

---

## Conclusão

Todos os pontos técnicos estão resolvidos. Nenhuma clarificação adicional necessária. Pronto para Phase 1 (design).
