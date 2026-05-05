/* ============================================================
   Time Manager — Frontend
   Vanilla JS, sem framework, sem dependências externas.
   Consome a API REST em API_BASE.
   ============================================================ */

const API_BASE = 'http://localhost:8000';

// Estado local
let tasks = [];
let activeFilter = null;

// ============================================================
// Utilitários
// ============================================================

/**
 * Envolve fetch em try/catch e extrai erros da API de forma padronizada.
 * Lança um Error com a mensagem `detail` da API ou erro de rede.
 *
 * @param {string} path - Caminho relativo (ex.: '/tasks/')
 * @param {RequestInit} [options] - Opções do fetch
 * @returns {Promise<any|null>} - JSON da resposta ou null para 204
 */
async function apiFetch(path, options = {}) {
  const response = await fetch(API_BASE + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (response.status === 204) return null;

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Erro desconhecido da API.');
  }

  return data;
}

/**
 * Formata uma string de data ISO para o formato abreviado em português.
 * Retorna null se dateStr for null ou undefined.
 *
 * @param {string|null} dateStr - Data no formato YYYY-MM-DD
 * @returns {string|null}
 */
function formatDate(dateStr) {
  if (!dateStr) return null;
  const [year, month, day] = dateStr.split('-').map(Number);
  const date = new Date(year, month - 1, day);
  return new Intl.DateTimeFormat('pt-BR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(date);
}

/**
 * Exibe uma mensagem no elemento de feedback do formulário.
 *
 * @param {string} message
 * @param {'error'|'warning'} type
 */
function showFormFeedback(message, type = 'error') {
  const el = document.getElementById('form-feedback');
  el.textContent = message;
  el.className = `feedback-message feedback-message--${type}`;
}

/** Limpa a mensagem de feedback do formulário. */
function clearFormFeedback() {
  const el = document.getElementById('form-feedback');
  el.textContent = '';
  el.className = 'feedback-message';
}

/**
 * Exibe uma mensagem no feedback global (ações de card).
 * Some automaticamente após 5 segundos.
 *
 * @param {string} message
 */
function showGlobalFeedback(message) {
  const el = document.getElementById('feedback');
  el.textContent = message;
  clearTimeout(el._timeout);
  el._timeout = setTimeout(() => { el.textContent = ''; }, 5000);
}

// ============================================================
// Renderização (US1)
// ============================================================

/** Mapeia status da API para texto exibido ao colaborador. */
const STATUS_LABEL = {
  pendente: 'Pendente',
  em_andamento: 'Em andamento',
  concluida: 'Concluída',
};

/** Mapeia prioridade para texto com ícone. */
const PRIORITY_LABEL = {
  baixa: '↓ Baixa',
  media: '→ Média',
  alta: '↑ Alta',
};

/**
 * Gera o HTML de um botão de avançar status para a tarefa.
 *
 * @param {object} task
 * @returns {string} HTML do botão ou string vazia
 */
function renderAdvanceButton(task) {
  if (task.status === 'pendente') {
    return `<button class="btn btn--sm btn--advance btn-advance"
               data-id="${task.id}" data-next="em_andamento">Iniciar</button>`;
  }
  if (task.status === 'em_andamento') {
    return `<button class="btn btn--sm btn--advance btn-advance"
               data-id="${task.id}" data-next="concluida">Concluir</button>`;
  }
  return '';
}

/**
 * Gera o HTML do botão de deletar para tarefas pendentes.
 *
 * @param {object} task
 * @returns {string} HTML do botão ou string vazia
 */
function renderDeleteButton(task) {
  if (task.status === 'pendente') {
    return `<button class="btn btn--sm btn--delete btn-delete"
               data-id="${task.id}">Deletar</button>`;
  }
  return '';
}

/**
 * Renderiza a lista de tarefas no DOM.
 * Exibe estado vazio quando não há tarefas.
 */
function renderTaskList() {
  const listEl = document.getElementById('task-list');
  const emptyEl = document.getElementById('empty-state');
  const emptyHint = document.getElementById('empty-hint');

  // Limpa cards anteriores (preserva o empty-state)
  Array.from(listEl.children).forEach(child => {
    if (child.id !== 'empty-state') child.remove();
  });

  if (tasks.length === 0) {
    emptyEl.hidden = false;
    emptyHint.textContent = activeFilter
      ? 'Nenhuma tarefa com este status.'
      : 'Crie sua primeira tarefa acima.';
    return;
  }

  emptyEl.hidden = true;

  tasks.forEach(task => {
    const card = document.createElement('article');
    card.className = 'task-card' + (task.is_due_today ? ' task-card--due-today' : '');

    const deadline = formatDate(task.deadline);
    const dueTodayBadge = task.is_due_today
      ? '<span class="due-today-badge">⚠ Vence hoje!</span>'
      : '';

    card.innerHTML = `
      <div class="task-card__header">
        <span class="badge badge--${task.status}">${STATUS_LABEL[task.status]}</span>
        <span class="task-card__title">${escapeHtml(task.title)}</span>
        <span class="priority-badge">${PRIORITY_LABEL[task.priority] || ''}</span>
      </div>
      ${task.description
        ? `<p class="task-card__description">${escapeHtml(task.description)}</p>`
        : ''}
      <div class="task-card__meta">
        ${deadline ? `<span>📅 ${deadline} ${dueTodayBadge}</span>` : dueTodayBadge}
      </div>
      <div class="task-card__actions">
        ${renderAdvanceButton(task)}
        ${renderDeleteButton(task)}
      </div>
    `;

    listEl.appendChild(card);
  });
}

/**
 * Escapa caracteres HTML para prevenir XSS.
 *
 * @param {string} str
 * @returns {string}
 */
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ============================================================
// Carregamento de dados (US1)
// ============================================================

/**
 * Busca tarefas na API aplicando o filtro de status ativo,
 * atualiza o estado local e re-renderiza a lista.
 */
async function loadTasks() {
  try {
    const query = activeFilter ? `?status=${activeFilter}` : '';
    tasks = await apiFetch(`/tasks/${query}`);
    renderTaskList();
  } catch (err) {
    showGlobalFeedback('Serviço temporariamente indisponível.');
    tasks = [];
    renderTaskList();
  }
}

// ============================================================
// Criação de tarefa (US2)
// ============================================================

/** Lê e valida os campos do formulário, então cria a tarefa via API. */
async function handleCreateTask() {
  const titleEl = document.getElementById('title');
  const titleErrorEl = document.getElementById('title-error');
  const title = titleEl.value.trim();

  // Validação frontend
  if (title.length < 3) {
    titleErrorEl.textContent = 'O título deve ter pelo menos 3 caracteres.';
    titleEl.focus();
    return;
  }
  titleErrorEl.textContent = '';

  const description = document.getElementById('description').value.trim() || null;
  const deadline = document.getElementById('deadline').value || null;
  const priority = document.getElementById('priority').value || null;

  clearFormFeedback();

  try {
    const result = await apiFetch('/tasks/', {
      method: 'POST',
      body: JSON.stringify({ title, description, deadline, priority }),
    });

    // Limpar formulário
    titleEl.value = '';
    document.getElementById('description').value = '';
    document.getElementById('deadline').value = '';
    document.getElementById('priority').value = '';

    if (result.duplicate_warning) {
      showFormFeedback('Aviso: já existe uma tarefa com este título hoje.', 'warning');
    }

    await loadTasks();
  } catch (err) {
    showFormFeedback(err.message);
  }
}

// ============================================================
// Filtro de status (US3)
// ============================================================

/**
 * Atualiza o filtro ativo, destaca o botão e recarrega a lista.
 *
 * @param {string} filterValue - Valor do filtro ('pendente', 'em_andamento', 'concluida' ou '')
 */
async function handleFilterChange(filterValue) {
  activeFilter = filterValue || null;

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.toggle('filter-btn--active', btn.dataset.filter === filterValue);
  });

  await loadTasks();
}

// ============================================================
// Avançar status (US4)
// ============================================================

/**
 * Avança o status de uma tarefa para o próximo no fluxo.
 *
 * @param {string} taskId
 * @param {string} nextStatus
 */
async function handleAdvanceStatus(taskId, nextStatus) {
  try {
    await apiFetch(`/tasks/${taskId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ new_status: nextStatus }),
    });
    await loadTasks();
  } catch (err) {
    showGlobalFeedback(err.message);
  }
}

// ============================================================
// Deletar tarefa (US5)
// ============================================================

/**
 * Remove uma tarefa pendente pelo seu id.
 *
 * @param {string} taskId
 */
async function handleDeleteTask(taskId) {
  try {
    await apiFetch(`/tasks/${taskId}`, { method: 'DELETE' });
    await loadTasks();
  } catch (err) {
    showGlobalFeedback(err.message);
  }
}

// ============================================================
// Inicialização e event wiring
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
  // US2 — botão salvar
  document.getElementById('btn-save').addEventListener('click', handleCreateTask);

  // US2 — submit com Enter no campo título
  document.getElementById('title').addEventListener('keydown', e => {
    if (e.key === 'Enter') handleCreateTask();
  });

  // US3 — filtros
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => handleFilterChange(btn.dataset.filter));
  });

  // US4 + US5 — event delegation na lista
  document.getElementById('task-list').addEventListener('click', e => {
    if (e.target.matches('.btn-advance')) {
      handleAdvanceStatus(e.target.dataset.id, e.target.dataset.next);
    }
    if (e.target.matches('.btn-delete')) {
      handleDeleteTask(e.target.dataset.id);
    }
  });

  // US1 — carregamento inicial
  loadTasks();
});
