import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_session_contract import (
    MobileScreenSessionContract,
)
from MAKSIMAR_SERVER.MOBILE_SCREEN_OBSERVER_RUNTIME.mobile_screen_observer_session_registry import (
    MobileScreenObserverSessionRegistry,
)


def _session(remote_control_allowed: bool = False) -> MobileScreenSessionContract:
    return MobileScreenSessionContract(
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
        remote_control_allowed=remote_control_allowed,
        touch_injection_allowed=False,
        keyboard_injection_allowed=False,
        external_network_access_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
        source_of_truth_override_allowed=False,
    )


def test_screen_observer_session_registry_smoke() -> None:
    registry = MobileScreenObserverSessionRegistry()
    record = registry.register(_session())

    assert record.session.session_id == "screen_session_001"
    assert registry.contains("screen_session_001") is True
    assert registry.list_session_ids() == ("screen_session_001",)
    assert registry.to_read_model()["child_control_enabled"] is False


def test_screen_observer_session_registry_rejects_duplicate() -> None:
    registry = MobileScreenObserverSessionRegistry()
    registry.register(_session())

    with pytest.raises(ValueError, match="session already registered"):
        registry.register(_session())
