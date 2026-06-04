from MAKSIMAR_CORE_LIB.workflow_engine.workflow_status_bridge import (
    build_workflow_dashboard_read_only_projection,
)


def test_workflow_dashboard_projection_is_read_only_and_non_executing() -> None:
    projection = build_workflow_dashboard_read_only_projection()
    payload = projection["payload"]

    assert projection["panel_kind"] == "read_only_status"
    assert projection["action_controls_enabled"] is False
    assert projection["execution_controls_enabled"] is False
    assert projection["mutation_controls_enabled"] is False
    assert payload["dashboard_read_only"] is True
    assert payload["dashboard_execution_allowed"] is False
    assert payload["runtime_execution_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["direct_core_write_allowed"] is False
    assert payload["direct_server_canonical_write_allowed"] is False
    assert payload["hidden_remote_control_allowed"] is False
    assert payload["direct_phone_control_allowed"] is False
