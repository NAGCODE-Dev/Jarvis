from __future__ import annotations

from dataclasses import dataclass

from jarvis.config import settings


@dataclass(frozen=True)
class AgentProfile:
    visible_model: str
    system_prompt_file: str
    primary_model: str
    fallback_model: str
    kind: str


AGENTS: dict[str, AgentProfile] = {
    "jarvis": AgentProfile(
        visible_model="jarvis",
        system_prompt_file="jarvis.md",
        primary_model=settings.planner_model,
        fallback_model=settings.planner_fallback_model,
        kind="orchestrator",
    ),
    "jarvis-coach": AgentProfile(
        visible_model="jarvis-coach",
        system_prompt_file="coach.md",
        primary_model=settings.planner_model,
        fallback_model=settings.planner_fallback_model,
        kind="coach",
    ),
    "jarvis-professor": AgentProfile(
        visible_model="jarvis-professor",
        system_prompt_file="professor.md",
        primary_model=settings.planner_model,
        fallback_model=settings.planner_fallback_model,
        kind="professor",
    ),
    "jarvis-programador": AgentProfile(
        visible_model="jarvis-programador",
        system_prompt_file="programador.md",
        primary_model=settings.coder_model,
        fallback_model=settings.coder_fallback_model,
        kind="coder",
    ),
    "jarvis-pesquisador": AgentProfile(
        visible_model="jarvis-pesquisador",
        system_prompt_file="pesquisador.md",
        primary_model=settings.planner_model,
        fallback_model=settings.planner_fallback_model,
        kind="researcher",
    ),
}

