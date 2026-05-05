"""Repositório de acesso ao banco de dados para tarefas."""

import sqlite3
from datetime import date

from src.models.task import Priority, Task, TaskStatus


class TaskRepository:
    """Camada de acesso a dados para a entidade Task.

    Responsável exclusivamente por operações de persistência.
    Nenhuma regra de negócio deve existir nesta camada.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        """Inicializa o repositório com uma conexão SQLite.

        Args:
            conn: Conexão SQLite ativa. Use ':memory:' para testes.
        """
        self._conn = conn

    def save(self, task: Task) -> Task:
        """Persiste uma nova tarefa no banco e retorna com o id gerado.

        Args:
            task: Tarefa a ser salva. O campo 'id' deve ser None.

        Returns:
            A mesma tarefa com o campo 'id' preenchido.
        """
        cursor = self._conn.execute(
            """
            INSERT INTO tasks (title, description, deadline, priority, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                task.title,
                task.description,
                task.deadline.isoformat() if task.deadline else None,
                task.priority.value,
                task.status.value,
                task.created_at.isoformat(),
            ),
        )
        self._conn.commit()
        task.id = cursor.lastrowid
        return task

    def find_all(
        self,
        status: TaskStatus | None = None,
        priority: Priority | None = None,
    ) -> list[Task]:
        """Retorna todas as tarefas, com filtragem opcional.

        Args:
            status: Filtro por status. None retorna todos os status.
            priority: Filtro por prioridade. None retorna todas as prioridades.

        Returns:
            Lista de tarefas. Retorna lista vazia se nenhuma tarefa encontrada.
        """
        query = "SELECT * FROM tasks WHERE 1=1"
        params: list[str] = []

        if status is not None:
            query += " AND status = ?"
            params.append(status.value)

        if priority is not None:
            query += " AND priority = ?"
            params.append(priority.value)

        rows = self._conn.execute(query, params).fetchall()
        return [self._row_to_task(row) for row in rows]

    def find_by_id(self, task_id: int) -> Task | None:
        """Busca uma tarefa pelo seu identificador único.

        Args:
            task_id: Identificador da tarefa.

        Returns:
            A tarefa encontrada ou None se não existir.
        """
        row = self._conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return self._row_to_task(row) if row else None

    def find_by_title_and_date(self, title: str, created_at: date) -> list[Task]:
        """Busca tarefas com o mesmo título criadas em uma data específica.

        Usado para detectar títulos duplicados no mesmo dia.

        Args:
            title: Título a ser verificado.
            created_at: Data de criação a ser comparada.

        Returns:
            Lista de tarefas com título e data correspondentes.
        """
        rows = self._conn.execute(
            "SELECT * FROM tasks WHERE title = ? AND created_at = ?",
            (title, created_at.isoformat()),
        ).fetchall()
        return [self._row_to_task(row) for row in rows]

    def update(self, task: Task) -> Task:
        """Atualiza os dados de uma tarefa existente no banco.

        Args:
            task: Tarefa com os dados atualizados. O campo 'id' deve estar preenchido.

        Returns:
            A tarefa atualizada.
        """
        self._conn.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, deadline = ?,
                priority = ?, status = ?, created_at = ?
            WHERE id = ?
            """,
            (
                task.title,
                task.description,
                task.deadline.isoformat() if task.deadline else None,
                task.priority.value,
                task.status.value,
                task.created_at.isoformat(),
                task.id,
            ),
        )
        self._conn.commit()
        return task

    def delete(self, task_id: int) -> None:
        """Remove uma tarefa do banco pelo seu identificador.

        Args:
            task_id: Identificador da tarefa a ser removida.
        """
        self._conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self._conn.commit()

    def _row_to_task(self, row: sqlite3.Row) -> Task:
        """Converte uma linha do banco em uma instância de Task.

        Args:
            row: Linha retornada pelo sqlite3 com Row factory.

        Returns:
            Instância de Task com os dados da linha.
        """
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            deadline=date.fromisoformat(row["deadline"]) if row["deadline"] else None,
            priority=Priority(row["priority"]),
            status=TaskStatus(row["status"]),
            created_at=date.fromisoformat(row["created_at"]),
        )
