from __future__ import annotations

from dataclasses import dataclass
import fcntl
import os
import shlex
import shutil
from pathlib import Path
import pty
import select
import signal
import struct
import subprocess
import termios
import time
from uuid import uuid4

from jarvis.config import settings


@dataclass
class TerminalSession:
    session_id: str
    fd: int
    process: subprocess.Popen[str]
    cwd: Path
    created_at: float


class TerminalService:
    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or settings.workspace_root).resolve()
        self.sessions: dict[str, TerminalSession] = {}

    def create_session(self, cwd: str | None = None, cols: int = 120, rows: int = 32) -> dict:
        workdir = self._resolve(cwd)
        master_fd, slave_fd = pty.openpty()
        self._set_winsize(slave_fd, rows=rows, cols=cols)

        shell = settings.terminal_shell
        argv = [shell, "-i"]
        if Path(shell).name == "bash":
            argv = [shell, "--noprofile", "--norc", "-i"]

        env = os.environ.copy()
        env.setdefault("TERM", "xterm-256color")
        env.setdefault("COLORTERM", "truecolor")
        env.setdefault("PS1", "jarvis$ ")

        process = subprocess.Popen(
            argv,
            cwd=workdir,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            text=False,
            env=env,
            start_new_session=True,
        )
        os.close(slave_fd)
        self._set_nonblocking(master_fd)

        session_id = uuid4().hex
        session = TerminalSession(
            session_id=session_id,
            fd=master_fd,
            process=process,
            cwd=workdir,
            created_at=time.time(),
        )
        self.sessions[session_id] = session
        initial_output = self.read(session_id)["output"]
        return {
            "session_id": session_id,
            "cwd": "." if workdir == self.root else workdir.relative_to(self.root).as_posix(),
            "pid": process.pid,
            "output": initial_output,
        }

    def list_sessions(self) -> list[dict]:
        items: list[dict] = []
        for session_id in list(self.sessions.keys()):
            session = self._require_session(session_id)
            items.append(
                {
                    "session_id": session.session_id,
                    "cwd": "." if session.cwd == self.root else session.cwd.relative_to(self.root).as_posix(),
                    "pid": session.process.pid,
                    "alive": session.process.poll() is None,
                }
            )
        return items

    def write(self, session_id: str, data: str, wait_ms: int = 120) -> dict:
        session = self._require_session(session_id)
        os.write(session.fd, data.encode("utf-8"))
        return self.read(session_id, wait_ms=wait_ms)

    def read(self, session_id: str, wait_ms: int = 0) -> dict:
        session = self._require_session(session_id)
        if wait_ms > 0:
            timeout = wait_ms / 1000.0
            select.select([session.fd], [], [], timeout)

        chunks: list[bytes] = []
        total_bytes = 0
        truncated = False
        while True:
            try:
                chunk = os.read(session.fd, 4096)
                if not chunk:
                    break
                chunks.append(chunk)
                total_bytes += len(chunk)
                if total_bytes >= settings.terminal_read_chunk_bytes:
                    truncated = True
                    break
            except BlockingIOError:
                break
            except OSError:
                break

        output = b"".join(chunks)
        if truncated:
            output = output[: settings.terminal_read_chunk_bytes]
        return {
            "session_id": session_id,
            "output": output.decode("utf-8", errors="ignore"),
            "alive": session.process.poll() is None,
            "exit_code": session.process.poll(),
            "truncated": truncated,
        }

    def resize(self, session_id: str, cols: int, rows: int) -> dict:
        session = self._require_session(session_id)
        self._set_winsize(session.fd, rows=rows, cols=cols)
        return {"session_id": session_id, "cols": cols, "rows": rows}

    def send_signal(self, session_id: str, signal_name: str) -> dict:
        session = self._require_session(session_id)
        signal_value = {"int": signal.SIGINT, "term": signal.SIGTERM, "kill": signal.SIGKILL}.get(signal_name)
        if signal_value is None:
            raise ValueError(f"Unsupported signal: {signal_name}")
        os.killpg(session.process.pid, signal_value)
        return self.read(session_id, wait_ms=80)

    def close(self, session_id: str) -> None:
        session = self._require_session(session_id)
        try:
            if session.process.poll() is None:
                os.killpg(session.process.pid, signal.SIGTERM)
                session.process.wait(timeout=1.0)
        except Exception:
            try:
                os.killpg(session.process.pid, signal.SIGKILL)
            except Exception:
                pass
        try:
            os.close(session.fd)
        except OSError:
            pass
        self.sessions.pop(session_id, None)

    def open_native(self, cwd: str | None = None) -> dict:
        workdir = self._resolve(cwd)
        shell = settings.terminal_shell
        shell_name = Path(shell).name
        shell_command = f"cd {shlex.quote(str(workdir))}; exec {shlex.quote(shell)} -i"

        candidates = [
            ["x-terminal-emulator", "-e", shell, "-lc", shell_command],
            ["gnome-terminal", "--working-directory", str(workdir), "--", shell, "-lc", shell_command],
            ["konsole", "--workdir", str(workdir), "-e", shell, "-lc", shell_command],
            ["xfce4-terminal", "--working-directory", str(workdir), "-e", f"{shell} -lc {shlex.quote(shell_command)}"],
            ["alacritty", "--working-directory", str(workdir), "-e", shell, "-lc", shell_command],
            ["kitty", "--directory", str(workdir), shell, "-lc", shell_command],
        ]

        last_error: Exception | None = None
        for candidate in candidates:
            binary = candidate[0]
            if shutil.which(binary) is None:
                continue
            try:
                process = subprocess.Popen(candidate, cwd=workdir, start_new_session=True)
                return {
                    "cwd": "." if workdir == self.root else workdir.relative_to(self.root).as_posix(),
                    "launcher": binary,
                    "pid": process.pid,
                    "shell": shell_name,
                }
            except Exception as exc:
                last_error = exc
                continue

        if last_error is not None:
            raise RuntimeError(f"Native terminal launch failed: {last_error}")
        raise RuntimeError("No supported native terminal launcher found on this Linux system.")

    def run(self, command: str, cwd: str | None = None) -> dict:
        session = self.create_session(cwd=cwd)
        try:
            written = self.write(session["session_id"], f"{command}\n")
            time.sleep(0.05)
            tail = self.read(session["session_id"], wait_ms=150)
            combined = f"{written['output']}{tail['output']}"
            return {
                "command": command,
                "cwd": session["cwd"],
                "exit_code": tail.get("exit_code"),
                "output": combined,
                "truncated": written["truncated"] or tail["truncated"],
            }
        finally:
            self.close(session["session_id"])

    def _require_session(self, session_id: str) -> TerminalSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise FileNotFoundError(f"Terminal session not found: {session_id}")
        return session

    def _resolve(self, path: str | None) -> Path:
        target = (self.root / (path or ".")).resolve()
        if target != self.root and self.root not in target.parents:
            raise ValueError("Path escapes workspace root")
        return target

    def _set_nonblocking(self, fd: int) -> None:
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    def _set_winsize(self, fd: int, *, rows: int, cols: int) -> None:
        packed = struct.pack("HHHH", rows, cols, 0, 0)
        fcntl.ioctl(fd, termios.TIOCSWINSZ, packed)
