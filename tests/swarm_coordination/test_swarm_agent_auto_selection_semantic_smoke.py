from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from tools.jarvis_live_runtime.owner_identity_claim import OwnerIdentityClaim


def _verified_terminal_claim() -> OwnerIdentityClaim:
    return OwnerIdentityClaim(
        claim_id="swarm_semantic_verified_terminal_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def test_swarm_agent_auto_selection_semantic_smoke() -> None:
    broken = route_swarm_task(
        "посмотри почему всё сломалось после последнего изменения",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    weather = route_swarm_task(
        "мне надо понять погоду без ручных команд",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    screen = route_swarm_task(
        "найди подходящий инструмент для чтения экрана",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    workflow = route_swarm_task(
        "собери цепочку: найди файл, проверь тест, предложи исправление",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )

    assert broken.selected_agent_role == "project_coder_agent"
    assert broken.selected_model_role_id == "daily_coder_model"
    assert weather.selected_agent_role == "tool_selector_agent"
    assert weather.selected_tools == ("weather_lookup",)
    assert screen.selected_agent_role == "tool_selector_agent"
    assert screen.selected_tools == ("screen_observer_read",)
    assert workflow.selected_agent_role == "project_coder_agent"
    assert workflow.task_contract.normalized_intent == "code_debug"
    assert "repo_search" in workflow.selected_tools
