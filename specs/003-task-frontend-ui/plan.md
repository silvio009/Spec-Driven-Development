# Implementation Plan: Interface Visual de Gestão de Tarefas

**Branch**: `003-task-frontend-ui` | **Date**: 2026-05-05 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/003-task-frontend-ui/spec.md`

## Summary

Criar interface web estática (HTML + CSS + JS puro) que consome a API `002-task-rest-api`. A interface exibe a lista de tarefas em cards com badges coloridos por status, oferece formulário de criação, botões de ação por card (avançar status / deletar), filtro por status e feedback visual de erros e estados especiais (vence hoje, lista vazia, API indisponível). Toda comunicação com o backend via `fetch()` nativo.

## Technical Context

**Language/Version**: HTML5, CSS3, JavaScript ES6+
**Primary Dependencies**: Nenhuma — sem bibliotecas externas
**Storage**: Sem persistência local; estado em memória (`tasks[]`, `activeFilter`)
**Testing**: Manual via navegador (Chrome e Edge)
**Target Platform**: Navegador desktop (Chrome e Edge — versões atuais)
**Project Type**: Static web frontend (arquivo aberto diretamente no browser)
**Performance Goals**: Carregamento em < 2s, operações CRUD em < 3s (dependente da API em localhost)
**Constraints**: Sem framework JS; sem build step; sem servidor web adicional; sem mobile
**Scale/Scope**: Tela única, uso individual/pequena equipe

## Constitution Check

Constituição ainda em formato template (não preenchida). Regras do `CLAUDE.md` aplicadas:
- Separação de camadas: frontend estático totalmente separado do backend Python ✓
- Sem modificação das camadas existentes (`src/`, `tests/`) ✓
- Nomes de variáveis e funções em inglês no código JS ✓
- Nenhuma rota ou banco alterado ✓

**Resultado**: Sem violações.

## Project Structure

### Documentation (this feature)

```text
specs/003-task-frontend-ui/
├── plan.md               ← Este arquivo
├── research.md           ← Phase 0: decisões técnicas
├── data-model.md         ← Phase 1: mapeamento de dados API ↔ UI
├── quickstart.md         ← Phase 1: como abrir e validar
├── contracts/
│   └── ui-interactions.md  ← Phase 1: fluxos de interação e chamadas à API
└── tasks.md              ← Phase 2: gerado por /speckit-tasks
```

### Source Code

```text
frontend/                 ← NOVO — diretório raiz da interface
├── index.html            ← Estrutura HTML: formulário, filtros, lista, área de feedback
├── style.css             ← Estilos: badges, cards, destaque "vence hoje", estados vazios
└── app.js                ← Lógica: fetch, renderização, state, handlers de eventos

[Demais diretórios existentes — sem modificação]
src/        ← EXISTENTE
tests/      ← EXISTENTE
specs/      ← EXISTENTE
```

**Structure Decision**: Diretório `frontend/` isolado na raiz. Três arquivos separados (HTML/CSS/JS) para legibilidade. Sem build step — arquivos consumidos diretamente pelo browser.

## Complexity Tracking

Sem violações — tabela não aplicável.
