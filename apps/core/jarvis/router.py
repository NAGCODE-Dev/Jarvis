from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from jarvis.agents import AGENTS, AgentProfile
from jarvis.knowledge import KnowledgeService
from jarvis.memory import MemoryService
from jarvis.model_registry import ModelRegistry
from jarvis.ollama_client import OllamaClient
from jarvis.prompting import load_prompt
from jarvis.schemas import ChatMessage


RouteKind = Literal["coach", "professor", "coder", "researcher", "planner", "complex-coder"]


@dataclass
class RouteDecision:
    agent: AgentProfile
    route_kind: RouteKind
    use_rag: bool = False
    workspace: str | None = None
    context_fields: list[str] | None = None


class JarvisRouter:
    def __init__(self, ollama: OllamaClient, memory: MemoryService, knowledge: KnowledgeService) -> None:
        self.ollama = ollama
        self.memory = memory
        self.knowledge = knowledge
        self.registry = ModelRegistry()

    def list_models(self) -> list[dict[str, str]]:
        return [{"id": key, "object": "model", "owned_by": "jarvis-local"} for key in AGENTS]

    def complete(self, visible_model: str, messages: list[ChatMessage], temperature: float | None = None) -> str:
        agent = AGENTS.get(visible_model, AGENTS["jarvis"])
        model_profile = self._model_profile(visible_model)
        if agent.visible_model in {"jarvis", "jarvis-safe"}:
            decision = self._route(messages, model_profile=model_profile)
        else:
            decision = RouteDecision(agent=agent, route_kind=agent.kind if agent.kind != "orchestrator" else "planner")
        return self._dispatch(decision, messages, temperature=temperature, model_profile=model_profile)

    def _model_profile(self, visible_model: str) -> Literal["safe", "quality"]:
        return "safe" if visible_model.endswith("-safe") or visible_model == "jarvis-safe" else "quality"

    def _route(self, messages: list[ChatMessage], model_profile: Literal["safe", "quality"] = "quality") -> RouteDecision:
        prompt = " ".join(message.content.lower() for message in messages if message.role == "user")
        coach_agent = AGENTS["jarvis-coach"]
        professor_agent = AGENTS["jarvis-professor"]
        programmer_agent = AGENTS["jarvis-programador-safe"] if model_profile == "safe" else AGENTS["jarvis-programador"]
        researcher_agent = AGENTS["jarvis-pesquisador-safe"] if model_profile == "safe" else AGENTS["jarvis-pesquisador"]
        orchestrator_agent = AGENTS["jarvis-safe"] if model_profile == "safe" else AGENTS["jarvis"]
        if any(token in prompt for token in ("treino", "crossfit", "muscula", "periodização", "workout")):
            return RouteDecision(
                agent=coach_agent,
                route_kind="coach",
                workspace="crossfit",
                context_fields=["weight.current_kg", "constraints.available_time", "goals.training_focus"],
            )
        if any(token in prompt for token in ("faculdade", "estudo", "resumo", "prova", "learn", "study")):
            return RouteDecision(
                agent=professor_agent,
                route_kind="professor",
                workspace="faculdade",
                context_fields=["goals.study_focus", "preferences.response_style"],
            )
        if any(token in prompt for token in ("documento", "pdf", "arquivo", "base de conhecimento", "knowledge base", "artigo")):
            return RouteDecision(
                agent=researcher_agent,
                route_kind="researcher",
                use_rag=True,
                workspace=self._infer_workspace(prompt),
            )
        if any(token in prompt for token in ("código", "codigo", "debug", "bug", "stack trace", "python", "typescript", "arquitetura", "refactor")):
            if any(token in prompt for token in ("planeje e implemente", "planejar e executar", "complexo", "arquitetar e codar")):
                return RouteDecision(
                    agent=programmer_agent,
                    route_kind="complex-coder",
                    workspace="programacao",
                    context_fields=["preferences.editor", "preferences.coding_style"],
                )
            return RouteDecision(
                agent=programmer_agent,
                route_kind="coder",
                workspace="programacao",
                context_fields=["preferences.editor", "preferences.coding_style"],
            )
        if any(token in prompt for token in ("peso", "altura", "idade", "aniversário", "birthday")):
            return RouteDecision(agent=orchestrator_agent, route_kind="planner", context_fields=["profile.name", "weight.current_kg", "profile.birth_date"])
        return RouteDecision(agent=orchestrator_agent, route_kind="planner", workspace=self._infer_workspace(prompt))

    def _infer_workspace(self, prompt: str) -> str | None:
        for workspace in ("minecraft", "faculdade", "jarvis", "crossfit", "programacao"):
            if workspace in prompt:
                return workspace
        return None

    def _dispatch(
        self,
        decision: RouteDecision,
        messages: list[ChatMessage],
        temperature: float | None = None,
        model_profile: Literal["safe", "quality"] = "quality",
    ) -> str:
        system_prompt = load_prompt(decision.agent.system_prompt_file)
        context = self.memory.resolve_context(fields=decision.context_fields, workspace=decision.workspace, include_archive=False)
        context_lines = [
            "Context policy:",
            "- Use identity and state facts only if they are relevant.",
            "- Treat workspace notes as scoped context.",
        ]
        if context["identity"]:
            context_lines.append(f"Identity facts: {context['identity']}")
        if context["state"]:
            context_lines.append(f"State facts: {context['state']}")
        if context["workspace"]:
            context_lines.append(f"Workspace facts: {context['workspace']}")

        enriched_messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="system", content="\n".join(context_lines)),
            *messages,
        ]

        if decision.use_rag:
            query = next((message.content for message in reversed(messages) if message.role == "user"), "")
            domain = decision.workspace
            results = self.knowledge.search(query=query, top_k=4, domain=domain)
            if results:
                context_block = "\n\n".join(
                    f"[{result.metadata.get('source_path', 'unknown')}] {result.text}" for result in results
                )
                enriched_messages.insert(
                    2,
                    ChatMessage(
                        role="system",
                        content=f"Retrieved knowledge context:\n{context_block}\n\nReference sources explicitly when using this context.",
                    ),
                )

        if decision.route_kind == "complex-coder":
            planner_primary, planner_fallback = self._resolve_primary("planning", decision.agent, model_profile)
            plan = self._call_with_fallback(
                "planning",
                planner_primary,
                planner_fallback,
                [ChatMessage(role="system", content="Produce a short execution plan in bullet points."), *messages],
                temperature=0.2,
            )
            execution_messages = [
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="system", content=f"Use this plan created by the planner model as guidance:\n{plan}"),
                *messages,
            ]
            coding_primary, coding_fallback = self._resolve_primary("coding", decision.agent, model_profile)
            result = self._call_with_fallback("coding", coding_primary, coding_fallback, execution_messages, temperature=temperature)
            return f"Plan:\n{plan}\n\nExecution:\n{result}"

        task_type = "coding" if decision.route_kind in {"coder", "complex-coder"} else "planning"
        primary, fallback = self._resolve_primary(task_type, decision.agent, model_profile)
        return self._call_with_fallback(task_type, primary, fallback, enriched_messages, temperature=temperature)

    def _resolve_primary(
        self,
        task_type: str,
        agent: AgentProfile,
        model_profile: Literal["safe", "quality"],
    ) -> tuple[str, str]:
        if model_profile == "safe":
            if task_type == "coding":
                return agent.primary_model, agent.fallback_model
            return agent.primary_model, agent.fallback_model
        return self.registry.resolve_primary(task_type)

    def _call_with_fallback(
        self,
        task_type: str,
        primary_model: str,
        fallback_model: str,
        messages: list[ChatMessage],
        temperature: float | None = None,
    ) -> str:
        installed = self._installed_models()
        candidates = self.registry.resolve_runtime_candidates(task_type, [primary_model, fallback_model], installed)
        last_error: Exception | None = None
        for model in candidates:
            try:
                return self.ollama.chat(model, messages, temperature=temperature)
            except Exception as exc:
                last_error = exc
        if last_error is not None:
            raise last_error
        raise RuntimeError("No installed Ollama models available for this task.")

    def _installed_models(self) -> list[str]:
        try:
            payload = self.ollama.list_models()
            return [model.get("name", "") for model in payload.get("models", []) if model.get("name")]
        except Exception:
            return []
