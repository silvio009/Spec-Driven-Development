"""Testes de integração para TaskRepository com banco SQLite em memória."""

from datetime import date, timedelta

import pytest

from src.database import create_schema, get_connection
from src.models.task import Priority, Task, TaskStatus
from src.repositories.task_repository import TaskRepository


@pytest.fixture
def repo() -> TaskRepository:
    """Repositório com banco SQLite em memória para cada teste."""
    conn = get_connection(":memory:")
    create_schema(conn)
    return TaskRepository(conn)


def _sample_task(title: str = "Tarefa de teste") -> Task:
    """Retorna uma tarefa de exemplo pronta para salvar."""
    return Task(
        title=title,
        description="Descrição de teste",
        deadline=date.today() + timedelta(days=7),
        priority=Priority.MEDIA,
        status=TaskStatus.PENDENTE,
        created_at=date.today(),
    )


class TestSave:
    """Testes para o método save."""

    def test_save_retorna_tarefa_com_id(self, repo: TaskRepository) -> None:
        """Tarefa salva deve ter id preenchido pelo banco."""
        task = repo.save(_sample_task())
        assert task.id is not None
        assert task.id > 0

    def test_save_preserva_campos(self, repo: TaskRepository) -> None:
        """Dados da tarefa devem ser preservados após a persistência."""
        original = _sample_task("Verificar relatório")
        saved = repo.save(original)
        assert saved.title == "Verificar relatório"
        assert saved.priority == Priority.MEDIA
        assert saved.status == TaskStatus.PENDENTE


class TestFindAll:
    """Testes para o método find_all."""

    def test_find_all_sem_tarefas_retorna_lista_vazia(
        self, repo: TaskRepository
    ) -> None:
        """Banco vazio deve retornar lista vazia sem erro."""
        assert repo.find_all() == []

    def test_find_all_retorna_todas_as_tarefas(self, repo: TaskRepository) -> None:
        """Sem filtro deve retornar todas as tarefas cadastradas."""
        repo.save(_sample_task("Tarefa 1"))
        repo.save(_sample_task("Tarefa 2"))
        result = repo.find_all()
        assert len(result) == 2

    def test_find_all_filtra_por_status(self, repo: TaskRepository) -> None:
        """Filtro por status deve retornar apenas tarefas correspondentes."""
        pendente = repo.save(_sample_task("Pendente"))
        em_andamento = repo.save(_sample_task("Em andamento"))
        em_andamento.status = TaskStatus.EM_ANDAMENTO
        repo.update(em_andamento)

        result = repo.find_all(status=TaskStatus.PENDENTE)
        assert all(t.status == TaskStatus.PENDENTE for t in result)
        assert any(t.id == pendente.id for t in result)

    def test_find_all_filtra_por_prioridade(self, repo: TaskRepository) -> None:
        """Filtro por prioridade deve retornar apenas tarefas correspondentes."""
        alta = _sample_task("Alta")
        alta.priority = Priority.ALTA
        repo.save(alta)
        repo.save(_sample_task("Média"))

        result = repo.find_all(priority=Priority.ALTA)
        assert all(t.priority == Priority.ALTA for t in result)
        assert len(result) == 1


class TestFindById:
    """Testes para o método find_by_id."""

    def test_find_by_id_retorna_tarefa(self, repo: TaskRepository) -> None:
        """Busca por id existente deve retornar a tarefa correta."""
        saved = repo.save(_sample_task())
        found = repo.find_by_id(saved.id)
        assert found is not None
        assert found.id == saved.id
        assert found.title == saved.title

    def test_find_by_id_inexistente_retorna_none(self, repo: TaskRepository) -> None:
        """Busca por id inexistente deve retornar None."""
        assert repo.find_by_id(999) is None


class TestFindByTitleAndDate:
    """Testes para o método find_by_title_and_date."""

    def test_encontra_tarefa_com_mesmo_titulo_e_data(
        self, repo: TaskRepository
    ) -> None:
        """Deve encontrar tarefa com mesmo título e data de criação."""
        repo.save(_sample_task("Reunião"))
        result = repo.find_by_title_and_date("Reunião", date.today())
        assert len(result) == 1
        assert result[0].title == "Reunião"

    def test_nao_encontra_titulo_diferente(self, repo: TaskRepository) -> None:
        """Não deve retornar tarefas com título diferente."""
        repo.save(_sample_task("Tarefa A"))
        result = repo.find_by_title_and_date("Tarefa B", date.today())
        assert result == []


class TestUpdate:
    """Testes para o método update."""

    def test_update_persiste_novo_status(self, repo: TaskRepository) -> None:
        """Atualização de status deve ser persistida no banco."""
        task = repo.save(_sample_task())
        task.status = TaskStatus.EM_ANDAMENTO
        repo.update(task)

        retrieved = repo.find_by_id(task.id)
        assert retrieved.status == TaskStatus.EM_ANDAMENTO


class TestDelete:
    """Testes para o método delete."""

    def test_delete_remove_tarefa(self, repo: TaskRepository) -> None:
        """Tarefa deletada não deve ser encontrada pelo id."""
        task = repo.save(_sample_task())
        repo.delete(task.id)
        assert repo.find_by_id(task.id) is None

    def test_delete_nao_afeta_outras_tarefas(self, repo: TaskRepository) -> None:
        """Deletar uma tarefa não deve afetar as demais."""
        task1 = repo.save(_sample_task("Tarefa 1"))
        task2 = repo.save(_sample_task("Tarefa 2"))
        repo.delete(task1.id)

        assert repo.find_by_id(task1.id) is None
        assert repo.find_by_id(task2.id) is not None
