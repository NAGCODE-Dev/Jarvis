from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

from jarvis.config import settings


DEFAULT_CAPABILITIES = {
    "qwen3:8b": {"coding": 11, "planning": 8, "reasoning": 9, "general": 8},
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
        text_models = [model for model in installed_models if "embed" not in model.lower()]
        if not text_models:
            return []

        benchmarks = self._read(settings.model_benchmarks_path) if settings.model_benchmarks_path.exists() else {}
        capabilities = self._read(settings.model_capabilities_path)
        available_ram_mb = self._available_memory_mb()
        strategy = settings.model_selection_strategy

        scored: list[tuple[float, str]] = []
        unscored: list[str] = []
        for model in text_models:
            if model in benchmarks:
                metrics = benchmarks[model]
                score = self._score_model(
                    model=model,
                    task=task,
                    metrics=metrics,
                    capabilities=capabilities,
                    available_ram_mb=available_ram_mb,
                    strategy=strategy,
                    preferred=preferred,
                )
                scored.append((score, model))
            else:
                unscored.append(model)

        scored.sort(reverse=True)
        ordered = [model for _, model in scored]

        for model in preferred:
            if model in text_models and model not in ordered:
                ordered.insert(0, model)

        ranked_prefixes = ["qwen", "deepseek", "codestral", "coder"] if task == "coding" else ["gemma", "qwen", "llama"]
        for prefix in ranked_prefixes:
            for model in unscored:
                if model not in ordered and model.lower().startswith(prefix):
                    ordered.append(model)

        for model in text_models:
            if model not in ordered:
                ordered.append(model)
        return ordered

    def list_visible_models(self) -> list[str]:
        return self._read(settings.model_registry_path).get("installed", [])

    def get_rankings(self) -> dict[str, Any]:
        return self._read(settings.model_rankings_path)

    def save_benchmark(self, results: dict[str, Any]) -> None:
        self._write(settings.model_benchmarks_path, results)
        previous_rankings = self.get_rankings() if settings.model_rankings_path.exists() else {}
        rankings = {
            "coding_primary": self._rank_models(results, capability="coding"),
            "planning_primary": self._rank_models(results, capability="planning"),
            "safe_fallback": self._rank_models(results, capability="general"),
        }
        has_stable_model = any(metrics.get("stable", False) for metrics in results.values())
        if not has_stable_model:
            rankings = previous_rankings.get(
                "rankings",
                {
                    "coding_primary": [settings.coder_model, settings.coder_fallback_model],
                    "planning_primary": [settings.planner_model, settings.planner_fallback_model],
                    "safe_fallback": [settings.coder_fallback_model, settings.planner_fallback_model],
                },
            )
        self._write(settings.model_rankings_path, {
            "benchmarked_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "strategy": settings.model_selection_strategy,
            "benchmark_status": "ok" if has_stable_model else "no_stable_models",
            "rankings": rankings,
            "models": results,
        })

    def _score_model(
        self,
        *,
        model: str,
        task: str,
        metrics: dict[str, Any],
        capabilities: dict[str, Any],
        available_ram_mb: float | None,
        strategy: str,
        preferred: list[str],
    ) -> float:
        if not metrics.get("stable", False):
            return float("-inf")

        capability_key = "coding" if task == "coding" else "planning"
        capability_score = float(capabilities.get(model, {}).get(capability_key, 0))
        general_score = float(capabilities.get(model, {}).get("general", 0))
        throughput = float(metrics.get("tokens_per_second", 0.0))
        latency = float(metrics.get("median_latency_ms", metrics.get("first_token_latency_ms", settings.benchmark_timeout_seconds * 1000)))
        peak_rss_mb = float(metrics.get("peak_rss_mb", 0.0))

        memory_penalty = 0.0
        if available_ram_mb is not None and available_ram_mb > 0:
            allowed = available_ram_mb * settings.model_memory_safety_ratio
            if peak_rss_mb > allowed:
                memory_penalty += (peak_rss_mb - allowed) * 2.5

        preferred_bonus = 20.0 if model in preferred else 0.0
        if strategy == "quality":
            soft_cap = settings.model_quality_latency_soft_cap_ms
            latency_penalty = max(0.0, latency - soft_cap) / 1500.0
            return capability_score * 12 + general_score * 2 + throughput * 0.8 + preferred_bonus - latency_penalty - memory_penalty
        if strategy == "speed":
            soft_cap = settings.model_speed_latency_soft_cap_ms
            latency_penalty = latency / 500.0 + max(0.0, latency - soft_cap) / 600.0
            return capability_score * 4 + general_score + throughput * 3 + preferred_bonus - latency_penalty - memory_penalty

        soft_cap = settings.model_balanced_latency_soft_cap_ms
        latency_penalty = latency / 1200.0 + max(0.0, latency - soft_cap) / 1000.0
        return capability_score * 8 + general_score * 1.5 + throughput * 1.8 + preferred_bonus - latency_penalty - memory_penalty

    def _available_memory_mb(self) -> float | None:
        try:
            meminfo = Path("/proc/meminfo").read_text(encoding="utf-8")
            for line in meminfo.splitlines():
                if line.startswith("MemAvailable:"):
                    parts = line.split()
                    return float(parts[1]) / 1024.0
        except Exception:
            return None
        return None

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
