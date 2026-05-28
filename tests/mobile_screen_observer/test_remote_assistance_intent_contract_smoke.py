import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.remote_assistance_intent_contract import (
    RemoteAssistanceIntentContract,
)


def test_remote_assistance_intent_contract_smoke() -> None:
    intent = RemoteAssistanceIntentContract(
        intent_id="remote_assist_intent_001",
        session_id="screen_session_001",
        intent_state="approval_required",
        owner_approval_required=True,
        consent_required=True,
        audit_required=True,
        disabled_by_default=True,
        dashboard_direct_execute_allowed=False,
        device_control_execution_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    assert intent.requires_manual_approval() is True


def test_remote_assistance_rejects_direct_device_execution() -> None:
    with pytest.raises(ValueError, match="device_control_execution_allowed must be False"):
        RemoteAssistanceIntentContract(
            intent_id="remote_assist_intent_bad",
            session_id="screen_session_001",
            intent_state="approval_required",
            owner_approval_required=True,
            consent_required=True,
            audit_required=True,
            disabled_by_default=True,
            dashboard_direct_execute_allowed=False,
            device_control_execution_allowed=True,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
