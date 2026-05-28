import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_policy_contract import (
    MobileScreenPolicyContract,
)


def test_mobile_screen_policy_contract_smoke() -> None:
    policy = MobileScreenPolicyContract(
        policy_id="normal_screen_policy_001",
        observer_mode="normal_observer",
        read_only_required=True,
        consent_required=True,
        audit_required=True,
        remote_assistance_disabled_by_default=True,
        direct_screen_capture_allowed=False,
        screenshot_allowed=False,
        screen_recording_allowed=False,
        touch_injection_allowed=False,
        keyboard_injection_allowed=False,
        app_control_allowed=False,
        screen_time_enforcement_allowed=False,
        external_network_access_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    assert policy.permits_normal_observer_remote_control() is False


def test_mobile_screen_policy_rejects_screenshot_for_normal_observer() -> None:
    with pytest.raises(ValueError, match="normal observer forbids enabled capabilities"):
        MobileScreenPolicyContract(
            policy_id="normal_screen_policy_bad",
            observer_mode="normal_observer",
            read_only_required=True,
            consent_required=True,
            audit_required=True,
            remote_assistance_disabled_by_default=True,
            direct_screen_capture_allowed=False,
            screenshot_allowed=True,
            screen_recording_allowed=False,
            touch_injection_allowed=False,
            keyboard_injection_allowed=False,
            app_control_allowed=False,
            screen_time_enforcement_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
