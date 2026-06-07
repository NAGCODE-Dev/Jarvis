from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
import shutil
from typing import Any, Literal

from pydantic import BaseModel, Field

from jarvis.config import settings


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
