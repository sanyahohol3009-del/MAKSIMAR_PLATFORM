import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.screen_stream_audit_contract import (
    ScreenStreamAuditContract,
)


def test_screen_stream_audit_contract_smoke() -> None:
    event = ScreenStreamAuditContract(
        audit_event_id="screen_audit_001",
        session_id="screen_session_001",
        action="remote_assistance_requested",
        actor_id="owner_001",
        device_id="android_device_001",
        event_epoch_ms=1000,
        append_only=True,
        visible_to_owner=True,
        contains_pixel_payload=False,
        contains_secret=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    assert event.append_only is True
    assert event.visible_to_owner is True


def test_screen_stream_audit_rejects_pixel_payload() -> None:
    with pytest.raises(ValueError, match="contains_pixel_payload must be False"):
        ScreenStreamAuditContract(
            audit_event_id="screen_audit_bad",
            session_id="screen_session_001",
            action="frame_reference_seen",
            actor_id="owner_001",
            device_id="android_device_001",
            event_epoch_ms=1000,
            append_only=True,
            visible_to_owner=True,
            contains_pixel_payload=True,
            contains_secret=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
