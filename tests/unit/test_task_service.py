"""Testes unitários para TaskService — todas as funções de serviço."""

from datetime import date, timedelta
from unittest.mock import MagicMock

import pytest

from src.models.task import Priority, Task, TaskStatus
from src.services.task_service import TaskService


# ---------------------------------------------------------------------------
# Fixtures compartilhadas
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_repo() -> MagicMock:
    """Repositório simulado para isolar a camada de serviço."""
    repo = MagicMock()
    repo.find_by_title_and_date.return_value = []
    repo.save.side_effect = lambda task: _task_with_id(task, 1)
    return repo


@pytest.fixture
def service(mock_repo: MagicMock) -> TaskService:
    """Instância de TaskService com repositório simulado."""
    return TaskService(mock_repo)


def _task_with_id(task: Task, task_id: int) -> Task:
    """Retorna uma cópia da tarefa com o id preenchido."""
    task.id = task_id
    return task


# ---------------------------------------------------------------------------
# US1 — Criar Tarefa
# ---------------------------------------------------------------------------

class TestCreateTask:
    """Testes para o método create_task."""

    def test_tarefa_valida_retorna_status_pendente(self, service: TaskService) -> None:
        """Cenário 1: tarefa com dados válidos deve ter status pendente."""
        task, warning = service.create_task(
            title="Revisar relatório",
            deadline=date.today() + timedelta(days=3),
        )
        assert task.status == TaskStatus.PENDENTE
        assert warning is False

    def test_titulo_muito_curto_lanca_value_error(self, service: TaskService) -> None:
        """Cenário 2: título com menos de 3 caracteres deve lançar ValueError."""
        with pytest.raises(ValueError, match="pelo menos 3"):
            service.create_task(title="AB")

    def test_prazo_no_passado_lanca_value_error(self, service: TaskService) -> None:
        """Cenário 3: prazo anterior à data atual deve lançar ValueError."""
        with pytest.raises(ValueError, match="Prazo não pode ser data passada"):
            service.create_task(
                title="Tarefa atrasada",
                deadline=date.today() - timedelta(days=1),
            )

    def test_titulo_muito_longo_lanca_value_error(self, service: TaskService) -> None:
        """Cenário 4: título com mais de 100 caracteres deve lançar ValueError."""
        titulo_longo = "A" * 101
        with pytest.raises(ValueError, match="no máximo 100"):
            service.create_task(title=titulo_longo)

    def test_titulo_duplicado_no_mesmo_dia_retorna_warning(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Cenário 5: título duplicado no mesmo dia deve retornar duplicate_warning=True."""
        mock_repo.find_by_title_and_date.return_value = [
            Task(id=1, title="Reunião de equipe")
        ]
        task, warning = service.create_task(title="Reunião de equipe")
        assert warning is True
        assert task.title == "Reunião de equipe"

    def test_prazo_hoje_retorna_is_due_today(self, service: TaskService) -> None:
        """Cenário 6: prazo igual à data atual deve marcar is_due_today como True."""
        task, _ = service.create_task(
            title="Entregar proposta",
            deadline=date.today(),
        )
        assert task.is_due_today is True

    def test_prioridade_padrao_e_media(self, service: TaskService) -> None:
        """Prioridade padrão deve ser MEDIA quando não informada."""
        task, _ = service.create_task(title="Tarefa sem prioridade")
        assert task.priority == Priority.MEDIA

    def test_prioridade_customizada_e_respeitada(self, service: TaskService) -> None:
        """Prioridade informada deve ser preservada na tarefa criada."""
        task, _ = service.create_task(title="Urgente", priority=Priority.ALTA)
        assert task.priority == Priority.ALTA


# ---------------------------------------------------------------------------
# US2 — Listar e Filtrar Tarefas
# ---------------------------------------------------------------------------

class TestListTasks:
    """Testes para o método list_tasks."""

    def test_sem_tarefas_retorna_lista_vazia(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Cenário 1: sem tarefas cadastradas deve retornar lista vazia sem erro."""
        mock_repo.find_all.return_value = []
        result = service.list_tasks()
        assert result == []

    def test_filtro_por_status_pendente(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Cenário 2: filtro por status deve retornar apenas tarefas correspondentes."""
        pendente = Task(id=1, title="Pendente", status=TaskStatus.PENDENTE)
        mock_repo.find_all.return_value = [pendente]
        result = service.list_tasks(status=TaskStatus.PENDENTE)
        mock_repo.find_all.assert_called_once_with(
            status=TaskStatus.PENDENTE, priority=None
        )
        assert all(t.status == TaskStatus.PENDENTE for t in result)

    def test_filtro_por_prioridade_alta(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Cenário 3: filtro por prioridade deve retornar apenas tarefas correspondentes."""
        alta = Task(id=1, title="Alta prioridade", priority=Priority.ALTA)
        mock_repo.find_all.return_value = [alta]
        result = service.list_tasks(priority=Priority.ALTA)
        mock_repo.find_all.assert_called_once_with(
            status=None, priority=Priority.ALTA
        )
        assert all(t.priority == Priority.ALTA for t in result)

    def test_filtros_combinados_passados_ao_repositorio(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Cenário 4: filtros combinados devem ser repassados corretamente ao repositório."""
        mock_repo.find_all.return_value = []
        service.list_tasks(status=TaskStatus.PENDENTE, priority=Priority.ALTA)
        mock_repo.find_all.assert_called_once_with(
            status=TaskStatus.PENDENTE, priority=Priority.ALTA
        )


# ---------------------------------------------------------------------------
# US3 — Atualizar Status da Tarefa
# ---------------------------------------------------------------------------

class TestUpdateTaskStatus:
    """Testes para o método update_task_status."""

    def test_pendente_para_em_andamento(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Cenário 1: transição pendente → em_andamento deve ter sucesso."""
        tarefa = Task(id=1, title="Tarefa", status=TaskStatus.PENDENTE)
        mock_repo.find_by_id.return_value = tarefa
        mock_repo.update.side_effect = lambda t: t

        result = service.update_task_status(1, TaskStatus.EM_ANDAMENTO)
        assert result.status == TaskStatus.EM_ANDAMENTO

    def test_em_andamento_para_concluida(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Cenário 2: transição em_andamento → concluida deve ter sucesso."""
        tarefa = Task(id=1, title="Tarefa", status=TaskStatus.EM_ANDAMENTO)
        mock_repo.find_by_id.return_value = tarefa
        mock_repo.update.side_effect = lambda t: t

        result = service.update_task_status(1, TaskStatus.CONCLUIDA)
        assert result.status == TaskStatus.CONCLUIDA

    def test_edicao_em_tarefa_concluida_lanca_value_error(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Cenário 3: qualquer edição em tarefa concluída deve lançar ValueError."""
        tarefa = Task(id=1, title="Tarefa", status=TaskStatus.CONCLUIDA)
        mock_repo.find_by_id.return_value = tarefa

        with pytest.raises(ValueError, match="concluída não pode ser editada"):
            service.update_task_status(1, TaskStatus.PENDENTE)

    def test_tarefa_inexistente_lanca_value_error(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Tarefa com id inexistente deve lançar ValueError."""
        mock_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="não encontrada"):
            service.update_task_status(999, TaskStatus.EM_ANDAMENTO)

    def test_transicao_invalida_lanca_value_error(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Transição não permitida deve lançar ValueError."""
        tarefa = Task(id=1, title="Tarefa", status=TaskStatus.PENDENTE)
        mock_repo.find_by_id.return_value = tarefa

        with pytest.raises(ValueError, match="Transição inválida"):
            service.update_task_status(1, TaskStatus.CONCLUIDA)


# ---------------------------------------------------------------------------
# US4 — Deletar Tarefa
# ---------------------------------------------------------------------------

class TestDeleteTask:
    """Testes para o método delete_task."""

    def test_tarefa_pendente_e_removida(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Cenário 1: tarefa com status pendente deve ser removida com sucesso."""
        tarefa = Task(id=1, title="Tarefa", status=TaskStatus.PENDENTE)
        mock_repo.find_by_id.return_value = tarefa

        service.delete_task(1)
        mock_repo.delete.assert_called_once_with(1)

    def test_tarefa_em_andamento_lanca_value_error(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Cenário 2: tarefa em andamento deve bloquear exclusão com ValueError."""
        tarefa = Task(id=1, title="Tarefa", status=TaskStatus.EM_ANDAMENTO)
        mock_repo.find_by_id.return_value = tarefa

        with pytest.raises(
            ValueError, match="Não é possível deletar tarefa em andamento"
        ):
            service.delete_task(1)

    def test_tarefa_concluida_lanca_value_error(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Cenário 3: tarefa concluída deve bloquear exclusão com ValueError."""
        tarefa = Task(id=1, title="Tarefa", status=TaskStatus.CONCLUIDA)
        mock_repo.find_by_id.return_value = tarefa

        with pytest.raises(ValueError, match="Não é possível deletar tarefa concluída"):
            service.delete_task(1)

    def test_tarefa_inexistente_lanca_value_error(
        self, service: TaskService, mock_repo: MagicMock
    ) -> None:
        """Tarefa com id inexistente deve lançar ValueError."""
        mock_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="não encontrada"):
            service.delete_task(999)
