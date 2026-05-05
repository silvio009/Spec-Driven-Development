"""Fábrica de dependências para injeção via FastAPI Depends."""

from collections.abc import Generator

from src.database import create_schema, get_connection
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService


def get_task_service() -> Generator[TaskService, None, None]:
    """Cria e entrega um TaskService conectado ao banco de dados.

    Abre a conexão, garante o schema e fecha ao final da requisição.

    Yields:
        TaskService configurado com repositório e banco ativos.
    """
    conn = get_connection("tasks.db")
    create_schema(conn)
    repo = TaskRepository(conn)
    service = TaskService(repo)
    try:
        yield service
    finally:
        conn.close()
