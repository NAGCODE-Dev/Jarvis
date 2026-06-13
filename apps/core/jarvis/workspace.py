from __future__ import annotations

import os
from pathlib import Path

from jarvis.config import settings


class WorkspaceService:
    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or settings.workspace_root).resolve()

    def list_tree(self, path: str | None = None) -> dict:
        target = self._resolve(path)
        return self._serialize_dir(target, depth=0)

    def read_file(self, path: str) -> dict:
        target = self._resolve(path)
        if not target.is_file():
            raise FileNotFoundError(path)
        size = target.stat().st_size
        if size > settings.workspace_max_file_bytes:
            raise ValueError(f"File too large: {size} bytes")
        return {
            "path": self._relative(target),
            "content": target.read_text(encoding="utf-8"),
            "size": size,
        }

    def write_file(self, path: str, content: str, create: bool = False) -> dict:
        target = self._resolve(path)
        if not create and not target.exists():
            raise FileNotFoundError(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {
            "path": self._relative(target),
            "size": target.stat().st_size,
        }

    def create_directory(self, path: str) -> dict:
        target = self._resolve(path)
        target.mkdir(parents=True, exist_ok=True)
        return {
            "path": self._relative(target),
            "type": "directory",
        }

    def rename_path(self, source_path: str, target_path: str) -> dict:
        source = self._resolve(source_path)
        if not source.exists():
            raise FileNotFoundError(source_path)
        target = self._resolve(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        source.rename(target)
        return {
            "from_path": source_path,
            "path": self._relative(target),
            "type": "directory" if target.is_dir() else "file",
        }

    def delete_path(self, path: str) -> dict:
        target = self._resolve(path)
        if not target.exists():
            raise FileNotFoundError(path)
        if target.is_dir():
            self._delete_dir(target)
            deleted_type = "directory"
        else:
            target.unlink()
            deleted_type = "file"
        return {
            "path": path,
            "type": deleted_type,
        }

    def search(self, query: str, limit: int = 30) -> dict:
        normalized = query.strip().lower()
        if not normalized:
            return {"query": query, "results": []}

        results: list[dict] = []
        for current_root, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [name for name in dirnames if not name.startswith(".git")]
            current_dir = Path(current_root)

            for filename in sorted(filenames):
                file_path = current_dir / filename
                relative_path = self._relative(file_path)
                path_match = normalized in relative_path.lower()
                content_match = None

                try:
                    size = file_path.stat().st_size
                except OSError:
                    continue

                if size <= settings.workspace_max_file_bytes:
                    try:
                        text = file_path.read_text(encoding="utf-8")
                    except Exception:
                        text = ""
                    if text:
                        content_match = self._match_snippet(text, normalized)

                if not path_match and content_match is None:
                    continue

                results.append(
                    {
                        "path": relative_path,
                        "name": file_path.name,
                        "type": "file",
                        "path_match": path_match,
                        "snippet": content_match,
                    }
                )
                if len(results) >= limit:
                    return {"query": query, "results": results}

        return {"query": query, "results": results}

    def _resolve(self, path: str | None) -> Path:
        target = (self.root / (path or ".")).resolve()
        if target != self.root and self.root not in target.parents:
            raise ValueError("Path escapes workspace root")
        return target

    def _relative(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def _serialize_dir(self, path: Path, depth: int) -> dict:
        if not path.exists():
            raise FileNotFoundError(path.as_posix())
        node = {
            "path": "." if path == self.root else self._relative(path),
            "name": path.name if path != self.root else self.root.name,
            "type": "directory" if path.is_dir() else "file",
        }
        if not path.is_dir():
            node["size"] = path.stat().st_size
            return node
        if depth >= settings.workspace_tree_max_depth:
            node["truncated"] = True
            return node
        children = []
        for child in sorted(path.iterdir(), key=lambda item: (item.is_file(), item.name.lower())):
            if child.name.startswith(".git"):
                continue
            if child.is_file() and child.stat().st_size > settings.workspace_max_file_bytes:
                children.append(
                    {
                        "path": self._relative(child),
                        "name": child.name,
                        "type": "file",
                        "size": child.stat().st_size,
                        "truncated": True,
                    }
                )
                continue
            children.append(self._serialize_dir(child, depth + 1))
        node["children"] = children
        return node

    def _delete_dir(self, path: Path) -> None:
        for child in path.iterdir():
            if child.is_dir():
                self._delete_dir(child)
            else:
                child.unlink()
        path.rmdir()

    def _match_snippet(self, text: str, normalized_query: str) -> str | None:
        lowered = text.lower()
        index = lowered.find(normalized_query)
        if index == -1:
            return None
        start = max(0, index - 80)
        end = min(len(text), index + len(normalized_query) + 120)
        snippet = text[start:end].replace("\n", " ").strip()
        if start > 0:
            snippet = f"...{snippet}"
        if end < len(text):
            snippet = f"{snippet}..."
        return snippet
