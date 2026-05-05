"""Fixtures compartilhadas para os testes da camada de API."""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.api.dependencies import get_task_service
from src.database import create_schema, get_connection
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService


@pytest.fixture
def client() -> TestClient:
    """Retorna um TestClient com banco em memória isolado por teste.

    Substitui a dependência get_task_service por uma versão em memória
    para garantir isolamento entre testes sem tocar em arquivos.
    """
    import sqlite3 as _sqlite3

    conn = _sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = _sqlite3.Row
    create_schema(conn)
    repo = TaskRepository(conn)
    service = TaskService(repo)

    def override_get_task_service():
        """Substitui a dependência com o serviço em memória."""
        yield service

    app.dependency_overrides[get_task_service] = override_get_task_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    conn.close()
