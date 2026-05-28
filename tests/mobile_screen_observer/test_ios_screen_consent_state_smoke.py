import pytest

from IOS_SHELL.screen_observer_client.ios_screen_consent_state import (
    IOSScreenConsentState,
)


def test_ios_screen_consent_state_smoke() -> None:
    state = IOSScreenConsentState(
        device_id="ios_device_001",
        owner_identity_id="owner_001",
        session_id="ios_screen_session_001",
        consent_state="consent_granted",
        consent_required=True,
        owner_visible=True,
        audit_required=True,
        permission_prompt_allowed=False,
        ios_platform_api_call_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
        source_of_truth_override_allowed=False,
    )

    read_model = state.to_read_model()

    assert state.is_granted() is True
    assert read_model["consent_granted"] is True
    assert read_model["owner_visible"] is True
    assert read_model["audit_required"] is True
    assert read_model["permission_prompt_allowed"] is False
    assert read_model["ios_platform_api_call_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["core_write_allowed"] is False
    assert read_model["source_of_truth_override_allowed"] is False


def test_ios_screen_consent_state_rejects_permission_prompt() -> None:
    with pytest.raises(ValueError, match="permission_prompt_allowed must be False"):
        IOSScreenConsentState(
            device_id="ios_device_001",
            owner_identity_id="owner_001",
            session_id="ios_screen_session_001",
            consent_state="consent_required",
            consent_required=True,
            owner_visible=True,
            audit_required=True,
            permission_prompt_allowed=True,
            ios_platform_api_call_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )


def test_ios_screen_consent_state_rejects_platform_api_call() -> None:
    with pytest.raises(ValueError, match="ios_platform_api_call_allowed must be False"):
        IOSScreenConsentState(
            device_id="ios_device_001",
            owner_identity_id="owner_001",
            session_id="ios_screen_session_001",
            consent_state="consent_required",
            consent_required=True,
            owner_visible=True,
            audit_required=True,
            permission_prompt_allowed=False,
            ios_platform_api_call_allowed=True,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )
