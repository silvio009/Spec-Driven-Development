"""Modelos de domínio para gestão de tarefas."""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class Priority(str, Enum):
    """Níveis de prioridade disponíveis para uma tarefa."""

    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


class TaskStatus(str, Enum):
    """Estados possíveis no ciclo de vida de uma tarefa."""

    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"


@dataclass
class Task:
    """Representa uma tarefa do colaborador.

    Atributos:
        id: Identificador único gerado pelo banco (None antes de persistir).
        title: Título da tarefa. Mínimo 3, máximo 100 caracteres.
        description: Descrição detalhada opcional.
        deadline: Prazo de conclusão. Não pode ser data anterior à atual.
        priority: Nível de prioridade. Padrão: MEDIA.
        status: Estado atual no fluxo de vida da tarefa. Padrão: PENDENTE.
        created_at: Data de criação. Usada para detecção de título duplicado.
    """

    title: str
    id: int | None = None
    description: str | None = None
    deadline: date | None = None
    priority: Priority = Priority.MEDIA
    status: TaskStatus = TaskStatus.PENDENTE
    created_at: date = field(default_factory=date.today)

    @property
    def is_due_today(self) -> bool:
        """Retorna True se o prazo da tarefa é exatamente hoje."""
        return self.deadline is not None and self.deadline == date.today()
