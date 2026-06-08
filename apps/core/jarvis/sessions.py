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
            payload = self._read(path)
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
            session["title"] = user_content.strip().splitlines()[0][:80] or "Nova conversa"
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

    def _read(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _write(self, path: Path, payload: dict) -> None:
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
