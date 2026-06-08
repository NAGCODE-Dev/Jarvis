from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from jarvis.api import create_api_router
from jarvis.config import settings
from jarvis.knowledge import KnowledgeService
from jarvis.memory import MemoryManager
from jarvis.ollama_client import OllamaClient


def create_app() -> FastAPI:
    ollama = OllamaClient()
    memory = MemoryManager()
    knowledge = KnowledgeService(ollama)

    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.include_router(create_api_router(ollama=ollama, memory=memory, knowledge=knowledge))
    app.mount("/app", StaticFiles(directory=settings.web_dir, html=True), name="jarvis-web")

    @app.get("/", include_in_schema=False)
    def root_redirect():
        return RedirectResponse(url="/app/")

    return app


app = create_app()
