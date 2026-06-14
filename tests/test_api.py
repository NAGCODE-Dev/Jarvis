from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from jarvis.api import create_api_router
from jarvis.memory import MemoryAction, MemoryManager
from jarvis.router import JarvisRouter
from jarvis.schemas import ChatMessage
from jarvis.sessions import SessionStore


class FakeOllama:
    def health(self):
        return {"status": "ok", "models": ["qwen3:4b"]}

    def list_models(self):
        return {"models": [{"name": "qwen3:4b"}, {"name": "gemma4:e2b"}]}

    def embed(self, text, model=None):
        if isinstance(text, list):
            return [[0.1, 0.2] for _ in text]
        return [[0.1, 0.2]]

    def chat(self, model, messages, temperature=None):
        joined = "\n".join(getattr(message, "content", str(message)) for message in messages)
        if "Return a JSON object with keys summary and files." in joined:
            return json.dumps(
                {
                    "summary": "Edicao em lote pronta",
                    "files": [
                        {
                            "path": "hello.txt",
                            "content": "ok",
                        }
                    ],
                }
            )
        if "Return a JSON object with keys summary, suggested_command, edit_instruction." in joined:
            if "Recent terminal output:\n[none]" in joined:
                return json.dumps(
                    {
                        "summary": "Analise inicial pronta",
                        "suggested_command": "printf 'cycle-ok'",
                        "edit_instruction": "Atualize o arquivo para refletir o resultado",
                    }
                )
            return json.dumps(
                {
                    "summary": "Analise apos comando pronta",
                    "suggested_command": "",
                    "edit_instruction": "Atualize o arquivo com o resultado final",
                }
            )
        if "Return only the fully revised file content." in joined:
            return "ok"
        return "ok"

    def chat_stream(self, model, messages, temperature=None):
        yield "o"
        yield "k"


class FakeKnowledge:
    def health(self):
        return {"status": "ok", "collections": 1}

    def search(self, query, top_k=4, domain=None, score_threshold=None):
        return []

    def index_domains(self, domains=None, force=False):
        return {"indexed_files": 0, "indexed_chunks": 0}

    def ingest_note(self, *, domain, title, content, source_path=None, force=False):
        return {
            "stored_path": f"knowledge/{domain}/obsidian/{title}.md",
            "indexed_chunks": 1,
            "domain": domain,
        }


def test_router_exposes_models_and_streams(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module
    import jarvis.sessions as sessions_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "OllamaClient", FakeOllama)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)
    monkeypatch.setattr(sessions_module, "settings", test_settings)

    memory = MemoryManager()
    router = JarvisRouter(FakeOllama(), memory, FakeKnowledge())

    models = router.list_models()
    assert any(model["id"] == "jarvis-programador" for model in models)
    assert any(model["id"] == "jarvis-programador-safe" for model in models)

    chunks = list(router.complete_stream("jarvis-safe", [ChatMessage(role="user", content="oi")]))
    assert "".join(chunks) == "ok"
    metadata = router.describe_request("jarvis-programador", [ChatMessage(role="user", content="analise este codigo")])
    assert metadata["effective_agent"] == "jarvis-programador"
    assert metadata["task_type"] == "coding"


def test_memory_and_workspace_context(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "OllamaClient", FakeOllama)
    monkeypatch.setattr(registry_module, "settings", test_settings)

    memory = MemoryManager()
    memory.apply(MemoryAction(action="update_state", field="weight.current_kg", value=72, source="test"))
    memory.apply(MemoryAction(action="append_workspace_note", field="topic", value="context selection", source="test", workspace="jarvis"))

    context = memory.resolve_context(workspace="jarvis")
    assert context["state"]["weight.current_kg"] == 72
    assert context["workspace"]["name"] == "jarvis"
    assert context["workspace"]["facts"]["topic"] == "context selection"


def test_session_store_persists_messages_and_metadata(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.sessions as sessions_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(sessions_module, "settings", test_settings)

    store = SessionStore()
    session = store.create_session(
        model="jarvis-safe",
        workspace="jarvis",
        mission={"objective": "estabilizar jarvis", "status": "planning", "next_steps": ["revisar router"]},
        ui_state={
            "active_file": "apps/web/app.js",
            "open_files": ["apps/web/app.js", "apps/web/styles.css"],
            "quick_flow_mode": "implement",
            "terminal_tail": "pytest -q\nE   AssertionError",
            "pending_attachments": [{"name": "brief.md", "content": "objetivo atual", "size": 14}],
            "pending_edit_proposal": {
                "path": "apps/web/app.js",
                "instruction": "melhorar render",
                "proposed_content": "console.log('ok')",
                "diff": "@@ -1 +1 @@",
                "hunks": [{"index": 0, "tag": "replace", "original_start": 0, "original_end": 1, "proposed_start": 0, "proposed_end": 1, "original_lines": ["a"], "proposed_lines": ["b"], "preview": "@@ -1 +1 @@", "applied": False}],
            },
            "pending_task_assist": {
                "summary": "Corrigir render",
                "suggested_command": "pytest -q",
                "edit_instruction": "ajuste o fluxo",
                "edit_proposal": {"path": "apps/web/app.js", "proposed_content": "console.log('ok')", "diff": "@@", "hunks": []},
                "command_result": {"command": "pytest -q", "exit_code": 1, "output": "falhou"},
            },
        },
        meta={"pinned": True, "archived": False},
    )
    updated = store.append_exchange(
        session["id"],
        user_content="oi",
        user_display_content="Oi limpo",
        assistant_content="ok",
        model="jarvis-safe",
        workspace="jarvis",
        user_attachments=[{"name": "notes.txt", "content": "linha 1\nlinha 2", "size": 15}],
    )

    assert updated["messages"][0]["display_content"] == "Oi limpo"
    assert updated["messages"][0]["attachments"][0]["name"] == "notes.txt"
    assert "linha 1" in updated["messages"][0]["attachments"][0]["content"]
    assert updated["messages"][1]["content"] == "ok"
    assert updated["workspace"] == "jarvis"
    assert "metadata" not in updated["messages"][1]
    assert updated["title"] == "Oi limpo"
    assert updated["operations"] == []
    assert updated["approvals"] == []
    assert updated["mission"]["objective"] == "estabilizar jarvis"
    assert updated["mission"]["status"] == "planning"
    assert updated["ui_state"]["active_file"] == "apps/web/app.js"
    assert updated["ui_state"]["open_files"] == ["apps/web/app.js", "apps/web/styles.css"]
    assert "AssertionError" in (updated["ui_state"]["terminal_tail"] or "")
    assert updated["ui_state"]["pending_attachments"][0]["name"] == "brief.md"
    assert updated["ui_state"]["pending_edit_proposal"]["path"] == "apps/web/app.js"
    assert updated["ui_state"]["pending_task_assist"]["suggested_command"] == "pytest -q"
    assert updated["meta"]["pinned"] is True
    assert updated["meta"]["archived"] is False
    listed = store.list_sessions()
    assert listed[0]["pinned"] is True
    assert listed[0]["preview"] == "estabilizar jarvis"
    checkpointed, checkpoint = store.create_checkpoint(session["id"], title="checkpoint inicial", summary="estado inicial")
    assert checkpointed["checkpoints"][0]["title"] == "checkpoint inicial"
    restored, restored_checkpoint = store.restore_checkpoint(session["id"], checkpoint["id"])
    assert restored_checkpoint["id"] == checkpoint["id"]
    assert restored["ui_state"]["active_file"] == "apps/web/app.js"
    assert Path(test_settings.sessions_dir / f"{session['id']}.json").exists()


def test_session_store_ignores_workspace_prefix_in_generated_title(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.sessions as sessions_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(sessions_module, "settings", test_settings)

    store = SessionStore()
    session = store.create_session(model="jarvis-safe", workspace="jarvis")
    updated = store.append_exchange(
        session["id"],
        user_content="[WORKSPACE: jarvis]\nResponda ao projeto atual",
        user_display_content=None,
        assistant_content="ok",
        model="jarvis-safe",
        workspace="jarvis",
    )

    assert updated["title"] == "Responda ao projeto atual"


def test_api_updates_can_clear_workspace_and_missing_session_returns_404(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module
    import jarvis.sessions as sessions_module
    from fastapi import FastAPI

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "OllamaClient", FakeOllama)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)
    monkeypatch.setattr(sessions_module, "settings", test_settings)

    app = FastAPI()
    app.include_router(create_api_router(ollama=FakeOllama(), memory=MemoryManager(), knowledge=FakeKnowledge()))
    client = TestClient(app)

    created = client.post("/api/chat/sessions", json={"model": "jarvis-safe", "workspace": "jarvis"})
    assert created.status_code == 200
    session_id = created.json()["session"]["id"]

    cleared = client.put(
        f"/api/chat/sessions/{session_id}",
        json={
            "workspace": None,
            "mission": {"objective": "corrigir pwa", "status": "executando", "next_steps": ["validar smoke", "revisar diff"]},
            "ui_state": {
                "active_file": "apps/web/app.js",
                "open_files": ["apps/web/app.js", "apps/web/styles.css"],
                "quick_flow_mode": "fix-terminal",
                "quick_target_path": "apps/web/app.js",
                "quick_goal": "corrigir o streaming",
                "draft_prompt": "analise o terminal",
                "editor_instruction": "refatore o fluxo",
                "terminal_command": "pytest -q",
                "workbench_mode": "review",
            },
            "meta": {"pinned": True, "archived": False},
        },
    )
    assert cleared.status_code == 200
    assert cleared.json()["session"]["workspace"] is None
    assert cleared.json()["session"]["mission"]["objective"] == "corrigir pwa"
    assert cleared.json()["session"]["mission"]["status"] == "executando"
    assert cleared.json()["session"]["mission"]["next_steps"] == ["validar smoke", "revisar diff"]
    assert cleared.json()["session"]["ui_state"]["active_file"] == "apps/web/app.js"
    assert cleared.json()["session"]["ui_state"]["quick_flow_mode"] == "fix-terminal"
    assert cleared.json()["session"]["meta"]["pinned"] is True
    assert cleared.json()["session"]["meta"]["archived"] is False
    assert any(event["type"] == "session_context_updated" for event in cleared.json()["session"]["events"])

    operation = client.post(
        f"/api/chat/sessions/{session_id}/operations",
        json={
            "kind": "file_open",
            "title": "Abriu apps/web/app.js",
            "path": "apps/web/app.js",
            "detail": "arquivo aberto no editor",
            "metadata": {"source": "pwa"},
        },
    )
    assert operation.status_code == 200
    assert operation.json()["session"]["operations"][0]["kind"] == "file_open"

    checkpoint = client.post(
        f"/api/chat/sessions/{session_id}/checkpoints",
        json={"title": "checkpoint pwa", "summary": "antes da validação"},
    )
    assert checkpoint.status_code == 200
    checkpoint_id = checkpoint.json()["checkpoint"]["id"]
    assert checkpoint.json()["session"]["checkpoints"][0]["title"] == "checkpoint pwa"
    assert any(event["type"] == "checkpoint_created" for event in checkpoint.json()["session"]["events"])

    restored_checkpoint = client.post(f"/api/chat/sessions/{session_id}/checkpoints/{checkpoint_id}/restore")
    assert restored_checkpoint.status_code == 200
    assert restored_checkpoint.json()["session"]["ui_state"]["active_file"] == "apps/web/app.js"
    assert any(event["type"] == "checkpoint_restored" for event in restored_checkpoint.json()["session"]["events"])

    task_create = client.post(
        f"/api/chat/sessions/{session_id}/tasks",
        json={
            "title": "Validar roteador local",
            "objective": "fechar o ciclo planner executor verifier",
            "phase": "planner",
            "status": "todo",
            "workspace": "jarvis",
        },
    )
    assert task_create.status_code == 200
    task_id = task_create.json()["task"]["id"]
    assert task_create.json()["session"]["tasks"][0]["phase"] == "planner"

    task_update = client.put(
        f"/api/chat/sessions/{session_id}/tasks/{task_id}",
        json={"phase": "executor", "status": "in_progress"},
    )
    assert task_update.status_code == 200
    assert task_update.json()["task"]["phase"] == "executor"
    assert task_update.json()["task"]["status"] == "in_progress"
    assert any(event["type"] == "task_updated" for event in task_update.json()["session"]["events"])

    task_done = client.put(
        f"/api/chat/sessions/{session_id}/tasks/{task_id}",
        json={"phase": "memory", "status": "done"},
    )
    assert task_done.status_code == 200
    assert any(item.get("source") == "auto" and item.get("trigger_event") == "task_completed" for item in task_done.json()["session"].get("checkpoints", []))

    terminal_run = client.post(
        f"/api/terminal/run?session_id={session_id}",
        json={"command": "printf terminal-ok", "cwd": "."},
    )
    assert terminal_run.status_code == 200
    refreshed = client.get(f"/api/chat/sessions/{session_id}")
    assert refreshed.status_code == 200
    assert any(event["type"] == "command_executed" for event in refreshed.json()["session"]["events"])

    approval = client.post(
        f"/api/chat/sessions/{session_id}/approvals",
        json={
            "kind": "terminal_command",
            "title": "Rodar teste rapido",
            "command": "printf 'approval-ok'",
            "detail": "validacao operacional",
            "payload": {"command": "printf 'approval-ok'", "cwd": "."},
        },
    )
    assert approval.status_code == 200
    approval_id = approval.json()["approval"]["id"]
    assert approval.json()["session"]["approvals"][0]["kind"] == "terminal_command"

    applied = client.post(
        f"/api/chat/sessions/{session_id}/approvals/{approval_id}",
        json={"action": "apply"},
    )
    assert applied.status_code == 200
    assert applied.json()["approval"]["status"] == "applied"
    assert "approval-ok" in applied.json()["result"]["output"]
    assert any(item.get("source") == "auto" and item.get("trigger_event") == "approval_applied" for item in applied.json()["session"].get("checkpoints", []))

    missing = client.get("/api/chat/sessions/does-not-exist")
    assert missing.status_code == 404


def test_api_session_message_updates_hierarchical_memory(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module
    import jarvis.sessions as sessions_module
    from fastapi import FastAPI

    test_settings = config_module.Settings(
        data_dir=tmp_path / "data",
        config_dir=config_module.settings.config_dir,
        semantic_memory_enabled=False,
    )
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "OllamaClient", FakeOllama)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)
    monkeypatch.setattr(sessions_module, "settings", test_settings)

    memory = MemoryManager()
    app = FastAPI()
    app.include_router(create_api_router(ollama=FakeOllama(), memory=memory, knowledge=FakeKnowledge()))
    client = TestClient(app)

    created = client.post("/api/chat/sessions", json={"model": "jarvis-safe", "workspace": "jarvis"})
    session_id = created.json()["session"]["id"]

    response = client.post(
        f"/api/chat/sessions/{session_id}/message",
        json={
            "model": "jarvis-safe",
            "content": "continuar o projeto jarvis",
            "display_content": "Continuar o projeto Jarvis",
            "workspace": "jarvis",
            "attachments": [{"name": "brief.md", "content": "objetivo atual\n- estabilizar pwa", "size": 30}],
        },
    )

    assert response.status_code == 200
    assert response.json()["session"]["messages"][0]["attachments"][0]["name"] == "brief.md"
    assert response.json()["session"]["messages"][-1]["metadata"]["effective_agent"] == "jarvis-safe"
    payload = test_settings.current_context_path.read_text(encoding="utf-8")
    assert "Continuar o projeto Jarvis" in payload
    assert '"topic": "jarvis"' in payload

    status = client.get("/api/status")
    assert status.status_code == 200
    assert status.json()["memory"]["hierarchical"]["working_memory_messages"] == 2


def test_workspace_and_terminal_api(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module
    import jarvis.sessions as sessions_module
    import jarvis.terminal as terminal_module
    import jarvis.workspace as workspace_module
    from fastapi import FastAPI

    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    (workspace_root / "hello.txt").write_text("hello", encoding="utf-8")

    test_settings = config_module.Settings(
        data_dir=tmp_path / "data",
        config_dir=config_module.settings.config_dir,
        workspace_root=workspace_root,
    )
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "OllamaClient", FakeOllama)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)
    monkeypatch.setattr(sessions_module, "settings", test_settings)
    monkeypatch.setattr(terminal_module, "settings", test_settings)
    monkeypatch.setattr(workspace_module, "settings", test_settings)

    native_calls = []

    def fake_open_native(self, cwd=None):
        native_calls.append(cwd)
        return {"cwd": cwd or ".", "launcher": "x-terminal-emulator", "pid": 1234, "shell": "bash"}

    monkeypatch.setattr(terminal_module.TerminalService, "open_native", fake_open_native)

    app = FastAPI()
    app.include_router(create_api_router(ollama=FakeOllama(), memory=MemoryManager(), knowledge=FakeKnowledge()))
    client = TestClient(app)

    tree = client.get("/api/workspace/tree")
    assert tree.status_code == 200
    assert tree.json()["tree"]["type"] == "directory"

    read_file = client.get("/api/workspace/file", params={"path": "hello.txt"})
    assert read_file.status_code == 200
    assert read_file.json()["content"] == "hello"

    create_file = client.post("/api/workspace/file", json={"path": "notes/test.md", "content": "# hi"})
    assert create_file.status_code == 200
    assert (workspace_root / "notes" / "test.md").read_text(encoding="utf-8") == "# hi"

    create_dir = client.post("/api/workspace/directory", json={"path": "notes/subdir"})
    assert create_dir.status_code == 200
    assert (workspace_root / "notes" / "subdir").is_dir()

    update_file = client.put("/api/workspace/file", json={"path": "notes/test.md", "content": "# changed"})
    assert update_file.status_code == 200
    assert (workspace_root / "notes" / "test.md").read_text(encoding="utf-8") == "# changed"

    search = client.get("/api/workspace/search", params={"q": "changed", "limit": 10})
    assert search.status_code == 200
    assert search.json()["results"][0]["path"] == "notes/test.md"
    assert "changed" in (search.json()["results"][0]["snippet"] or "").lower()

    renamed = client.post("/api/workspace/rename", json={"source_path": "notes/test.md", "target_path": "notes/renamed.md"})
    assert renamed.status_code == 200
    assert not (workspace_root / "notes" / "test.md").exists()
    assert (workspace_root / "notes" / "renamed.md").read_text(encoding="utf-8") == "# changed"

    deleted = client.delete("/api/workspace/path", params={"path": "notes/renamed.md"})
    assert deleted.status_code == 200
    assert not (workspace_root / "notes" / "renamed.md").exists()

    edit_proposal = client.post(
        "/api/workspace/edit-proposal",
        json={
            "path": "hello.txt",
            "instruction": "Mude o conteúdo para ok",
            "model": "jarvis-programador-safe",
            "content": "hello",
            "workspace": "jarvis",
        },
    )
    assert edit_proposal.status_code == 200
    assert edit_proposal.json()["path"] == "hello.txt"
    assert "proposed_content" in edit_proposal.json()
    assert "diff" in edit_proposal.json()
    assert "hunks" in edit_proposal.json()

    batch_edit_proposal = client.post(
        "/api/workspace/batch-edit-proposal",
        json={
            "instruction": "Atualize os arquivos abertos",
            "model": "jarvis-programador-safe",
            "workspace": "jarvis",
            "files": [
                {"path": "hello.txt", "content": "hello"},
                {"path": "notes/second.md", "content": "second"},
            ],
        },
    )
    assert batch_edit_proposal.status_code == 200
    assert batch_edit_proposal.json()["summary"] == "Edicao em lote pronta"
    assert batch_edit_proposal.json()["proposals"][0]["path"] == "hello.txt"
    assert batch_edit_proposal.json()["proposals"][0]["proposed_content"] == "ok"

    task_assist = client.post(
        "/api/workspace/task-assist",
        json={
            "instruction": "Corrija o arquivo e sugira o próximo comando",
            "model": "jarvis-programador-safe",
            "path": "hello.txt",
            "content": "hello",
            "workspace": "jarvis",
            "terminal_output": "pytest falhou no arquivo ativo",
        },
    )
    assert task_assist.status_code == 200
    assert "summary" in task_assist.json()
    assert "suggested_command" in task_assist.json()
    assert "edit_proposal" in task_assist.json()

    workspace_session = client.post("/api/chat/sessions", json={"model": "jarvis-programador-safe", "workspace": "jarvis"})
    assert workspace_session.status_code == 200
    workspace_session_id = workspace_session.json()["session"]["id"]

    workspace_turn = client.post(
        f"/api/chat/sessions/{workspace_session_id}/workspace-turn",
        json={
            "model": "jarvis-programador-safe",
            "content": "Corrija o arquivo ativo e prepare a próxima ação.",
            "display_content": "Corrija o arquivo ativo e prepare a próxima ação.",
            "workspace": "jarvis",
            "path": "hello.txt",
            "file_content": "hello",
            "terminal_output": None,
            "attachments": [{"name": "context.txt", "content": "falha relevante", "size": 14}],
        },
    )
    assert workspace_turn.status_code == 200
    assert workspace_turn.json()["task_assist"]["summary"] == "Analise inicial pronta"
    assert len(workspace_turn.json()["approvals"]) == 2
    assert workspace_turn.json()["approvals"][0]["kind"] == "file_edit"
    assert workspace_turn.json()["approvals"][1]["kind"] == "terminal_command"
    assert workspace_turn.json()["session"]["messages"][-1]["metadata"]["workspace_turn"] is True
    assert workspace_turn.json()["session"]["messages"][-2]["attachments"][0]["name"] == "context.txt"
    assert workspace_turn.json()["session"]["operations"][-1]["kind"] == "workspace_turn"

    task_cycle = client.post(
        "/api/workspace/task-cycle",
        json={
            "instruction": "Corrija o arquivo e execute o proximo passo",
            "model": "jarvis-programador-safe",
            "path": "hello.txt",
            "content": "hello",
            "workspace": "jarvis",
            "terminal_output": None,
            "execute_command": True,
        },
    )
    assert task_cycle.status_code == 200
    assert task_cycle.json()["initial"]["suggested_command"] == "printf 'cycle-ok'"
    assert "cycle-ok" in task_cycle.json()["command_result"]["output"]
    assert task_cycle.json()["final"]["summary"] == "Analise apos comando pronta"

    terminal = client.post("/api/terminal/run", json={"command": "printf 'jarvis'", "cwd": "."})
    assert terminal.status_code == 200
    assert "jarvis" in terminal.json()["result"]["output"]

    native_terminal = client.post("/api/terminal/native", json={"cwd": "notes"})
    assert native_terminal.status_code == 200
    assert native_terminal.json()["result"]["launcher"] == "x-terminal-emulator"
    assert native_calls == ["notes"]

    created_terminal = client.post("/api/terminal/sessions", json={"cwd": ".", "cols": 80, "rows": 24})
    assert created_terminal.status_code == 200
    terminal_session_id = created_terminal.json()["session"]["session_id"]

    written = client.post(
        f"/api/terminal/sessions/{terminal_session_id}/write",
        json={"data": "printf 'abc'\\n", "wait_ms": 200},
    )
    assert written.status_code == 200
    follow_up_read = client.get(f"/api/terminal/sessions/{terminal_session_id}/read", params={"wait_ms": 200})
    assert follow_up_read.status_code == 200
    assert "abc" in f"{written.json()['result']['output']}{follow_up_read.json()['result']['output']}"

    resized = client.post(f"/api/terminal/sessions/{terminal_session_id}/resize", json={"cols": 100, "rows": 30})
    assert resized.status_code == 200

    interrupted = client.post(f"/api/terminal/sessions/{terminal_session_id}/signal", json={"signal": "int"})
    assert interrupted.status_code == 200

    closed = client.delete(f"/api/terminal/sessions/{terminal_session_id}")
    assert closed.status_code == 200


def test_hierarchical_memory_compacts_important_history(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module

    test_settings = config_module.Settings(
        data_dir=tmp_path / "data",
        config_dir=config_module.settings.config_dir,
        working_memory_limit=3,
        working_memory_preserve_recent=2,
    )
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "OllamaClient", FakeOllama)

    memory = MemoryManager()
    memory.record_exchange(
        user_content="Decidi usar Kotlin no app Android do projeto.",
        user_display_content="Decidi usar Kotlin no app Android do projeto.",
        assistant_content="Vamos manter Kotlin como base.",
        workspace=None,
        model="jarvis-codex",
    )
    memory.record_exchange(
        user_content="oi",
        user_display_content="oi",
        assistant_content="ok",
        workspace=None,
        model="jarvis-codex",
    )

    summary_path = test_settings.memory_dir / "summaries" / "programming.json"
    topic_path = test_settings.topic_memory_dir / "programming.md"
    active_path = test_settings.active_memory_dir / "programming.json"

    assert summary_path.exists()
    assert topic_path.exists()
    assert active_path.exists()
    assert "Kotlin" in summary_path.read_text(encoding="utf-8")
    assert "Kotlin" in topic_path.read_text(encoding="utf-8")
    assert "Kotlin" in active_path.read_text(encoding="utf-8")
