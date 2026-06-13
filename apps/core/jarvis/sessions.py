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

    def list_sessions(self) -> list[dict[str, str]]:
        sessions: list[dict[str, str]] = []
        for path in sorted(self.root.glob("*.json")):
            try:
                payload = self._read(path)
            except (OSError, json.JSONDecodeError, KeyError):
                continue
            sessions.append(
                {
                    "id": payload["id"],
                    "title": payload.get("title", "Untitled"),
                    "model": payload.get("model", "jarvis-safe"),
                    "workspace": payload.get("workspace") or "",
                    "updated_at": payload.get("updated_at", ""),
                }
            )
        sessions.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
        return sessions

    def create_session(self, *, title: str | None = None, model: str = "jarvis-safe", workspace: str | None = None) -> dict:
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
    ) -> dict:
        session = self.get_session(session_id)
        if workspace is not None:
            session["workspace"] = workspace
        session["model"] = model
        if not session.get("title") or session["title"] == "Nova conversa":
            session["title"] = self._derive_title(user_content=user_content, user_display_content=user_display_content)
        session.setdefault("messages", []).extend(
            [
                {
                    "role": "user",
                    "content": user_content,
                    **({"display_content": user_display_content} if user_display_content else {}),
                },
                {"role": "assistant", "content": assistant_content},
            ]
        )
        return self.save_session(session_id, session)

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
