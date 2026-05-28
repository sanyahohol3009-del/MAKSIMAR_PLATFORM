import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_window_read_model import (
    PhoneScreenWindowReadModel,
    build_default_phone_screen_window_read_model,
)


def test_phone_screen_window_read_model_smoke() -> None:
    read_model = build_default_phone_screen_window_read_model(
        window_id="phone_screen_window_001",
        panel_id="phone_screen_window_panel",
        device_id="android_device_001",
        owner_identity_id="owner_001",
        platform="android",
        frame_ref="artifact://mobile-screen/frame/latest",
    )

    payload = read_model.to_dict()

    assert payload["dashboard_section"] == "Phone Window"
    assert payload["platform"] == "android"
    assert payload["frame_reference_only"] is True
    assert payload["read_only"] is True
    assert payload["remote_assistance_requires_approval"] is True
    assert payload["dashboard_control_allowed"] is False
    assert payload["direct_execution_allowed"] is False
    assert payload["child_control_surface"] is False
    assert payload["family_children_surface_required"] is True
    assert payload["audit_visible"] is True
    assert payload["runtime_mutation_allowed"] is False
    assert payload["core_write_allowed"] is False
    assert payload["source_of_truth_override_allowed"] is False


def test_phone_screen_window_rejects_child_control_surface() -> None:
    with pytest.raises(ValueError, match="child_control_surface must be False"):
        PhoneScreenWindowReadModel(
            window_id="phone_screen_window_001",
            panel_id="phone_screen_window_panel",
            device_id="android_device_001",
            owner_identity_id="owner_001",
            platform="android",
            dashboard_section="Phone Window",
            observer_state="observing_metadata",
            consent_state="consent_granted",
            frame_ref="artifact://mobile-screen/frame/latest",
            frame_reference_only=True,
            read_only=True,
            remote_assistance_state="approval_required",
            remote_assistance_requires_approval=True,
            dashboard_control_allowed=False,
            direct_execution_allowed=False,
            child_control_surface=True,
            family_children_surface_required=True,
            audit_visible=True,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )
