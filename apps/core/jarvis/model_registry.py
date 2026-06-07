from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

from jarvis.config import settings


DEFAULT_CAPABILITIES = {
    "qwen3:4b": {"coding": 10, "planning": 7, "reasoning": 8, "general": 7},
    "qwen3:1.7b": {"coding": 7, "planning": 5, "reasoning": 5, "general": 5},
    "gemma4:e4b": {"coding": 6, "planning": 10, "reasoning": 9, "general": 9},
    "gemma4:e2b": {"coding": 4, "planning": 7, "reasoning": 6, "general": 6},
    "nomic-embed-text": {"embeddings": 10},
}


class ModelRegistry:
    def __init__(self) -> None:
        self._ensure_layout()

    def _ensure_layout(self) -> None:
        settings.models_dir.mkdir(parents=True, exist_ok=True)
        settings.model_rankings_path.parent.mkdir(parents=True, exist_ok=True)
        if not settings.model_registry_path.exists():
            self._write(settings.model_registry_path, {
                "installed": [
                    settings.planner_model,
                    settings.planner_fallback_model,
                    settings.coder_model,
                    settings.coder_fallback_model,
                    settings.embedding_model,
                ]
            })
        if not settings.model_capabilities_path.exists():
            self._write(settings.model_capabilities_path, DEFAULT_CAPABILITIES)
        if not settings.model_benchmarks_path.exists():
            self._write(settings.model_benchmarks_path, {})
        if not settings.model_rankings_path.exists():
            self._write(settings.model_rankings_path, {
                "rankings": {
                    "coding_primary": [settings.coder_model, settings.coder_fallback_model],
                    "planning_primary": [settings.planner_model, settings.planner_fallback_model],
                    "safe_fallback": [settings.coder_fallback_model, settings.planner_fallback_model],
                }
            })

    def resolve_primary(self, task: str) -> tuple[str, str]:
        rankings = self._read(settings.model_rankings_path).get("rankings", {})
        if task == "coding":
            options = rankings.get("coding_primary", [settings.coder_model, settings.coder_fallback_model])
        else:
            options = rankings.get("planning_primary", [settings.planner_model, settings.planner_fallback_model])
        return options[0], options[1] if len(options) > 1 else options[0]

    def resolve_runtime_candidates(
        self,
        task: str,
        preferred: list[str],
        installed_models: list[str],
    ) -> list[str]:
        candidates: list[str] = []
        for model in preferred:
            if model in installed_models:
                candidates.append(model)

        ranked_prefixes = ["qwen", "deepseek", "codestral", "coder"] if task == "coding" else ["gemma", "qwen", "llama"]
        for prefix in ranked_prefixes:
            for model in installed_models:
                if model not in candidates and model.lower().startswith(prefix):
                    candidates.append(model)

        for model in installed_models:
            if model not in candidates:
                candidates.append(model)
        return candidates

    def list_visible_models(self) -> list[str]:
        return self._read(settings.model_registry_path).get("installed", [])

    def get_rankings(self) -> dict[str, Any]:
        return self._read(settings.model_rankings_path)

    def save_benchmark(self, results: dict[str, Any]) -> None:
        self._write(settings.model_benchmarks_path, results)
        rankings = {
            "coding_primary": self._rank_models(results, capability="coding"),
            "planning_primary": self._rank_models(results, capability="planning"),
            "safe_fallback": self._rank_models(results, capability="general"),
        }
        self._write(settings.model_rankings_path, {
            "benchmarked_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "rankings": rankings,
            "models": results,
        })

    def _rank_models(self, results: dict[str, Any], *, capability: str) -> list[str]:
        capabilities = self._read(settings.model_capabilities_path)
        scored: list[tuple[float, str]] = []
        for model, metrics in results.items():
            if not metrics.get("stable", False):
                continue
            capability_score = capabilities.get(model, {}).get(capability, 0)
            performance = metrics.get("tokens_per_second", 0.0)
            latency_penalty = metrics.get("first_token_latency_ms", 0.0) / 1000.0
            total = capability_score * 10 + performance - latency_penalty
            scored.append((total, model))
        scored.sort(reverse=True)
        return [model for _, model in scored] or [settings.coder_fallback_model, settings.planner_fallback_model]

    def _read(self, path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    def _write(self, path: Path, payload: Any) -> None:
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
