from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
import math
from pathlib import Path
import re
import shutil
from typing import Any, Literal

from pydantic import BaseModel, Field

from jarvis.config import settings
from jarvis.ollama_client import OllamaClient
from jarvis.schemas import ChatMessage


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


class MemoryAction(BaseModel):
    action: Literal[
        "set_identity_fact",
        "update_preference",
        "set_goal",
        "update_constraint",
        "update_state",
        "append_timeline_event",
        "append_workspace_note",
    ]
    field: str
    value: Any
    source: str = "system"
    workspace: str | None = None
    timestamp: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class MemoryService:
    def __init__(self) -> None:
        self.current_dir = settings.memory_dir / "current"
        self.archive_dir = settings.memory_dir / "archive"
        self.summaries_dir = settings.memory_dir / "summaries"
        self.workspace_dir = settings.workspace_memory_dir
        self.active_dir = settings.active_memory_dir
        self.topics_dir = settings.topic_memory_dir
        self.vectors_dir = settings.vector_memory_dir
        self.current_context_path = settings.current_context_path
        self.topic_index_path = settings.topic_index_path
        self.memory_vectors_path = settings.memory_vectors_path
        self.ollama = OllamaClient()
        self._ensure_layout()

    def _ensure_layout(self) -> None:
        dirs = [
            settings.data_dir,
            settings.identity_dir,
            settings.state_dir,
            settings.state_history_dir,
            settings.timeline_dir,
            settings.memory_dir,
            self.current_dir,
            self.archive_dir,
            self.summaries_dir,
            self.workspace_dir,
            self.active_dir,
            self.topics_dir,
            self.vectors_dir,
            settings.models_dir,
            settings.model_rankings_path.parent,
        ]
        for path in dirs:
            path.mkdir(parents=True, exist_ok=True)

        self._ensure_file(settings.profile_path, "# Profile\n\n")
        self._ensure_file(settings.preferences_path, "# Preferences\n\n")
        self._ensure_file(settings.goals_path, "# Goals\n\n")
        self._ensure_file(settings.constraints_path, "# Constraints\n\n")
        self._ensure_file(settings.state_path, "# Current State\n\n")
        self._ensure_file(settings.timeline_path, "# Timeline\n\n")
        self._ensure_json(settings.identity_index_path, {})
        self._ensure_json(settings.state_index_path, {})
        self._ensure_json(settings.timeline_index_path, {})
        self._ensure_json(settings.memory_catalog_path, {})
        self._ensure_json(
            self.current_context_path,
            {
                "messages": [],
                "active_topics": [],
                "updated_at": _now_iso(),
                "last_compacted_at": None,
            },
        )
        self._ensure_json(self.topic_index_path, self._default_topic_index())
        self._ensure_json(self.memory_vectors_path, {"items": [], "updated_at": _now_iso()})

    def apply(self, action: MemoryAction) -> dict[str, Any]:
        handlers = {
            "set_identity_fact": self._set_identity_fact,
            "update_preference": self._update_preference,
            "set_goal": self._set_goal,
            "update_constraint": self._update_constraint,
            "update_state": self._update_state,
            "append_timeline_event": self._append_timeline_event,
            "append_workspace_note": self._append_workspace_note,
        }
        result = handlers[action.action](action)
        self._update_catalog(action, result)
        return result

    def summarize_memory(self, label: str | None = None, scope: str = "current") -> Path:
        label = label or datetime.now(UTC).strftime("%Y-%m")
        summary_path = self.summaries_dir / f"{label}.md"
        files = sorted(self.current_dir.glob("*.md"))
        lines = [f"# Memory Summary {label}", "", f"- generated_at: {_now_iso()}", f"- scope: {scope}", ""]
        for file in files:
            lines.append(f"## {file.name}")
            lines.append("")
            lines.append(file.read_text(encoding="utf-8").strip())
            lines.append("")
        if len(lines) == 5:
            lines.append("No current memory notes found.")
        summary_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
        return summary_path

    def archive_old_memory(self, days: int | None = None) -> list[Path]:
        cutoff = datetime.now(UTC) - timedelta(days=days or settings.memory_archive_days)
        archived: list[Path] = []
        for path in self.current_dir.glob("*.md"):
            modified = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
            if modified < cutoff:
                target = self.archive_dir / path.name
                shutil.move(str(path), str(target))
                archived.append(target)
        return archived

    def resolve_context(
        self,
        *,
        fields: list[str] | None = None,
        workspace: str | None = None,
        include_archive: bool = False,
    ) -> dict[str, Any]:
        identity_index = self._read_json(settings.identity_index_path)
        state_index = self._read_json(settings.state_index_path)
        result: dict[str, Any] = {
            "identity": {},
            "state": {},
            "workspace": {},
            "archive": {},
        }
        if fields:
            for field in fields:
                if field in identity_index:
                    result["identity"][field] = identity_index[field]["value"]
                if field in state_index:
                    result["state"][field] = state_index[field]["value"]
        else:
            result["identity"] = {key: value["value"] for key, value in identity_index.items()}
            result["state"] = {key: value["value"] for key, value in state_index.items()}

        if workspace:
            workspace_index = self._workspace_index_path(workspace)
            if workspace_index.exists():
                index = self._read_json(workspace_index)
                result["workspace"] = {
                    "name": workspace,
                    "facts": {key: value["value"] for key, value in index.items()},
                }

        if include_archive:
            archives = [path.name for path in self.archive_dir.glob("*.md")]
            result["archive"] = {"files": archives}
        return result

    def create_current_note(self, title: str, content: str) -> Path:
        slug = title.lower().replace(" ", "-")
        path = self.current_dir / f"{slug}.md"
        path.write_text(f"# {title}\n\n- created_at: {_now_iso()}\n\n{content}\n", encoding="utf-8")
        return path

    def snapshot(self) -> dict[str, Any]:
        return self.resolve_context()

    def record_exchange(
        self,
        *,
        user_content: str,
        assistant_content: str,
        workspace: str | None = None,
        user_display_content: str | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        topic = self.detect_topic(user_display_content or user_content, workspace=workspace)
        summary_bucket = self._summary_bucket_for_topic(topic)
        current_context = self._read_json(self.current_context_path)
        current_context.setdefault("messages", []).extend(
            [
                self._build_working_message(
                    role="user",
                    content=user_content,
                    workspace=workspace,
                    topic=topic,
                    summary_bucket=summary_bucket,
                    display_content=user_display_content,
                    model=model,
                ),
                self._build_working_message(
                    role="assistant",
                    content=assistant_content,
                    workspace=workspace,
                    topic=topic,
                    summary_bucket=summary_bucket,
                    model=model,
                ),
            ]
        )
        current_context["active_topics"] = self._merge_recent_topics(current_context.get("active_topics", []), topic)
        current_context["updated_at"] = _now_iso()
        self._write_json(self.current_context_path, current_context)
        self._touch_active_topic(topic, workspace=workspace)
        self._compact_working_memory_if_needed()
        return {"topic": topic, "summary_bucket": summary_bucket}

    def build_runtime_context(
        self,
        *,
        user_message: str,
        recent_messages: list[ChatMessage] | None = None,
        workspace: str | None = None,
    ) -> dict[str, Any]:
        topic = self.detect_topic(user_message, workspace=workspace)
        summary_bucket = self._summary_bucket_for_topic(topic)
        global_summary = self._read_summary_bucket(summary_bucket)
        topic_memory = self._read_topic_memory(topic)
        active_memory = self._read_active_topic(topic)
        recent_context = self._format_recent_context(recent_messages)
        semantic_fragments = self._semantic_memory_search(user_message, topic=topic)
        return {
            "topic": topic,
            "summary_bucket": summary_bucket,
            "global_summary": global_summary,
            "topic_memory": topic_memory,
            "active_memory": active_memory,
            "recent_context": recent_context,
            "semantic_fragments": semantic_fragments,
        }

    def detect_topic(self, text: str, workspace: str | None = None) -> str:
        if workspace:
            return self._slugify(workspace)
        lowered = text.lower()
        best_topic = "general"
        best_score = 0
        for topic, keywords in self._read_json(self.topic_index_path).items():
            score = sum(1 for keyword in keywords if keyword.lower() in lowered)
            if score > best_score:
                best_score = score
                best_topic = topic
        return self._slugify(best_topic)

    def hierarchical_status(self) -> dict[str, Any]:
        current_context = self._read_json(self.current_context_path)
        return {
            "working_memory_messages": len(current_context.get("messages", [])),
            "active_topics": len(list(self.active_dir.glob("*.json"))),
            "summary_files": len(list(self.summaries_dir.glob("*.json"))),
            "topic_files": len(list(self.topics_dir.glob("*.md"))),
            "semantic_memory_enabled": settings.semantic_memory_enabled,
        }

    def _set_identity_fact(self, action: MemoryAction) -> dict[str, Any]:
        namespace = self._field_namespace(action.field)
        target_map = {
            "profile": settings.profile_path,
            "preferences": settings.preferences_path,
            "goals": settings.goals_path,
            "constraints": settings.constraints_path,
        }
        path = target_map[namespace]
        entry = self._upsert_index(settings.identity_index_path, action.field, action.value, action.source, namespace=namespace)
        self._rewrite_identity_markdown(namespace)
        return {"path": str(path), "entry": entry}

    def _update_preference(self, action: MemoryAction) -> dict[str, Any]:
        action = action.model_copy(update={"field": f"preferences.{action.field}" if "." not in action.field else action.field})
        return self._set_identity_fact(action)

    def _set_goal(self, action: MemoryAction) -> dict[str, Any]:
        action = action.model_copy(update={"field": f"goals.{action.field}" if "." not in action.field else action.field})
        return self._set_identity_fact(action)

    def _update_constraint(self, action: MemoryAction) -> dict[str, Any]:
        action = action.model_copy(update={"field": f"constraints.{action.field}" if "." not in action.field else action.field})
        return self._set_identity_fact(action)

    def _update_state(self, action: MemoryAction) -> dict[str, Any]:
        entry = self._upsert_index(settings.state_index_path, action.field, action.value, action.source, namespace="state")
        history_name = datetime.now(UTC).strftime("%Y-%m")
        history_path = settings.state_history_dir / f"{history_name}.md"
        history_block = (
            f"## {action.field}\n\n"
            f"- value: {action.value}\n"
            f"  created_at: {entry['created_at']}\n"
            f"  updated_at: {entry['updated_at']}\n"
            f"  source: {action.source}\n\n"
        )
        with history_path.open("a", encoding="utf-8") as handle:
            handle.write(history_block)
        self._rewrite_state_markdown()
        return {"path": str(settings.state_path), "entry": entry}

    def _append_timeline_event(self, action: MemoryAction) -> dict[str, Any]:
        happened_at = action.timestamp or _now_iso()
        day = happened_at[:10]
        content = settings.timeline_path.read_text(encoding="utf-8").rstrip()
        if f"## {day}" not in content:
            content += f"\n\n## {day}\n"
        content += f"\n- {action.value}"
        settings.timeline_path.write_text(content.strip() + "\n", encoding="utf-8")
        timeline_index = self._read_json(settings.timeline_index_path)
        timeline_index.setdefault(day, []).append({"event": action.value, "updated_at": happened_at, "source": action.source})
        self._write_json(settings.timeline_index_path, timeline_index)
        return {"path": str(settings.timeline_path), "day": day}

    def _append_workspace_note(self, action: MemoryAction) -> dict[str, Any]:
        if not action.workspace:
            raise ValueError("workspace is required for append_workspace_note")
        workspace_root = self._ensure_workspace(action.workspace)
        current_path = workspace_root / "current.md"
        index_path = self._workspace_index_path(action.workspace)
        entry = self._upsert_index(index_path, action.field, action.value, action.source, namespace="workspace", workspace=action.workspace)
        content = current_path.read_text(encoding="utf-8").rstrip()
        content += (
            f"\n\n## {action.field}\n\n"
            f"- value: {action.value}\n"
            f"  created_at: {entry['created_at']}\n"
            f"  updated_at: {entry['updated_at']}\n"
            f"  source: {action.source}\n"
        )
        current_path.write_text(content.strip() + "\n", encoding="utf-8")
        return {"path": str(current_path), "entry": entry}

    def _rewrite_identity_markdown(self, namespace: str) -> None:
        index = self._read_json(settings.identity_index_path)
        groups = {
            "profile": settings.profile_path,
            "preferences": settings.preferences_path,
            "goals": settings.goals_path,
            "constraints": settings.constraints_path,
        }
        path = groups[namespace]
        title = path.stem.replace("_", " ").title()
        lines = [f"# {title}", ""]
        entries = {key: value for key, value in index.items() if value.get("namespace") == namespace}
        for key, value in sorted(entries.items()):
            lines.append(f"## {key}")
            lines.append("")
            lines.append(f"- value: {value['value']}")
            lines.append(f"  created_at: {value['created_at']}")
            lines.append(f"  updated_at: {value['updated_at']}")
            lines.append(f"  source: {value['source']}")
            lines.append("")
        path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    def _rewrite_state_markdown(self) -> None:
        index = self._read_json(settings.state_index_path)
        lines = ["# Current State", ""]
        for key, value in sorted(index.items()):
            lines.append(f"## {key}")
            lines.append("")
            lines.append(f"- value: {value['value']}")
            lines.append(f"  created_at: {value['created_at']}")
            lines.append(f"  updated_at: {value['updated_at']}")
            lines.append(f"  source: {value['source']}")
            lines.append("")
        settings.state_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    def _update_catalog(self, action: MemoryAction, result: dict[str, Any]) -> None:
        catalog = self._read_json(settings.memory_catalog_path)
        catalog[action.field] = {
            "source": result["path"],
            "updated_at": action.timestamp or _now_iso(),
            "action": action.action,
            "workspace": action.workspace,
        }
        self._write_json(settings.memory_catalog_path, catalog)

    def _upsert_index(
        self,
        path: Path,
        field: str,
        value: Any,
        source: str,
        *,
        namespace: str,
        workspace: str | None = None,
    ) -> dict[str, Any]:
        index = self._read_json(path)
        existing = index.get(field)
        created_at = existing["created_at"] if existing else _now_iso()
        entry = {
            "value": value,
            "created_at": created_at,
            "updated_at": _now_iso(),
            "source": source,
            "namespace": namespace,
        }
        if workspace:
            entry["workspace"] = workspace
        index[field] = entry
        self._write_json(path, index)
        return entry

    def _field_namespace(self, field: str) -> str:
        prefix = field.split(".", 1)[0]
        if prefix in {"profile", "preferences", "goals", "constraints"}:
            return prefix
        return "profile"

    def _ensure_workspace(self, name: str) -> Path:
        root = self.workspace_dir / name
        for path in (root, root / "notes", root / "summaries", root / "archive"):
            path.mkdir(parents=True, exist_ok=True)
        self._ensure_file(root / "profile.md", f"# Workspace {name}\n\n")
        self._ensure_file(root / "current.md", f"# Workspace {name} Current\n\n")
        self._ensure_json(root / "workspace.index.json", {})
        self._ensure_json(root / "links.json", {"knowledge_domains": [name]})
        return root

    def _workspace_index_path(self, name: str) -> Path:
        return self.workspace_dir / name / "workspace.index.json"

    def _build_working_message(
        self,
        *,
        role: str,
        content: str,
        workspace: str | None,
        topic: str,
        summary_bucket: str,
        model: str | None = None,
        display_content: str | None = None,
    ) -> dict[str, Any]:
        importance = self._score_importance(content, topic=topic, role=role)
        return {
            "role": role,
            "content": content,
            "display_content": display_content,
            "workspace": workspace,
            "topic": topic,
            "summary_bucket": summary_bucket,
            "importance": importance,
            "model": model,
            "timestamp": _now_iso(),
        }

    def _merge_recent_topics(self, topics: list[str], topic: str) -> list[str]:
        merged = [topic, *[item for item in topics if item != topic]]
        return merged[:8]

    def _compact_working_memory_if_needed(self) -> None:
        current_context = self._read_json(self.current_context_path)
        messages = current_context.get("messages", [])
        if len(messages) <= settings.working_memory_limit:
            return

        preserve_recent = max(2, settings.working_memory_preserve_recent)
        cut_index = max(0, len(messages) - preserve_recent)
        old_messages = messages[:cut_index]
        current_context["messages"] = messages[cut_index:]

        for message in old_messages:
            if int(message.get("importance", 1)) < 4:
                continue
            topic = self._slugify(message.get("topic") or "general")
            bucket = self._slugify(message.get("summary_bucket") or self._summary_bucket_for_topic(topic))
            entry = self._extract_memory_entry(message)
            self._upsert_summary_entry(bucket, entry)
            self._append_topic_entry(topic, entry)
            self._append_active_entry(topic, entry)

        current_context["last_compacted_at"] = _now_iso()
        current_context["updated_at"] = _now_iso()
        self._write_json(self.current_context_path, current_context)
        if settings.semantic_memory_enabled:
            self._refresh_vector_index()

    def _extract_memory_entry(self, message: dict[str, Any]) -> dict[str, Any]:
        text = (message.get("display_content") or message["content"]).strip()
        kind = self._classify_memory_kind(text)
        return {
            "text": text[:1000],
            "kind": kind,
            "importance": int(message.get("importance", 3)),
            "topic": self._slugify(message.get("topic") or "general"),
            "workspace": message.get("workspace"),
            "source_role": message.get("role"),
            "updated_at": message.get("timestamp") or _now_iso(),
        }

    def _classify_memory_kind(self, text: str) -> str:
        lowered = text.lower()
        if re.search(r"\b(prefiro|preferencia|preferência|gosto de|use|evite|não use|nao use)\b", lowered):
            return "preferences"
        if re.search(r"\b(quero|objetivo|meta|preciso|precisamos|planejo|planos)\b", lowered):
            return "goals"
        if re.search(r"\b(decidi|decidimos|ficou definido|vamos usar|escolhi|escolhemos)\b", lowered):
            return "decisions"
        if re.search(r"\b(projeto|app|aplicativo|jarvis|build|feature|release)\b", lowered):
            return "projects"
        return "facts"

    def _upsert_summary_entry(self, bucket: str, entry: dict[str, Any]) -> None:
        path = self.summaries_dir / f"{bucket}.json"
        payload = self._read_or_default(
            path,
            {
                "facts": [],
                "preferences": [],
                "goals": [],
                "decisions": [],
                "projects": [],
                "updated_at": _now_iso(),
            },
        )
        items = payload.setdefault(entry["kind"], [])
        text = entry["text"]
        if not any(existing.get("text") == text for existing in items):
            items.append(entry)
        payload[entry["kind"]] = items[-settings.summary_item_limit :]
        payload["updated_at"] = _now_iso()
        self._write_json(path, payload)

    def _append_topic_entry(self, topic: str, entry: dict[str, Any]) -> None:
        path = self.topics_dir / f"{topic}.md"
        current = path.read_text(encoding="utf-8") if path.exists() else f"# Topic: {topic}\n\n"
        block = (
            f"## {entry['kind'].title()} | {entry['updated_at']}\n\n"
            f"- importance: {entry['importance']}\n"
            f"- source_role: {entry['source_role']}\n"
            f"- workspace: {entry.get('workspace') or 'none'}\n"
            f"- text: {entry['text']}\n\n"
        )
        path.write_text((current + block).strip() + "\n", encoding="utf-8")
        self._trim_topic_file(path)

    def _trim_topic_file(self, path: Path) -> None:
        content = path.read_text(encoding="utf-8")
        sections = content.split("\n## ")
        if len(sections) <= settings.topic_memory_entry_limit + 1:
            return
        head = sections[0]
        tail = sections[-settings.topic_memory_entry_limit :]
        rebuilt = head + "\n## " + "\n## ".join(tail)
        path.write_text(rebuilt.strip() + "\n", encoding="utf-8")

    def _touch_active_topic(self, topic: str, workspace: str | None = None) -> None:
        path = self.active_dir / f"{topic}.json"
        payload = self._read_or_default(
            path,
            {"topic": topic, "workspace": workspace, "items": [], "last_used_at": _now_iso()},
        )
        payload["workspace"] = workspace or payload.get("workspace")
        payload["last_used_at"] = _now_iso()
        self._write_json(path, payload)
        self._prune_active_topics()

    def _append_active_entry(self, topic: str, entry: dict[str, Any]) -> None:
        path = self.active_dir / f"{topic}.json"
        payload = self._read_or_default(
            path,
            {"topic": topic, "workspace": entry.get("workspace"), "items": [], "last_used_at": _now_iso()},
        )
        items = payload.setdefault("items", [])
        if not any(existing.get("text") == entry["text"] for existing in items):
            items.append(entry)
        payload["items"] = items[-settings.topic_memory_entry_limit :]
        payload["last_used_at"] = _now_iso()
        self._write_json(path, payload)
        self._prune_active_topics()

    def _prune_active_topics(self) -> None:
        cutoff = datetime.now(UTC) - timedelta(days=settings.active_memory_days)
        for path in self.active_dir.glob("*.json"):
            payload = self._read_or_default(path, {})
            last_used_at = payload.get("last_used_at")
            if not last_used_at:
                continue
            try:
                parsed = datetime.fromisoformat(last_used_at)
            except ValueError:
                continue
            if parsed < cutoff:
                path.unlink(missing_ok=True)

    def _read_summary_bucket(self, bucket: str) -> dict[str, Any]:
        path = self.summaries_dir / f"{bucket}.json"
        return self._read_or_default(
            path,
            {
                "facts": [],
                "preferences": [],
                "goals": [],
                "decisions": [],
                "projects": [],
                "updated_at": None,
            },
        )

    def _read_topic_memory(self, topic: str) -> str:
        path = self.topics_dir / f"{topic}.md"
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8").strip()

    def _read_active_topic(self, topic: str) -> dict[str, Any]:
        path = self.active_dir / f"{topic}.json"
        return self._read_or_default(path, {"topic": topic, "items": [], "last_used_at": None})

    def _format_recent_context(self, recent_messages: list[ChatMessage] | None) -> list[str]:
        if recent_messages:
            return [f"{message.role}: {message.content}" for message in recent_messages[-settings.history_preserve_messages :]]
        current_context = self._read_json(self.current_context_path)
        messages = current_context.get("messages", [])[-settings.history_preserve_messages :]
        return [f"{message['role']}: {message['content']}" for message in messages]

    def _semantic_memory_search(self, query: str, *, topic: str) -> list[dict[str, Any]]:
        if not settings.semantic_memory_enabled:
            return []
        index = self._read_or_default(self.memory_vectors_path, {"items": []})
        items = index.get("items", [])
        if not items:
            return []
        query_vector = self.ollama.embed(query)[0]
        scored: list[tuple[float, dict[str, Any]]] = []
        for item in items:
            if item.get("topic") not in {topic, "general"} and item.get("bucket") not in {
                self._summary_bucket_for_topic(topic),
                "general",
            }:
                continue
            score = self._cosine_similarity(query_vector, item.get("embedding", []))
            scored.append((score, item))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [item for score, item in scored[: settings.semantic_memory_top_k] if score > 0.25]

    def _refresh_vector_index(self) -> None:
        records: list[dict[str, Any]] = []
        for path in sorted(self.summaries_dir.glob("*.json")):
            payload = self._read_or_default(path, {})
            text = self._render_summary_payload(payload)
            if not text.strip():
                continue
            records.append(
                {
                    "id": path.stem,
                    "kind": "summary",
                    "topic": "general",
                    "bucket": path.stem,
                    "text": text[:2000],
                }
            )
        for path in sorted(self.active_dir.glob("*.json")):
            payload = self._read_or_default(path, {})
            text = self._render_active_payload(payload)
            if not text.strip():
                continue
            records.append(
                {
                    "id": path.stem,
                    "kind": "active",
                    "topic": path.stem,
                    "bucket": self._summary_bucket_for_topic(path.stem),
                    "text": text[:2000],
                }
            )
        for path in sorted(self.topics_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8").strip()
            if not text:
                continue
            records.append(
                {
                    "id": path.stem,
                    "kind": "topic",
                    "topic": path.stem,
                    "bucket": self._summary_bucket_for_topic(path.stem),
                    "text": text[:2000],
                }
            )
        if not records:
            self._write_json(self.memory_vectors_path, {"items": [], "updated_at": _now_iso()})
            return
        embeddings = self.ollama.embed([record["text"] for record in records])
        items = []
        for record, embedding in zip(records, embeddings, strict=False):
            items.append({**record, "embedding": embedding})
        self._write_json(self.memory_vectors_path, {"items": items, "updated_at": _now_iso()})

    def _render_summary_payload(self, payload: dict[str, Any]) -> str:
        parts: list[str] = []
        for key in ("facts", "preferences", "goals", "decisions", "projects"):
            entries = payload.get(key, [])
            if not entries:
                continue
            parts.append(f"{key}:")
            parts.extend(f"- {entry['text']}" for entry in entries[-20:])
        return "\n".join(parts)

    def _render_active_payload(self, payload: dict[str, Any]) -> str:
        items = payload.get("items", [])
        return "\n".join(f"- {item['kind']}: {item['text']}" for item in items[-20:])

    def _score_importance(self, text: str, *, topic: str, role: str) -> int:
        lowered = text.lower().strip()
        if not lowered:
            return 1
        if re.fullmatch(r"(oi|ola|olá|ok|blz|beleza|valeu|thanks|thank you)[!. ]*", lowered):
            return 1
        if "?" in lowered and len(lowered) < 80:
            return 2
        if self._classify_memory_kind(text) in {"preferences", "goals", "decisions", "projects"}:
            return 5 if role == "user" else 4
        if topic not in {"general", "personal"} and len(lowered) > 80:
            return 4
        if len(lowered) > 160:
            return 3
        return 2

    def _summary_bucket_for_topic(self, topic: str) -> str:
        topic = self._slugify(topic)
        mapping = {
            "crossfit": "training",
            "weightlifting": "training",
            "powerlifting": "training",
            "musculacao": "training",
            "training": "training",
            "programming": "programming",
            "android_app": "programming",
            "coding": "programming",
            "programacao": "programming",
            "jarvis": "projects",
            "hardware": "hardware",
            "pc_build": "hardware",
            "personal": "personal",
        }
        return mapping.get(topic, "projects" if topic not in {"general", "personal"} else topic)

    def _slugify(self, value: str) -> str:
        cleaned = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
        return cleaned or "general"

    def _default_topic_index(self) -> dict[str, list[str]]:
        return {
            "crossfit": ["crossfit", "wod", "snatch", "clean", "jerk", "metcon", "bar muscle up"],
            "training": ["treino", "hipertrofia", "força", "forca", "periodização", "periodizacao", "rpe", "rir", "vbt"],
            "programming": ["python", "java", "kotlin", "android", "api", "docker", "linux", "git", "backend", "frontend"],
            "jarvis": ["jarvis", "memória", "memoria", "rag", "agent", "llm", "qdrant", "ollama"],
            "hardware": ["hardware", "pc", "gpu", "cpu", "ram", "ssd", "fonte", "placa mãe", "placa mae"],
            "personal": ["minha rotina", "meu objetivo", "preferência", "preferencia", "pessoal"],
        }

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        if not left or not right or len(left) != len(right):
            return 0.0
        dot = sum(a * b for a, b in zip(left, right, strict=False))
        left_norm = math.sqrt(sum(a * a for a in left))
        right_norm = math.sqrt(sum(b * b for b in right))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return dot / (left_norm * right_norm)

    def _read_or_default(self, path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        return self._read_json(path)

    def _ensure_file(self, path: Path, content: str) -> None:
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    def _ensure_json(self, path: Path, content: dict[str, Any] | list[Any]) -> None:
        if not path.exists():
            self._write_json(path, content)

    def _read_json(self, path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_json(self, path: Path, content: Any) -> None:
        path.write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


MemoryManager = MemoryService
