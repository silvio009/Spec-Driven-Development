"""Schemas Pydantic para request e response da API de tarefas."""

from datetime import date

from pydantic import BaseModel, Field

from src.models.task import Priority, TaskStatus


class TaskCreateRequest(BaseModel):
    """Corpo da requisição para criação de tarefa."""

    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    deadline: date | None = None
    priority: Priority | None = None


class StatusUpdateRequest(BaseModel):
    """Corpo da requisição para atualização de status."""

    new_status: TaskStatus


class TaskResponse(BaseModel):
    """Resposta padrão com dados de uma tarefa."""

    id: int
    title: str
    description: str | None
    deadline: date | None
    priority: Priority
    status: TaskStatus
    created_at: date
    is_due_today: bool

    model_config = {"from_attributes": True}


class TaskCreateResponse(TaskResponse):
    """Resposta da criação de tarefa — inclui aviso de duplicidade."""

    duplicate_warning: bool


class ErrorResponse(BaseModel):
    """Resposta de erro com mensagem descritiva."""

    detail: str
