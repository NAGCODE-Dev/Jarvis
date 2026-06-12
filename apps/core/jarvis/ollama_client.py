from __future__ import annotations

from collections.abc import Iterable
import json
from hashlib import sha256
from typing import Any

import httpx

from jarvis.config import settings
from jarvis.schemas import ChatMessage


class OllamaClient:
    def __init__(self) -> None:
        self._client = httpx.Client(
            base_url=settings.ollama_base_url,
            timeout=settings.ollama_timeout_seconds,
        )

    def list_models(self) -> dict[str, Any]:
        response = self._client.get("/api/tags")
        response.raise_for_status()
        return response.json()

    def health(self) -> dict[str, Any]:
        response = self._client.get("/api/tags")
        response.raise_for_status()
        payload = response.json()
        return {
            "status": "ok",
            "models": [model.get("name") for model in payload.get("models", [])],
        }

    def chat(
        self,
        model: str,
        messages: Iterable[ChatMessage],
        *,
        temperature: float | None = None,
        options: dict[str, Any] | None = None,
    ) -> str:
        payload: dict[str, Any] = {
            "model": model,
            "messages": [message.model_dump() for message in messages],
            "stream": False,
        }
        if settings.ollama_keep_alive:
            payload["keep_alive"] = settings.ollama_keep_alive
        merged_options = dict(options or {})
        merged_options.setdefault("num_ctx", settings.ollama_num_ctx)
        if temperature is not None:
            merged_options["temperature"] = temperature
        if merged_options:
            payload["options"] = merged_options

        response = self._client.post("/api/chat", json=payload)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]

    def chat_stream(
        self,
        model: str,
        messages: Iterable[ChatMessage],
        *,
        temperature: float | None = None,
        options: dict[str, Any] | None = None,
    ):
        payload: dict[str, Any] = {
            "model": model,
            "messages": [message.model_dump() for message in messages],
            "stream": True,
        }
        if settings.ollama_keep_alive:
            payload["keep_alive"] = settings.ollama_keep_alive
        merged_options = dict(options or {})
        merged_options.setdefault("num_ctx", settings.ollama_num_ctx)
        if temperature is not None:
            merged_options["temperature"] = temperature
        if merged_options:
            payload["options"] = merged_options

        with self._client.stream("POST", "/api/chat", json=payload) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                if isinstance(line, bytes):
                    line = line.decode("utf-8")
                data = json.loads(line)
                message = data.get("message", {})
                chunk = message.get("content", "")
                if chunk:
                    yield chunk

    def embed(self, text: str | list[str], model: str | None = None) -> list[list[float]]:
        payload = {
            "model": model or settings.embedding_model,
            "input": text,
        }
        try:
            response = self._client.post("/api/embed", json=payload)
            response.raise_for_status()
            data = response.json()
            embeddings = data.get("embeddings", [])
            if embeddings and isinstance(embeddings[0], float):
                return [embeddings]
            return embeddings
        except Exception:
            if not settings.allow_local_embedding_fallback:
                raise
            if isinstance(text, list):
                return [self._fallback_embed(item) for item in text]
            return [self._fallback_embed(text)]

    def _fallback_embed(self, text: str, dims: int = 256) -> list[float]:
        vector = [0.0] * dims
        for token in text.lower().split():
            digest = sha256(token.encode("utf-8")).digest()
            bucket = int.from_bytes(digest[:4], "big") % dims
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[bucket] += sign
        norm = sum(value * value for value in vector) ** 0.5 or 1.0
        return [value / norm for value in vector]
