from __future__ import annotations

import json

from jarvis.model_registry import ModelRegistry


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_registry_prefers_stronger_model_in_quality_mode(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.model_registry as registry_module

    test_settings = config_module.Settings(
        data_dir=tmp_path / "data",
        config_dir=config_module.settings.config_dir,
        model_selection_strategy="quality",
    )
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)

    _write_json(
        test_settings.model_capabilities_path,
        {
            "qwen3:8b": {"coding": 11, "general": 8},
            "qwen3:4b": {"coding": 10, "general": 7},
        },
    )
    _write_json(
        test_settings.model_benchmarks_path,
        {
            "qwen3:8b": {"stable": True, "tokens_per_second": 6.0, "median_latency_ms": 15000, "first_token_latency_ms": 9000, "peak_rss_mb": 4500},
            "qwen3:4b": {"stable": True, "tokens_per_second": 12.0, "median_latency_ms": 9000, "first_token_latency_ms": 5000, "peak_rss_mb": 2600},
        },
    )

    registry = registry_module.ModelRegistry()
    candidates = registry.resolve_runtime_candidates("coding", ["qwen3:8b", "qwen3:4b"], ["qwen3:8b", "qwen3:4b"])
    assert candidates[0] == "qwen3:8b"


def test_registry_prefers_faster_model_in_speed_mode(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.model_registry as registry_module

    test_settings = config_module.Settings(
        data_dir=tmp_path / "data",
        config_dir=config_module.settings.config_dir,
        model_selection_strategy="speed",
    )
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)

    _write_json(
        test_settings.model_capabilities_path,
        {
            "qwen3:8b": {"coding": 11, "general": 8},
            "qwen3:4b": {"coding": 10, "general": 7},
        },
    )
    _write_json(
        test_settings.model_benchmarks_path,
        {
            "qwen3:8b": {"stable": True, "tokens_per_second": 4.0, "median_latency_ms": 32000, "first_token_latency_ms": 20000, "peak_rss_mb": 5200},
            "qwen3:4b": {"stable": True, "tokens_per_second": 11.0, "median_latency_ms": 7000, "first_token_latency_ms": 4000, "peak_rss_mb": 2600},
        },
    )

    registry = registry_module.ModelRegistry()
    candidates = registry.resolve_runtime_candidates("coding", ["qwen3:8b", "qwen3:4b"], ["qwen3:8b", "qwen3:4b"])
    assert candidates[0] == "qwen3:4b"


def test_registry_preserves_previous_rankings_when_benchmark_has_no_stable_models(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.model_registry as registry_module

    test_settings = config_module.Settings(
        data_dir=tmp_path / "data",
        config_dir=config_module.settings.config_dir,
        model_selection_strategy="quality",
    )
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)

    _write_json(
        test_settings.model_rankings_path,
        {
            "rankings": {
                "coding_primary": ["qwen3:8b", "qwen3:4b"],
                "planning_primary": ["gemma4:e4b", "gemma4:e2b"],
                "safe_fallback": ["qwen3:4b", "gemma4:e2b"],
            }
        },
    )

    registry = registry_module.ModelRegistry()
    registry.save_benchmark(
        {
            "qwen3:8b": {"stable": False, "tokens_per_second": 0.0, "median_latency_ms": 120000.0, "first_token_latency_ms": 120000.0, "peak_rss_mb": 100.0},
            "gemma4:e4b": {"stable": False, "tokens_per_second": 0.0, "median_latency_ms": 120000.0, "first_token_latency_ms": 120000.0, "peak_rss_mb": 100.0},
        }
    )

    saved = registry.get_rankings()
    assert saved["benchmark_status"] == "no_stable_models"
    assert saved["rankings"]["coding_primary"] == ["qwen3:8b", "qwen3:4b"]
