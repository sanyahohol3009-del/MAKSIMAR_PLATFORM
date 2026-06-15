from __future__ import annotations

from MAKSIMAR_CORE_LIB.app_safe_core.app_safe_core_boundary_contract import (
    build_app_safe_core_boundary_contract,
)


def test_app_safe_core_boundary_contract_is_read_only_intent_only() -> None:
    read_model = build_app_safe_core_boundary_contract().to_read_model()

    assert read_model["app_safe_core_boundary"] is True
    assert read_model["read_only_export_allowed"] is True
    assert read_model["intent_only_access"] is True
    assert read_model["canonical_core_access_allowed"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["core_action_execution_allowed"] is False
    assert read_model["shell_execution_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["proposal_only"] is True
    assert read_model["app_safe_only"] is True
