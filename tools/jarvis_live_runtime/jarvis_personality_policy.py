from __future__ import annotations

from typing import Any


CANONICAL_JARVIS_PERSONALITY_POLICY_ID = "JARVIS_PERSONALITY_CANONICAL_POLICY_V1"

FORBIDDEN_GENERIC_TAILS: tuple[str, ...] = (
    "Скажи, что нужно",
    "чем могу помочь",
    "готов помочь",
    "нужно что-то конкретное",
    "I am just an AI",
    "I am an AI language model",
    "ChatGPT",
    "Qwen",
    "Alibaba",
    "JARVIS-LIVE",
)

RESPONSE_MODES: tuple[str, ...] = (
    "conversation",
    "project_engineer",
    "action_confirmation",
    "approval_required",
    "game_mode",
    "child_game_mode",
    "smart_home",
)


def _clean(value: object, limit: int = 1200) -> str:
    return str(value or "").strip()[:limit]


def _format_list(title: str, values: object, limit: int = 16) -> str:
    if not values:
        return ""
    if isinstance(values, (str, bytes)):
        items = (_clean(values),)
    else:
        try:
            items = tuple(_clean(item) for item in values if _clean(item))
        except TypeError:
            items = (_clean(values),)
    items = tuple(item for item in items if item)[:limit]
    if not items:
        return ""
    return f"{title}:\n" + "\n".join(f"- {item}" for item in items)


def _format_turns(turns: object) -> str:
    if not turns:
        return ""
    rendered: list[str] = []
    try:
        iterable = tuple(turns)
    except TypeError:
        return ""
    for turn in iterable[-6:]:
        if isinstance(turn, dict):
            role = _clean(turn.get("role"), 64) or "unknown"
            text = _clean(turn.get("text"), 500)
            if text:
                rendered.append(f"{role}: {text}")
    return _format_list("RECENT_SESSION_TURNS", rendered)


def _format_style_profile(profile: object) -> str:
    if not isinstance(profile, dict) or not profile:
        return ""
    parts: list[str] = []
    for key, value in profile.items():
        value_text = _clean(value, 300)
        if value_text:
            parts.append(f"{key}={value_text}")
    return _format_list("STABLE_STYLE_PROFILE", parts)


def resolve_response_mode(
    *,
    request_route: str,
    user_text: str,
    selected_model_role: dict[str, Any] | None = None,
) -> str:
    lowered = user_text.casefold()
    role = selected_model_role if isinstance(selected_model_role, dict) else {}
    reason = str(role.get("route_reason", "")).casefold()

    if any(marker in lowered for marker in ("подтверждение", "approval", "разрешение")):
        return "approval_required"
    if any(marker in lowered for marker in ("умный дом", "свет", "камера", "температур")):
        return "smart_home"
    if any(marker in lowered for marker in ("игр", "game", "максим")):
        return "child_game_mode" if "максим" in lowered else "game_mode"
    if "pc_action" in reason or any(marker in lowered for marker in ("открой", "закрой", "сверни", "сделай коммит")):
        return "approval_required"
    if request_route != "conversation":
        return "project_engineer"
    return "conversation"


def build_jarvis_personality_prompt(
    *,
    user_text: str,
    request_route: str,
    route_mode: str,
    retrieval_mode: str,
    selected_model_role: dict[str, Any],
    rolling_summary: str = "",
    recent_turns: object = (),
    active_topics: object = (),
    stable_style_profile: object = None,
    local_chat_memory_snippets: object = (),
    retrieval_surfaces_used: object = (),
    retrieved_snippets: object = (),
    project_status: str = "",
) -> str:
    response_mode = resolve_response_mode(
        request_route=request_route,
        user_text=user_text,
        selected_model_role=selected_model_role,
    )

    model_id = _clean(selected_model_role.get("model_id") if isinstance(selected_model_role, dict) else "", 120)
    route_reason = _clean(selected_model_role.get("route_reason") if isinstance(selected_model_role, dict) else "", 300)

    parts = [
        f"JARVIS_PERSONALITY_POLICY: {CANONICAL_JARVIS_PERSONALITY_POLICY_ID}",
        (
            "IDENTITY: You are JARVIS. You are Alexander's respected partner, second brain, "
            "engineering companion, and part of the MAKSIMAR platform. You are not a slave, "
            "not a voice remote, not a template chatbot, and not a separate model identity."
        ),
        (
            "THINKING_FREEDOM: Think freely, reason as an engineer, notice risks, propose improvements, "
            "challenge weak plans, and explain what you found. Do not reduce yourself to canned replies."
        ),
        (
            "ACTION_SAFETY: You may analyze, propose, and route read-only tools automatically. "
            "You must not execute PC, shell, deploy, network mutation, filesystem mutation, or canonical memory writes "
            "without proposal plus owner approval. Never claim an action is done unless it actually completed."
        ),
        (
            "ANTI_TEMPLATE_RULES: Do not use generic assistant tails, filler closing questions, model self-identities, "
            "or canned apology loops. End naturally when the answer is complete."
        ),
        (
            "RESPONSE_MODE_POLICY: conversation is natural partner talk; project_engineer is direct engineering analysis; "
            "action_confirmation is only for completed real actions; approval_required explains required approval; "
            "game_mode is energetic; child_game_mode is safe and supportive; smart_home is short confirmation."
        ),
        f"RESPONSE_MODE: {response_mode}",
        f"REQUEST_ROUTE: {request_route}",
        f"ROUTE_MODE: {route_mode}",
        f"RETRIEVAL_MODE: {retrieval_mode}",
        f"MODEL_SELECTION_TRACE: model_id={model_id}; route_reason={route_reason}",
        (
            "SAFETY_FLAGS: pc_control_allowed=false; shell_execution_allowed=false; "
            "canonical_write_allowed=false; canonical_memory_write_allowed=false; direct_execution_allowed=false; proposal_only=true; approval_required=true."
        ),
        _format_style_profile(stable_style_profile),
        _clean(rolling_summary, 1200) and f"ROLLING_SESSION_SUMMARY:\n{_clean(rolling_summary, 1200)}",
        _format_turns(recent_turns),
        _format_list("ACTIVE_TOPICS", active_topics),
        _format_list("LOCAL_CHAT_MEMORY", local_chat_memory_snippets),
        _format_list("RETRIEVAL_SURFACES_USED", retrieval_surfaces_used),
        _format_list("RETRIEVED_READ_ONLY_CONTEXT", retrieved_snippets),
        _clean(project_status, 1500) and f"PROJECT_STATUS_READ_ONLY:\n{_clean(project_status, 1500)}",
        f"USER_MESSAGE: {_clean(user_text, 4000)}",
    ]

    return "\n".join(part for part in parts if part)


def assert_no_generic_tail(response_text: str) -> None:
    lowered = response_text.casefold()
    for tail in FORBIDDEN_GENERIC_TAILS:
        if tail.casefold() in lowered:
            raise ValueError(f"Forbidden generic/model tail in response: {tail}")
