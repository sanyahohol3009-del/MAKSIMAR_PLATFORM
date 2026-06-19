from __future__ import annotations

from MAKSIMAR_CORE_LIB.swarm_coordination import SwarmStatusReadModel


def test_swarm_status_read_model_smoke() -> None:
    read_model = SwarmStatusReadModel(
        read_model_id="swarm_status_read_model_test_v1",
        active_agents=("tool_selector_agent",),
        selected_model_role="jarvis_chat_model",
        selected_tools=("weather_lookup",),
        conflict_status="clear",
        heavy_gpu_lock_status="unlocked",
        direct_execution_disabled_for_swarm=True,
        safe_action_delegated_to_action_library=True,
    ).to_read_model()

    assert read_model["active_agents"] == ("tool_selector_agent",)
    assert read_model["selected_model_role"] == "jarvis_chat_model"
    assert read_model["selected_tools"] == ("weather_lookup",)
    assert read_model["conflict_status"] == "clear"
