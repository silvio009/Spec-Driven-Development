"""Configuração e inicialização do banco de dados SQLite."""

import sqlite3


def get_connection(path: str) -> sqlite3.Connection:
    """Retorna uma conexão SQLite para o caminho informado.

    Use ':memory:' para banco em memória (ideal para testes).

    Args:
        path: Caminho do arquivo SQLite ou ':memory:' para banco em memória.

    Returns:
        Conexão SQLite configurada com Row factory para acesso por nome de coluna.
    """
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    """Cria a tabela 'tasks' caso ainda não exista.

    As constraints de CHECK no banco garantem integridade básica de dados.
    As regras de negócio (prazo no passado, transições de status,
    exclusão condicional) são aplicadas exclusivamente na camada de serviço.

    Args:
        conn: Conexão SQLite ativa.
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL
                                CHECK(length(title) >= 3 AND length(title) <= 100),
            description TEXT,
            deadline    TEXT,
            priority    TEXT    NOT NULL DEFAULT 'media'
                                CHECK(priority IN ('baixa', 'media', 'alta')),
            status      TEXT    NOT NULL DEFAULT 'pendente'
                                CHECK(status IN ('pendente', 'em_andamento', 'concluida')),
            created_at  TEXT    NOT NULL
        )
    """)
    conn.commit()
