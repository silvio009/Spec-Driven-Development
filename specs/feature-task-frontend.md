# SPEC: Frontend — Gestão de Tarefas

**Status:** aprovada  
**Autor:** dev-requisitos  
**Revisado por:** dev-senior  
**Data:** 2026-05-05  
**Depende de:** 002-task-rest-api  

## Propósito
Fornecer uma interface visual simples e funcional
para que colaboradores gerenciem suas tarefas
diretamente no navegador.

## Usuários afetados
- Colaborador: cria, visualiza e gerencia tarefas
  pela interface web

## Requisitos funcionais
1. Exibir lista de tarefas cadastradas
2. Formulário para criar nova tarefa
3. Botão para atualizar status da tarefa
4. Botão para deletar tarefa pendente
5. Filtrar tarefas por status

## Regras de negócio
- Interface consome exclusivamente a API REST da 002
- Erros da API exibidos como mensagem visível ao usuário
- Lista atualizada automaticamente após cada operação
- Tarefa com "vence hoje" destacada visualmente

## Key Entities

### Tarefa exibida na interface
- title: texto visível
- status: badge colorido (pendente=cinza, em_andamento=azul, concluida=verde)
- priority: ícone ou badge (baixa, media, alta)
- due_date: data formatada em português
- is_due_today: destaque visual especial

## Edge cases
- API indisponível: exibir mensagem "Serviço temporariamente indisponível"
- Lista vazia: exibir estado vazio com mensagem orientativa
- Erro ao criar tarefa: exibir mensagem de erro sem fechar o formulário
- Título muito curto: exibir erro inline no campo antes de enviar

## Critérios de aceite (Given/When/Then)

**Cenário 1 — Visualizar tarefas**  
Given existem tarefas cadastradas na API  
When o usuário acessa a página  
Then a lista de tarefas é exibida corretamente  

**Cenário 2 — Criar tarefa**  
Given o formulário está preenchido corretamente  
When o usuário clica em salvar  
Then tarefa aparece na lista sem recarregar a página  

**Cenário 3 — API indisponível**  
Given a API está fora do ar  
When o usuário acessa a página  
Then exibe mensagem de erro amigável  

**Cenário 4 — Lista vazia**  
Given nenhuma tarefa cadastrada  
When o usuário acessa a página  
Then exibe estado vazio com orientação para criar a primeira tarefa  

## Success Criteria
- Interface funciona nos navegadores Chrome e Edge
- Todas as operações CRUD funcionam via API
- Erros da API são exibidos de forma clara
- Página carrega em menos de 2 segundos

## Assumptions
- API REST da 002 está funcionando e acessível em localhost:8000
- Interface será HTML + CSS + JavaScript puro — sem framework
- Sem autenticação nesta versão
- Compatibilidade apenas com navegadores modernos

## Fora do escopo desta spec
- Autenticação e login
- Versão mobile responsiva
- Temas ou personalização visual