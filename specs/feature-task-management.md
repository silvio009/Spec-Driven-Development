# SPEC: Gestão de Tarefas

**Status:** aprovada  
**Autor:** dev-requisitos  
**Revisado por:** dev-senior  
**Data:** 2026-05-04  

## Propósito
Permitir que colaboradores criem, organizem e acompanhem
suas tarefas diárias com controle de tempo dedicado.

## Usuários afetados
- Colaborador: cria e gerencia suas próprias tarefas
- Gestor: visualiza tarefas do time (somente leitura)

## Requisitos funcionais
1. Criar tarefa com título (obrigatório), descrição, prazo e prioridade
2. Listar tarefas com filtro por status e prioridade
3. Atualizar status: pendente → em_andamento → concluida
4. Deletar tarefa somente se status = pendente

## Regras de negócio
- Título: mínimo 3, máximo 100 caracteres
- Prazo não pode ser data passada
- Prioridade: baixa | media | alta (padrão: media)
- Tarefa concluída não pode ser editada
- Deletar tarefa em andamento é bloqueado

## Edge cases
- Título duplicado no mesmo dia: permitir com aviso
- Prazo hoje: permitir, marcar como "vence hoje"
- Usuário sem tarefas: retornar lista vazia, não erro

## Critérios de aceite (Given/When/Then)

**Cenário 1 — Criar tarefa válida**  
Given título com pelo menos 3 caracteres e prazo futuro  
When chamar create_task()  
Then retorna tarefa com status=pendente  

**Cenário 2 — Título muito curto**  
Given título com menos de 3 caracteres  
When chamar create_task()  
Then lança ValueError com mensagem clara  

**Cenário 3 — Prazo no passado**  
Given data anterior a hoje  
When chamar create_task()  
Then lança ValueError "Prazo não pode ser data passada"  

**Cenário 4 — Deletar tarefa em andamento**  
Given tarefa com status=em_andamento  
When chamar delete_task()  
Then lança ValueError "Não é possível deletar tarefa em andamento"  

## Fora do escopo desta spec
- Autenticação e usuários
- Notificações e lembretes
- Interface web ou API REST