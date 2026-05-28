import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_button_intent_contract import (
    PhoneScreenButtonIntentContract,
)


def test_phone_screen_button_intent_contract_smoke() -> None:
    intent = PhoneScreenButtonIntentContract.remote_assistance_request(
        intent_id="phone_screen_remote_assistance_request_001",
        panel_id="phone_screen_window_panel",
        device_id="android_device_001",
        owner_identity_id="owner_001",
    )

    payload = intent.to_dict()

    assert payload["button_id"] == "request_remote_assistance"
    assert payload["intent_type"] == "remote_assistance_request"
    assert payload["approval_required"] is True
    assert payload["audit_required"] is True
    assert payload["read_only_intent"] is True
    assert payload["dashboard_direct_execution_allowed"] is False
    assert payload["device_control_execution_allowed"] is False
    assert payload["remote_assistance_requires_approval"] is True
    assert payload["child_control_intent_allowed"] is False


def test_phone_screen_button_intent_rejects_device_execution() -> None:
    with pytest.raises(ValueError, match="device_control_execution_allowed must be False"):
        PhoneScreenButtonIntentContract(
            intent_id="phone_screen_remote_assistance_request_001",
            panel_id="phone_screen_window_panel",
            device_id="android_device_001",
            owner_identity_id="owner_001",
            button_id="request_remote_assistance",
            intent_type="remote_assistance_request",
            approval_required=True,
            audit_required=True,
            read_only_intent=True,
            dashboard_direct_execution_allowed=False,
            device_control_execution_allowed=True,
            remote_assistance_requires_approval=True,
            child_control_intent_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )
