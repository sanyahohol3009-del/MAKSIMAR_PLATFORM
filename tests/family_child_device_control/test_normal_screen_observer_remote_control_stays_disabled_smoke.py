import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_session_contract import (
    MobileScreenSessionContract,
)
from MAKSIMAR_CORE_LIB.mobile_screen_observer.remote_assistance_intent_contract import (
    RemoteAssistanceIntentContract,
)


def test_normal_screen_observer_remote_control_stays_disabled_smoke() -> None:
    session = MobileScreenSessionContract(
        session_id="screen_session_001",
        device_id="adult_device_001",
        owner_identity_id="owner_001",
        device_type="android",
        session_state="consent_required",
        consent_required=True,
        audit_required=True,
        read_only=True,
        frame_reference_only=True,
        direct_screen_capture_allowed=False,
        remote_control_allowed=False,
        touch_injection_allowed=False,
        keyboard_injection_allowed=False,
        external_network_access_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
        source_of_truth_override_allowed=False,
    )

    assert session.remote_control_allowed is False

    with pytest.raises(ValueError, match="device_control_execution_allowed must be False"):
        RemoteAssistanceIntentContract(
            intent_id="remote_assist_direct_bad",
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
