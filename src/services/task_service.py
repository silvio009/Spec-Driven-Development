"""Camada de serviço para gestão de tarefas — regras de negócio."""

from datetime import date

from src.models.task import Priority, Task, TaskStatus
from src.repositories.task_repository import TaskRepository

# Transições de status permitidas (máquina de estados unidirecional)
VALID_TRANSITIONS: dict[TaskStatus, list[TaskStatus]] = {
    TaskStatus.PENDENTE: [TaskStatus.EM_ANDAMENTO],
    TaskStatus.EM_ANDAMENTO: [TaskStatus.CONCLUIDA],
    TaskStatus.CONCLUIDA: [],
}


class TaskService:
    """Serviço de negócio para criação, listagem, atualização e exclusão de tarefas.

    Todas as regras de negócio da spec estão encapsuladas nesta classe.
    Nenhuma lógica de negócio deve existir fora desta camada.
    """

    def __init__(self, repository: TaskRepository) -> None:
        """Inicializa o serviço com um repositório de tarefas.

        Args:
            repository: Repositório responsável pela persistência das tarefas.
        """
        self._repo = repository

    def create_task(
        self,
        title: str,
        description: str | None = None,
        deadline: date | None = None,
        priority: Priority = Priority.MEDIA,
    ) -> tuple[Task, bool]:
        """Cria uma nova tarefa com status inicial pendente.

        Valida as regras de negócio antes de persistir. Detecta títulos
        duplicados no mesmo dia e sinaliza via o segundo elemento do retorno.

        Args:
            title: Título da tarefa. Obrigatório; entre 3 e 100 caracteres.
            description: Descrição opcional sem restrição de tamanho.
            deadline: Prazo de conclusão. Não pode ser data anterior à atual.
            priority: Nível de prioridade. Padrão: MEDIA.

        Returns:
            Tupla (task, duplicate_warning) onde duplicate_warning é True se
            já existe outra tarefa com o mesmo título criada hoje.

        Raises:
            ValueError: Se o título não respeitar os limites de tamanho.
            ValueError: Se o prazo for uma data anterior à data atual.
        """
        self._validate_title(title)
        self._validate_deadline(deadline)

        today = date.today()
        duplicates = self._repo.find_by_title_and_date(title, today)
        duplicate_warning = len(duplicates) > 0

        task = Task(
            title=title,
            description=description,
            deadline=deadline,
            priority=priority,
            status=TaskStatus.PENDENTE,
            created_at=today,
        )
        saved_task = self._repo.save(task)
        return saved_task, duplicate_warning

    def list_tasks(
        self,
        status: TaskStatus | None = None,
        priority: Priority | None = None,
    ) -> list[Task]:
        """Retorna as tarefas com filtragem opcional por status e/ou prioridade.

        Nunca lança exceção quando não há tarefas — retorna lista vazia.

        Args:
            status: Filtro por status. None retorna todos os status.
            priority: Filtro por prioridade. None retorna todas as prioridades.

        Returns:
            Lista de tarefas correspondentes aos filtros. Pode ser vazia.
        """
        return self._repo.find_all(status=status, priority=priority)

    def update_task_status(self, task_id: int, new_status: TaskStatus) -> Task:
        """Avança o status de uma tarefa seguindo o fluxo unidirecional.

        Fluxo permitido: pendente → em_andamento → concluida.
        Tarefas concluídas são imutáveis e rejeitem qualquer atualização.

        Args:
            task_id: Identificador da tarefa a ser atualizada.
            new_status: Novo status desejado.

        Returns:
            A tarefa com o status atualizado.

        Raises:
            ValueError: Se a tarefa não for encontrada.
            ValueError: Se a tarefa estiver concluída (imutável).
            ValueError: Se a transição de status não for permitida.
        """
        task = self._get_task_or_raise(task_id)

        if task.status == TaskStatus.CONCLUIDA:
            raise ValueError("Tarefa concluída não pode ser editada.")

        allowed = VALID_TRANSITIONS.get(task.status, [])
        if new_status not in allowed:
            raise ValueError(
                f"Transição inválida: '{task.status.value}' → '{new_status.value}'. "
                f"Transições permitidas: {[s.value for s in allowed] or 'nenhuma'}."
            )

        task.status = new_status
        return self._repo.update(task)

    def delete_task(self, task_id: int) -> None:
        """Remove permanentemente uma tarefa com status pendente.

        Tarefas em andamento ou concluídas são protegidas contra exclusão.

        Args:
            task_id: Identificador da tarefa a ser removida.

        Raises:
            ValueError: Se a tarefa não for encontrada.
            ValueError: Se a tarefa estiver em andamento.
            ValueError: Se a tarefa estiver concluída.
        """
        task = self._get_task_or_raise(task_id)

        if task.status == TaskStatus.EM_ANDAMENTO:
            raise ValueError("Não é possível deletar tarefa em andamento.")

        if task.status == TaskStatus.CONCLUIDA:
            raise ValueError("Não é possível deletar tarefa concluída.")

        self._repo.delete(task_id)

    # ---------------------------------------------------------------------------
    # Métodos auxiliares privados
    # ---------------------------------------------------------------------------

    def _validate_title(self, title: str) -> None:
        """Valida os limites de tamanho do título da tarefa.

        Args:
            title: Título a ser validado.

        Raises:
            ValueError: Se o título tiver menos de 3 ou mais de 100 caracteres.
        """
        if len(title) < 3:
            raise ValueError(
                "O título deve ter pelo menos 3 caracteres. "
                f"Recebido: {len(title)} caractere(s)."
            )
        if len(title) > 100:
            raise ValueError(
                "O título deve ter no máximo 100 caracteres. "
                f"Recebido: {len(title)} caractere(s)."
            )

    def _validate_deadline(self, deadline: date | None) -> None:
        """Valida que o prazo não seja uma data anterior à data atual.

        Args:
            deadline: Prazo a ser validado. None é aceito (prazo opcional).

        Raises:
            ValueError: Se o prazo for anterior à data atual.
        """
        if deadline is not None and deadline < date.today():
            raise ValueError("Prazo não pode ser data passada.")

    def _get_task_or_raise(self, task_id: int) -> Task:
        """Busca uma tarefa pelo id ou lança ValueError se não encontrada.

        Args:
            task_id: Identificador da tarefa.

        Returns:
            A tarefa encontrada.

        Raises:
            ValueError: Se nenhuma tarefa for encontrada com o id informado.
        """
        task = self._repo.find_by_id(task_id)
        if task is None:
            raise ValueError(f"Tarefa não encontrada: id={task_id}.")
        return task
