import pytest

from IOS_SHELL.screen_observer_client.ios_remote_assistance_intent_bridge import (
    IOSRemoteAssistanceIntentBridge,
)
from MAKSIMAR_CORE_LIB.mobile_screen_observer.remote_assistance_intent_contract import (
    RemoteAssistanceIntentContract,
)


def test_ios_remote_assistance_intent_bridge_smoke() -> None:
    bridge = IOSRemoteAssistanceIntentBridge.default(
        device_id="ios_device_001",
        session_id="ios_screen_session_001",
        owner_identity_id="owner_001",
    )

    intent = bridge.build_intent_contract(intent_id="ios_remote_assist_001")
    read_model = bridge.to_read_model()

    assert isinstance(intent, RemoteAssistanceIntentContract)
    assert intent.intent_id == "ios_remote_assist_001"
    assert intent.session_id == "ios_screen_session_001"
    assert intent.owner_approval_required is True
    assert intent.consent_required is True
    assert intent.audit_required is True
    assert intent.disabled_by_default is True
    assert intent.dashboard_direct_execute_allowed is False
    assert intent.device_control_execution_allowed is False
    assert intent.runtime_mutation_allowed is False
    assert intent.core_write_allowed is False

    assert read_model["bridge"] == "remote_assistance_intent"
    assert read_model["ios_platform_api_call_allowed"] is False
    assert read_model["replaykit_allowed"] is False
    assert read_model["accessibility_api_allowed"] is False
    assert read_model["touch_execution_allowed"] is False
    assert read_model["keyboard_execution_allowed"] is False
    assert read_model["child_control_enabled"] is False


def test_ios_remote_assistance_intent_bridge_rejects_device_control() -> None:
    with pytest.raises(ValueError, match="device_control_execution_allowed must be False"):
        IOSRemoteAssistanceIntentBridge(
            device_id="ios_device_001",
            session_id="ios_screen_session_001",
            owner_identity_id="owner_001",
            owner_approval_required=True,
            consent_required=True,
            audit_required=True,
            disabled_by_default=True,
            dashboard_direct_execute_allowed=False,
            device_control_execution_allowed=True,
            ios_platform_api_call_allowed=False,
            replaykit_allowed=False,
            accessibility_api_allowed=False,
            touch_execution_allowed=False,
            keyboard_execution_allowed=False,
            child_control_enabled=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )


def test_ios_remote_assistance_intent_bridge_rejects_child_control() -> None:
    with pytest.raises(ValueError, match="normal iOS remote assistance cannot enable child control"):
        IOSRemoteAssistanceIntentBridge(
            device_id="ios_device_001",
            session_id="ios_screen_session_001",
            owner_identity_id="owner_001",
            owner_approval_required=True,
            consent_required=True,
            audit_required=True,
            disabled_by_default=True,
            dashboard_direct_execute_allowed=False,
            device_control_execution_allowed=False,
            ios_platform_api_call_allowed=False,
            replaykit_allowed=False,
            accessibility_api_allowed=False,
            touch_execution_allowed=False,
            keyboard_execution_allowed=False,
            child_control_enabled=True,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
