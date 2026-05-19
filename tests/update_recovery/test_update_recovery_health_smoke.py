from __future__ import annotations

from tests.update_recovery.test_update_recovery_read_model_builder_smoke import _runtime_read_model

from MAKSIMAR_SERVER.UPDATE_RECOVERY.update_recovery_health import (
    UPDATE_RECOVERY_HEALTH_READ_MODEL_ID,
    UpdateRecoveryHealthStatus,
    build_update_recovery_health_read_model,
)


def test_update_recovery_health_is_dashboard_safe_and_read_only() -> None:
    runtime_read_model = _runtime_read_model()
    health = build_update_recovery_health_read_model(runtime_read_model)

    assert health.read_model_id == UPDATE_RECOVERY_HEALTH_READ_MODEL_ID
    assert health.status is UpdateRecoveryHealthStatus.HEALTHY
    assert health.runtime_wrapper_only is True
    assert health.existing_transport_preserved is True
    assert health.existing_recovery_manager_preserved is True
    assert health.update_recovery_ready_for_next_gate is True
    assert health.runtime_apply_allowed is False
    assert health.canonical_write_allowed is False
    assert health.dashboard_execution_allowed is False
    assert health.dashboard_safe is True
