from __future__ import annotations

from functools import lru_cache

from jarvis.config import settings


@lru_cache(maxsize=32)
def load_prompt(name: str) -> str:
    path = settings.prompts_dir / name
    return path.read_text(encoding="utf-8").strip()

