import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_session_contract import (
    MobileScreenSessionContract,
)


def test_mobile_screen_session_contract_smoke() -> None:
    session = MobileScreenSessionContract(
        session_id="screen_session_001",
        device_id="android_device_001",
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

    assert session.read_only is True
    assert session.frame_reference_only is True
    assert session.remote_control_allowed is False


def test_mobile_screen_session_rejects_direct_capture() -> None:
    with pytest.raises(ValueError, match="direct_screen_capture_allowed must be False"):
        MobileScreenSessionContract(
            session_id="screen_session_bad",
            device_id="android_device_001",
            owner_identity_id="owner_001",
            device_type="android",
            session_state="consent_required",
            consent_required=True,
            audit_required=True,
            read_only=True,
            frame_reference_only=True,
            direct_screen_capture_allowed=True,
            remote_control_allowed=False,
            touch_injection_allowed=False,
            keyboard_injection_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )


def test_mobile_screen_session_rejects_remote_control() -> None:
    with pytest.raises(ValueError, match="remote_control_allowed must be False"):
        MobileScreenSessionContract(
            session_id="screen_session_remote_bad",
            device_id="ios_device_001",
            owner_identity_id="owner_001",
            device_type="ios",
            session_state="consent_required",
            consent_required=True,
            audit_required=True,
            read_only=True,
            frame_reference_only=True,
            direct_screen_capture_allowed=False,
            remote_control_allowed=True,
            touch_injection_allowed=False,
            keyboard_injection_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )
