"""Testes de integração dos endpoints da API de tarefas."""

from datetime import date, timedelta

from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# POST /tasks — US1
# ---------------------------------------------------------------------------


def test_create_task_returns_201_with_task_data(client: TestClient) -> None:
    """Criação com payload válido retorna HTTP 201 e dados da tarefa."""
    response = client.post("/tasks/", json={"title": "Revisar documentação"})

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Revisar documentação"
    assert data["status"] == "pendente"
    assert data["priority"] == "media"
    assert data["duplicate_warning"] is False
    assert data["id"] is not None


def test_create_task_short_title_returns_422(client: TestClient) -> None:
    """Título com menos de 3 caracteres retorna HTTP 422."""
    response = client.post("/tasks/", json={"title": "AB"})

    assert response.status_code == 422


def test_create_task_long_title_returns_422(client: TestClient) -> None:
    """Título com mais de 100 caracteres retorna HTTP 422."""
    response = client.post("/tasks/", json={"title": "A" * 101})

    assert response.status_code == 422


def test_create_task_past_deadline_returns_422(client: TestClient) -> None:
    """Prazo anterior à data atual retorna HTTP 422 com mensagem em português."""
    past = (date.today() - timedelta(days=1)).isoformat()
    response = client.post("/tasks/", json={"title": "Tarefa atrasada", "deadline": past})

    assert response.status_code == 422
    assert "Prazo não pode ser data passada" in response.json()["detail"]


def test_create_task_missing_title_returns_422(client: TestClient) -> None:
    """Body sem campo title retorna HTTP 422."""
    response = client.post("/tasks/", json={"description": "sem título"})

    assert response.status_code == 422


def test_create_task_duplicate_title_returns_warning(client: TestClient) -> None:
    """Título duplicado no mesmo dia retorna HTTP 201 com duplicate_warning=true."""
    payload = {"title": "Tarefa duplicada"}
    client.post("/tasks/", json=payload)
    response = client.post("/tasks/", json=payload)

    assert response.status_code == 201
    assert response.json()["duplicate_warning"] is True


def test_create_task_with_all_fields(client: TestClient) -> None:
    """Criação com todos os campos opcionais retorna dados completos."""
    future = (date.today() + timedelta(days=7)).isoformat()
    response = client.post(
        "/tasks/",
        json={
            "title": "Tarefa completa",
            "description": "Descrição detalhada",
            "deadline": future,
            "priority": "alta",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["priority"] == "alta"
    assert data["deadline"] == future
    assert data["description"] == "Descrição detalhada"


# ---------------------------------------------------------------------------
# GET /tasks — US2
# ---------------------------------------------------------------------------


def test_list_tasks_empty_returns_200(client: TestClient) -> None:
    """Listagem sem tarefas retorna HTTP 200 com lista vazia."""
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_returns_created_task(client: TestClient) -> None:
    """Tarefa criada aparece na listagem."""
    client.post("/tasks/", json={"title": "Tarefa listada"})
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Tarefa listada"


def test_list_tasks_filter_by_status(client: TestClient) -> None:
    """Filtro por status retorna apenas tarefas com aquele status."""
    client.post("/tasks/", json={"title": "Tarefa pendente"})
    response = client.get("/tasks/?status=pendente")

    assert response.status_code == 200
    tasks = response.json()
    assert all(t["status"] == "pendente" for t in tasks)


def test_list_tasks_filter_by_priority(client: TestClient) -> None:
    """Filtro por prioridade retorna apenas tarefas com aquela prioridade."""
    client.post("/tasks/", json={"title": "Alta prioridade", "priority": "alta"})
    client.post("/tasks/", json={"title": "Baixa prioridade", "priority": "baixa"})

    response = client.get("/tasks/?priority=alta")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["priority"] == "alta"


def test_list_tasks_combined_filters(client: TestClient) -> None:
    """Filtros combinados retornam apenas tarefas que atendem a ambos."""
    client.post("/tasks/", json={"title": "Match", "priority": "alta"})
    client.post("/tasks/", json={"title": "No match priority", "priority": "baixa"})

    response = client.get("/tasks/?status=pendente&priority=alta")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Match"


def test_list_tasks_invalid_status_returns_422(client: TestClient) -> None:
    """Valor de status inválido no filtro retorna HTTP 422."""
    response = client.get("/tasks/?status=invalido")

    assert response.status_code == 422


# ---------------------------------------------------------------------------
# PATCH /tasks/{id}/status — US3
# ---------------------------------------------------------------------------


def test_update_status_pendente_to_em_andamento(client: TestClient) -> None:
    """Transição pendente → em_andamento retorna HTTP 200 com status atualizado."""
    create = client.post("/tasks/", json={"title": "Tarefa para avançar"})
    task_id = create.json()["id"]

    response = client.patch(f"/tasks/{task_id}/status", json={"new_status": "em_andamento"})

    assert response.status_code == 200
    assert response.json()["status"] == "em_andamento"


def test_update_status_em_andamento_to_concluida(client: TestClient) -> None:
    """Transição em_andamento → concluida retorna HTTP 200."""
    create = client.post("/tasks/", json={"title": "Tarefa para concluir"})
    task_id = create.json()["id"]
    client.patch(f"/tasks/{task_id}/status", json={"new_status": "em_andamento"})

    response = client.patch(f"/tasks/{task_id}/status", json={"new_status": "concluida"})

    assert response.status_code == 200
    assert response.json()["status"] == "concluida"


def test_update_status_not_found_returns_404(client: TestClient) -> None:
    """ID inexistente retorna HTTP 404."""
    response = client.patch("/tasks/9999/status", json={"new_status": "em_andamento"})

    assert response.status_code == 404


def test_update_status_concluida_is_immutable(client: TestClient) -> None:
    """Tarefa concluída não pode ser editada — retorna HTTP 422."""
    create = client.post("/tasks/", json={"title": "Tarefa concluída"})
    task_id = create.json()["id"]
    client.patch(f"/tasks/{task_id}/status", json={"new_status": "em_andamento"})
    client.patch(f"/tasks/{task_id}/status", json={"new_status": "concluida"})

    response = client.patch(f"/tasks/{task_id}/status", json={"new_status": "pendente"})

    assert response.status_code == 422
    assert "concluída" in response.json()["detail"]


def test_update_status_invalid_transition_returns_422(client: TestClient) -> None:
    """Transição inválida (pendente → concluida direto) retorna HTTP 422."""
    create = client.post("/tasks/", json={"title": "Salto inválido"})
    task_id = create.json()["id"]

    response = client.patch(f"/tasks/{task_id}/status", json={"new_status": "concluida"})

    assert response.status_code == 422


def test_update_status_invalid_value_returns_422(client: TestClient) -> None:
    """Valor de new_status inválido retorna HTTP 422."""
    create = client.post("/tasks/", json={"title": "Status inválido"})
    task_id = create.json()["id"]

    response = client.patch(f"/tasks/{task_id}/status", json={"new_status": "xxx"})

    assert response.status_code == 422


# ---------------------------------------------------------------------------
# DELETE /tasks/{id} — US4
# ---------------------------------------------------------------------------


def test_delete_pending_task_returns_204(client: TestClient) -> None:
    """Exclusão de tarefa pendente retorna HTTP 204 sem corpo."""
    create = client.post("/tasks/", json={"title": "Tarefa a deletar"})
    task_id = create.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_removes_task_from_list(client: TestClient) -> None:
    """Após exclusão, tarefa não aparece mais na listagem."""
    create = client.post("/tasks/", json={"title": "Sumirá"})
    task_id = create.json()["id"]
    client.delete(f"/tasks/{task_id}")

    response = client.get("/tasks/")

    assert response.status_code == 200
    assert all(t["id"] != task_id for t in response.json())


def test_delete_not_found_returns_404(client: TestClient) -> None:
    """ID inexistente retorna HTTP 404."""
    response = client.delete("/tasks/9999")

    assert response.status_code == 404


def test_delete_in_progress_task_returns_422(client: TestClient) -> None:
    """Tarefa em andamento não pode ser deletada — retorna HTTP 422."""
    create = client.post("/tasks/", json={"title": "Em andamento"})
    task_id = create.json()["id"]
    client.patch(f"/tasks/{task_id}/status", json={"new_status": "em_andamento"})

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 422
    assert "em andamento" in response.json()["detail"]


def test_delete_completed_task_returns_422(client: TestClient) -> None:
    """Tarefa concluída não pode ser deletada — retorna HTTP 422."""
    create = client.post("/tasks/", json={"title": "Concluída"})
    task_id = create.json()["id"]
    client.patch(f"/tasks/{task_id}/status", json={"new_status": "em_andamento"})
    client.patch(f"/tasks/{task_id}/status", json={"new_status": "concluida"})

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 422
