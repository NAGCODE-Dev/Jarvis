from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from uuid import uuid4

from jarvis.config import settings


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


class SessionStore:
    def __init__(self) -> None:
        self.root = settings.sessions_dir
        self.root.mkdir(parents=True, exist_ok=True)

    def list_sessions(self) -> list[dict[str, object]]:
        sessions: list[dict[str, object]] = []
        for path in sorted(self.root.glob("*.json")):
            try:
                payload = self._read(path)
            except (OSError, json.JSONDecodeError, KeyError):
                continue
            meta = self._normalize_meta(payload.get("meta") or None)
            sessions.append(
                {
                    "id": payload["id"],
                    "title": payload.get("title", "Untitled"),
                    "model": payload.get("model", "jarvis-safe"),
                    "workspace": payload.get("workspace") or "",
                    "updated_at": payload.get("updated_at", ""),
                    "mission_objective": (payload.get("mission") or {}).get("objective") or "",
                    "mission_status": (payload.get("mission") or {}).get("status") or "",
                    "active_tasks": len([task for task in (payload.get("tasks") or []) if task.get("status") != "done"]),
                    "active_file": (payload.get("ui_state") or {}).get("active_file") or "",
                    "checkpoint_count": len(payload.get("checkpoints") or []),
                    "message_count": len(payload.get("messages") or []),
                    "preview": self._session_preview(payload),
                    "meta": meta,
                    "pinned": bool(meta.get("pinned")),
                    "archived": bool(meta.get("archived")),
                }
            )
        sessions.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
        return sessions

    def create_session(
        self,
        *,
        title: str | None = None,
        model: str = "jarvis-safe",
        workspace: str | None = None,
        mission: dict | None = None,
        ui_state: dict | None = None,
        meta: dict | None = None,
    ) -> dict:
        session_id = uuid4().hex
        payload = {
            "id": session_id,
            "title": title or "Nova conversa",
            "model": model,
            "workspace": workspace,
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
            "messages": [],
            "operations": [],
            "approvals": [],
            "mission": self._normalize_mission(mission),
            "ui_state": self._normalize_ui_state(ui_state),
            "meta": self._normalize_meta(meta),
            "tasks": [],
            "events": [],
            "checkpoints": [],
        }
        self._write(self._path(session_id), payload)
        return payload

    def get_session(self, session_id: str) -> dict:
        return self._read(self._path(session_id))

    def save_session(self, session_id: str, payload: dict) -> dict:
        payload["updated_at"] = _now_iso()
        self._write(self._path(session_id), payload)
        return payload

    def delete_session(self, session_id: str) -> None:
        path = self._path(session_id)
        if path.exists():
            path.unlink()


    def append_operation(
        self,
        session_id: str,
        *,
        kind: str,
        title: str,
        path: str | None = None,
        command: str | None = None,
        detail: str | None = None,
        metadata: dict | None = None,
    ) -> dict:
        session = self.get_session(session_id)
        operations = session.setdefault("operations", [])
        operations.append(
            {
                "kind": kind,
                "title": title,
                "path": path,
                "command": command,
                "detail": detail,
                "metadata": metadata or {},
                "created_at": _now_iso(),
            }
        )
        session["operations"] = operations[-200:]
        return self.save_session(session_id, session)



    def append_approval(
        self,
        session_id: str,
        *,
        kind: str,
        title: str,
        path: str | None = None,
        command: str | None = None,
        detail: str | None = None,
        metadata: dict | None = None,
        payload: dict | None = None,
    ) -> dict:
        session = self.get_session(session_id)
        approvals = session.setdefault("approvals", [])
        approvals.append(
            {
                "id": uuid4().hex,
                "kind": kind,
                "title": title,
                "path": path,
                "command": command,
                "detail": detail,
                "metadata": metadata or {},
                "payload": payload or {},
                "status": "pending",
                "created_at": _now_iso(),
                "updated_at": _now_iso(),
            }
        )
        session["approvals"] = approvals[-80:]
        return self.save_session(session_id, session)

    def update_approval(
        self,
        session_id: str,
        approval_id: str,
        *,
        status: str,
        result: dict | None = None,
        metadata_patch: dict | None = None,
    ) -> tuple[dict, dict]:
        session = self.get_session(session_id)
        approvals = session.setdefault("approvals", [])
        for approval in approvals:
            if approval.get("id") != approval_id:
                continue
            approval["status"] = status
            approval["updated_at"] = _now_iso()
            if result is not None:
                approval["result"] = result
            if metadata_patch:
                merged = dict(approval.get("metadata") or {})
                merged.update(metadata_patch)
                approval["metadata"] = merged
            updated = self.save_session(session_id, session)
            return updated, approval
        raise FileNotFoundError(f"Approval not found: {approval_id}")

    def get_approval(self, session_id: str, approval_id: str) -> dict:
        session = self.get_session(session_id)
        for approval in session.get("approvals", []):
            if approval.get("id") == approval_id:
                return approval
        raise FileNotFoundError(f"Approval not found: {approval_id}")

    def append_exchange(
        self,
        session_id: str,
        *,
        user_content: str,
        user_display_content: str | None,
        assistant_content: str,
        model: str,
        workspace: str | None = None,
        assistant_metadata: dict | None = None,
        user_attachments: list[dict] | None = None,
    ) -> dict:
        session = self.get_session(session_id)
        if workspace is not None:
            session["workspace"] = workspace
        session["model"] = model
        if not session.get("title") or session["title"] == "Nova conversa":
            session["title"] = self._derive_title(user_content=user_content, user_display_content=user_display_content)
        normalized_attachments = self._normalize_attachments(user_attachments)
        session.setdefault("messages", []).extend(
            [
                {
                    "role": "user",
                    "content": user_content,
                    **({"display_content": user_display_content} if user_display_content else {}),
                    **({"attachments": normalized_attachments} if normalized_attachments else {}),
                },
                {
                    "role": "assistant",
                    "content": assistant_content,
                    **({"metadata": assistant_metadata} if assistant_metadata else {}),
                },
            ]
        )
        return self.save_session(session_id, session)

    def append_event(self, session_id: str, *, event_type: str, payload: dict | None = None, source: str | None = None) -> dict:
        session = self.get_session(session_id)
        events = session.setdefault("events", [])
        events.append(
            {
                "type": event_type,
                "payload": payload or {},
                "source": source or "jarvis",
                "created_at": _now_iso(),
            }
        )
        session["events"] = events[-200:]
        return self.save_session(session_id, session)

    def create_checkpoint(
        self,
        session_id: str,
        *,
        title: str | None = None,
        summary: str | None = None,
        source: str | None = None,
        trigger_event: str | None = None,
    ) -> tuple[dict, dict]:
        session = self.get_session(session_id)
        checkpoint = {
            "id": uuid4().hex,
            "title": title or self._derive_checkpoint_title(session),
            "summary": summary,
            "source": source or "manual",
            "trigger_event": trigger_event,
            "workspace": session.get("workspace"),
            "active_file": (session.get("ui_state") or {}).get("active_file"),
            "message_count": len(session.get("messages") or []),
            "operation_count": len(session.get("operations") or []),
            "event_count": len(session.get("events") or []),
            "task_count": len(session.get("tasks") or []),
            "created_at": _now_iso(),
            "snapshot": {
                "ui_state": self._normalize_ui_state(session.get("ui_state") or None),
                "mission": self._normalize_mission(session.get("mission") or None),
                "workspace": session.get("workspace"),
            },
        }
        checkpoints = session.setdefault("checkpoints", [])
        checkpoints.append(checkpoint)
        session["checkpoints"] = checkpoints[-80:]
        updated = self.save_session(session_id, session)
        return updated, checkpoint

    def restore_checkpoint(self, session_id: str, checkpoint_id: str) -> tuple[dict, dict]:
        session = self.get_session(session_id)
        checkpoints = session.setdefault("checkpoints", [])
        for checkpoint in checkpoints:
            if checkpoint.get("id") != checkpoint_id:
                continue
            snapshot = checkpoint.get("snapshot") or {}
            if "ui_state" in snapshot:
                session["ui_state"] = self._normalize_ui_state(snapshot.get("ui_state") or None)
            if "mission" in snapshot:
                session["mission"] = self._normalize_mission(snapshot.get("mission") or None)
            if "workspace" in snapshot:
                session["workspace"] = snapshot.get("workspace")
            updated = self.save_session(session_id, session)
            return updated, checkpoint
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")

    def create_task(
        self,
        session_id: str,
        *,
        title: str,
        objective: str | None = None,
        phase: str = "planner",
        status: str = "todo",
        workspace: str | None = None,
        notes: str | None = None,
    ) -> tuple[dict, dict]:
        session = self.get_session(session_id)
        task = self._normalize_task(
            {
                "id": uuid4().hex,
                "title": title,
                "objective": objective,
                "phase": phase,
                "status": status,
                "workspace": workspace,
                "notes": notes,
                "created_at": _now_iso(),
                "updated_at": _now_iso(),
            }
        )
        tasks = session.setdefault("tasks", [])
        tasks.append(task)
        session["tasks"] = tasks[-120:]
        updated = self.save_session(session_id, session)
        return updated, task

    def update_task(self, session_id: str, task_id: str, patch: dict) -> tuple[dict, dict]:
        session = self.get_session(session_id)
        tasks = session.setdefault("tasks", [])
        for task in tasks:
            if task.get("id") != task_id:
                continue
            merged = {**task, **{k: v for k, v in patch.items() if v is not None}}
            merged["updated_at"] = _now_iso()
            normalized = self._normalize_task(merged)
            task.clear()
            task.update(normalized)
            updated = self.save_session(session_id, session)
            return updated, task
        raise FileNotFoundError(f"Task not found: {task_id}")

    def _normalize_task(self, task: dict | None) -> dict:
        payload = dict(task or {})
        return {
            "id": payload.get("id") or uuid4().hex,
            "title": payload.get("title") or "Nova tarefa",
            "objective": payload.get("objective"),
            "phase": payload.get("phase") or "planner",
            "status": payload.get("status") or "todo",
            "workspace": payload.get("workspace"),
            "notes": payload.get("notes"),
            "created_at": payload.get("created_at") or _now_iso(),
            "updated_at": payload.get("updated_at") or _now_iso(),
        }

    def _normalize_mission(self, mission: dict | None) -> dict:
        payload = dict(mission or {})
        return {
            "objective": payload.get("objective"),
            "status": payload.get("status") or "idle",
            "next_steps": list(payload.get("next_steps") or []),
            "updated_at": _now_iso(),
        }

    def _normalize_attachments(self, attachments: list[dict] | None) -> list[dict]:
        normalized: list[dict] = []
        for index, item in enumerate(attachments or []):
            payload = dict(item or {})
            name = str(payload.get("name") or "").strip()
            content = str(payload.get("content") or "")
            if not name or not content:
                continue
            normalized.append(
                {
                    "id": str(payload.get("id") or f"attachment-{index + 1}"),
                    "name": name[:240],
                    "content": content[:20_000],
                    "size": int(payload.get("size") or len(content.encode("utf-8"))),
                }
            )
            if len(normalized) >= 8:
                break
        return normalized

    def _normalize_meta(self, meta: dict | None) -> dict:
        payload = dict(meta or {})
        return {
            "pinned": bool(payload.get("pinned")),
            "archived": bool(payload.get("archived")),
        }

    def _session_preview(self, session: dict) -> str:
        mission_objective = ((session.get("mission") or {}).get("objective") or "").strip()
        if mission_objective:
            return mission_objective[:160]
        for message in reversed(session.get("messages") or []):
            content = str(message.get("display_content") or message.get("content") or "").strip().replace("\n", " ")
            if content:
                return content[:160]
        return ""

    def _normalize_ui_state(self, ui_state: dict | None) -> dict:
        payload = dict(ui_state or {})
        open_files = []
        for item in payload.get("open_files") or []:
            value = str(item or "").strip()
            if value and value not in open_files:
                open_files.append(value)
        return {
            "active_file": payload.get("active_file"),
            "open_files": open_files,
            "quick_flow_mode": payload.get("quick_flow_mode"),
            "quick_target_path": payload.get("quick_target_path"),
            "quick_goal": payload.get("quick_goal"),
            "draft_prompt": payload.get("draft_prompt"),
            "editor_instruction": payload.get("editor_instruction"),
            "terminal_command": payload.get("terminal_command"),
            "workbench_mode": payload.get("workbench_mode"),
            "updated_at": _now_iso(),
        }

    def _derive_checkpoint_title(self, session: dict) -> str:
        active_file = ((session.get("ui_state") or {}).get("active_file") or "").strip()
        mission_objective = ((session.get("mission") or {}).get("objective") or "").strip()
        if active_file:
            return f"Checkpoint em {active_file}"
        if mission_objective:
            return mission_objective[:80]
        return "Checkpoint operacional"

    def _path(self, session_id: str) -> Path:
        return self.root / f"{session_id}.json"

    def _derive_title(self, *, user_content: str, user_display_content: str | None) -> str:
        raw_title = (user_display_content or user_content).strip()
        if not raw_title:
            return "Nova conversa"
        lines = [line.strip() for line in raw_title.splitlines() if line.strip()]
        if not lines:
            return "Nova conversa"
        first_line = lines[0]
        if first_line.startswith("[WORKSPACE:") and "]" in first_line:
            _, _, remainder = first_line.partition("]")
            first_line = remainder.strip() or (lines[1] if len(lines) > 1 else "")
        return first_line[:80] or "Nova conversa"

    def _read(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _write(self, path: Path, payload: dict) -> None:
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
