"""Rotas da API de tarefas — camada de tradução HTTP ↔ domínio."""

from fastapi import APIRouter, Depends

from src.api.dependencies import get_task_service
from src.api.schemas.task import (
    StatusUpdateRequest,
    TaskCreateRequest,
    TaskCreateResponse,
    TaskResponse,
)
from src.models.task import Priority, TaskStatus
from src.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=201, response_model=TaskCreateResponse)
def create_task(
    body: TaskCreateRequest,
    service: TaskService = Depends(get_task_service),
) -> TaskCreateResponse:
    """Registra uma nova tarefa com status inicial pendente.

    Aplica todas as regras de negócio: validação de título, prazo e duplicidade.
    Retorna a tarefa criada com aviso se o título já existir no dia.
    """
    task, duplicate_warning = service.create_task(
        title=body.title,
        description=body.description,
        deadline=body.deadline,
        priority=body.priority or Priority.MEDIA,
    )
    return TaskCreateResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        deadline=task.deadline,
        priority=task.priority,
        status=task.status,
        created_at=task.created_at,
        is_due_today=task.is_due_today,
        duplicate_warning=duplicate_warning,
    )


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    status: TaskStatus | None = None,
    priority: Priority | None = None,
    service: TaskService = Depends(get_task_service),
) -> list[TaskResponse]:
    """Lista tarefas com filtro opcional por status e/ou prioridade.

    Retorna lista vazia sem erro quando não há tarefas cadastradas.
    Valores inválidos nos filtros geram resposta 422 automaticamente via Pydantic.
    """
    tasks = service.list_tasks(status=status, priority=priority)
    return [
        TaskResponse(
            id=t.id,
            title=t.title,
            description=t.description,
            deadline=t.deadline,
            priority=t.priority,
            status=t.status,
            created_at=t.created_at,
            is_due_today=t.is_due_today,
        )
        for t in tasks
    ]


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    body: StatusUpdateRequest,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Avança o status de uma tarefa seguindo o fluxo unidirecional.

    Fluxo permitido: pendente → em_andamento → concluida.
    ID inexistente retorna 404; transição inválida ou tarefa concluída retorna 422.
    """
    task = service.update_task_status(task_id, body.new_status)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        deadline=task.deadline,
        priority=task.priority,
        status=task.status,
        created_at=task.created_at,
        is_due_today=task.is_due_today,
    )


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> None:
    """Remove permanentemente uma tarefa com status pendente.

    ID inexistente retorna 404; tarefa em andamento ou concluída retorna 422.
    """
    service.delete_task(task_id)
