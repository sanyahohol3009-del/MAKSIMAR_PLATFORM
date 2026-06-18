from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_guarded_answer_engine import (
    _asks_pc_action,
    _asks_weather_or_current_facts,
)
from tools.jarvis_live_runtime.memory_context_sources import _needs_deep_memory


def _route_mode(text: str) -> str:
    return _plan_jarvis_request(text)["route_mode"]


def _plan_jarvis_request(text: str) -> dict[str, str]:
    lowered = text.casefold()
    if _asks_pc_action(lowered):
        return {
            "request_route": "pc_action_proposal",
            "route_mode": "FAST",
            "retrieval_mode": "session_only",
        }
    if _asks_weather_or_current_facts(lowered):
        return {
            "request_route": "current_facts_tool",
            "route_mode": "FAST",
            "retrieval_mode": "session_only",
        }
    if _is_deep_code_request(lowered):
        return {
            "request_route": "code_deep",
            "route_mode": "DEEP",
            "retrieval_mode": "deep_memory",
        }
    if _is_simple_code_request(lowered):
        return {
            "request_route": "code_simple",
            "route_mode": "DEEP",
            "retrieval_mode": "targeted_memory",
        }
    if _needs_deep_memory(lowered):
        return {
            "request_route": "project_memory",
            "route_mode": "DEEP",
            "retrieval_mode": "deep_memory",
        }
    return {
        "request_route": "conversation",
        "route_mode": "FAST",
        "retrieval_mode": "session_only",
    }


def _is_simple_code_request(lowered: str) -> bool:
    markers = ("pytest", "brokenpipeerror", "ошибка", "traceback", "код", "тест", "python")
    return any(marker in lowered for marker in markers)


def _is_deep_code_request(lowered: str) -> bool:
    markers = ("architecture", "архитектур", "сложн", "complex", "approval gate", "patch proposal")
    return any(marker in lowered for marker in markers) and _is_simple_code_request(lowered)


def _needs_project_status(text: str) -> bool:
    lowered = text.casefold()
    return any(
        marker in lowered
        for marker in (
            "проект",
            "статус",
            "git",
            "ветка",
            "runtime_history_store",
            "структур",
            "дерево",
            "файл",
            "ядро",
            "repo",
            "workspace",
        )
    )
