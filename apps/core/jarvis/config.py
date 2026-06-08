from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="JARVIS_",
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Jarvis Router"
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "info"

    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_timeout_seconds: float = 300.0
    qdrant_url: str = "http://127.0.0.1:6333"
    qdrant_collection: str = "jarvis-knowledge"
    qdrant_local_pathname: str = "qdrant-local"

    data_dir: Path = ROOT_DIR / "data"
    config_dir: Path = ROOT_DIR / "config"

    planner_model: str = "gemma4:e4b"
    planner_fallback_model: str = "gemma4:e2b"
    coder_model: str = "qwen3:8b"
    coder_fallback_model: str = "qwen3:1.7b"
    embedding_model: str = "nomic-embed-text"

    default_response_language: Literal["auto", "pt-BR", "en"] = "auto"
    model_selection_strategy: Literal["quality", "balanced", "speed"] = "quality"
    max_search_results: int = 6
    memory_archive_days: int = 30
    benchmark_timeout_seconds: float = 120.0
    memory_catalog_filename: str = "memory_catalog.json"
    allow_local_embedding_fallback: bool = True
    model_memory_safety_ratio: float = 0.75
    model_quality_latency_soft_cap_ms: float = 45000.0
    model_balanced_latency_soft_cap_ms: float = 25000.0
    model_speed_latency_soft_cap_ms: float = 12000.0

    @property
    def identity_dir(self) -> Path:
        return self.data_dir / "identity"

    @property
    def profile_path(self) -> Path:
        return self.identity_dir / "profile.md"

    @property
    def preferences_path(self) -> Path:
        return self.identity_dir / "preferences.md"

    @property
    def goals_path(self) -> Path:
        return self.identity_dir / "goals.md"

    @property
    def constraints_path(self) -> Path:
        return self.identity_dir / "constraints.md"

    @property
    def identity_index_path(self) -> Path:
        return self.identity_dir / "identity.index.json"

    @property
    def state_dir(self) -> Path:
        return self.data_dir / "state"

    @property
    def state_path(self) -> Path:
        return self.state_dir / "current.md"

    @property
    def state_history_dir(self) -> Path:
        return self.state_dir / "history"

    @property
    def state_index_path(self) -> Path:
        return self.state_dir / "state.index.json"

    @property
    def timeline_dir(self) -> Path:
        return self.data_dir / "timeline"

    @property
    def timeline_path(self) -> Path:
        return self.timeline_dir / "timeline.md"

    @property
    def timeline_index_path(self) -> Path:
        return self.timeline_dir / "timeline.index.json"

    @property
    def memory_dir(self) -> Path:
        return self.data_dir / "memory"

    @property
    def memory_catalog_path(self) -> Path:
        return self.data_dir / self.memory_catalog_filename

    @property
    def workspace_memory_dir(self) -> Path:
        return self.memory_dir / "workspaces"

    @property
    def knowledge_dir(self) -> Path:
        return self.data_dir / "knowledge"

    @property
    def prompts_dir(self) -> Path:
        return self.config_dir / "prompts"

    @property
    def web_dir(self) -> Path:
        return ROOT_DIR / "apps" / "web"

    @property
    def models_dir(self) -> Path:
        return self.data_dir / "models"

    @property
    def qdrant_local_path(self) -> Path:
        return self.data_dir / self.qdrant_local_pathname

    @property
    def model_registry_path(self) -> Path:
        return self.models_dir / "registry.json"

    @property
    def model_capabilities_path(self) -> Path:
        return self.models_dir / "capabilities.json"

    @property
    def model_benchmarks_path(self) -> Path:
        return self.models_dir / "benchmarks.json"

    @property
    def model_rankings_path(self) -> Path:
        return self.data_dir / "benchmark" / "model_rankings.json"

    @property
    def benchmark_history_path(self) -> Path:
        return self.data_dir / "benchmark" / "benchmark_history.jsonl"

    @property
    def sessions_dir(self) -> Path:
        return self.data_dir / "sessions"


settings = Settings()
