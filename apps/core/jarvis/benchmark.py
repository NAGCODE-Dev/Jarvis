from __future__ import annotations

from datetime import UTC, datetime
import json
import resource
import time
from typing import Any

from jarvis.config import settings
from jarvis.ollama_client import OllamaClient
from jarvis.schemas import ChatMessage


class BenchmarkService:
    def __init__(self, ollama: OllamaClient) -> None:
        self.ollama = ollama

    def run(self, models: list[str] | None = None) -> dict[str, Any]:
        prompt_by_task = {
            "general": "Explique em até 6 linhas o objetivo de um assistente pessoal local.",
            "planning": "Monte um plano curto de estudos para 3 dias.",
            "coding": "Explique um bug simples de Python e como corrigir.",
        }
        models = models or [
            settings.planner_model,
            settings.planner_fallback_model,
            settings.coder_model,
            settings.coder_fallback_model,
        ]
        results: dict[str, Any] = {}
        for model in models:
            measures = []
            stable = True
            for task, prompt in prompt_by_task.items():
                started = time.perf_counter()
                rss_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                try:
                    content = self.ollama.chat(
                        model,
                        [ChatMessage(role="user", content=prompt)],
                        temperature=0.2,
                    )
                    elapsed = time.perf_counter() - started
                    rss_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                    char_count = max(len(content), 1)
                    tokens_estimate = max(char_count / 4.0, 1.0)
                    measures.append({
                        "task": task,
                        "latency_ms": round(elapsed * 1000, 2),
                        "tokens_per_second": round(tokens_estimate / max(elapsed, 0.001), 2),
                        "peak_rss_mb": round(max(rss_before, rss_after) / 1024.0, 2),
                    })
                except Exception:
                    stable = False
                    measures.append({
                        "task": task,
                        "latency_ms": None,
                        "tokens_per_second": 0.0,
                        "peak_rss_mb": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0, 2),
                    })
            latencies = [m["latency_ms"] for m in measures if m["latency_ms"] is not None]
            throughputs = [m["tokens_per_second"] for m in measures]
            results[model] = {
                "stable": stable and len(latencies) == len(prompt_by_task),
                "first_token_latency_ms": min(latencies) if latencies else settings.benchmark_timeout_seconds * 1000,
                "median_latency_ms": sorted(latencies)[len(latencies) // 2] if latencies else settings.benchmark_timeout_seconds * 1000,
                "tokens_per_second": round(sum(throughputs) / max(len(throughputs), 1), 2),
                "peak_rss_mb": max(m["peak_rss_mb"] for m in measures),
                "measures": measures,
                "benchmarked_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
            }
        with settings.benchmark_history_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"at": datetime.now(UTC).isoformat(), "results": results}, ensure_ascii=False) + "\n")
        return results
