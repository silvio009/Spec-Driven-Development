"""Aplicação FastAPI — ponto de entrada da API de gestão de tarefas."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes import tasks as tasks_router
from src.database import create_schema, get_connection


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Gerencia o ciclo de vida da aplicação.

    Abre a conexão com o banco e cria o schema na inicialização.
    Fecha a conexão no encerramento.
    """
    conn = get_connection("tasks.db")
    create_schema(conn)
    app.state.conn = conn
    yield
    conn.close()


app = FastAPI(
    title="Time Manager — API de Tarefas",
    description="API REST para gestão de tarefas. Depende de 001-task-management.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Converte ValueError em resposta HTTP adequada.

    Mensagens contendo 'não encontrada' mapeiam para HTTP 404.
    Demais ValueError de negócio mapeiam para HTTP 422.
    """
    message = str(exc)
    status_code = 404 if "não encontrada" in message else 422
    return JSONResponse(status_code=status_code, content={"detail": message})


app.include_router(tasks_router.router)
