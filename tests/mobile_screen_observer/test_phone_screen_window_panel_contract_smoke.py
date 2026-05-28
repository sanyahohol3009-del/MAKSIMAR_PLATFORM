import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_window_panel_contract import (
    PhoneScreenWindowPanelContract,
)


def test_phone_screen_window_panel_contract_smoke() -> None:
    panel = PhoneScreenWindowPanelContract.default(panel_id="phone_screen_window_panel")
    payload = panel.to_dict()

    assert payload["panel_kind"] == "phone_screen_window"
    assert payload["dashboard_section"] == "Phone Window"
    assert payload["source_binding"] == "mobile_screen_observer"
    assert payload["read_model_binding"] == "PhoneScreenWindowReadModel"
    assert payload["read_only_default"] is True
    assert payload["can_show_frame_reference"] is True
    assert payload["can_show_consent_state"] is True
    assert payload["can_show_remote_assistance_intent"] is True
    assert payload["can_show_audit_state"] is True
    assert payload["dashboard_direct_execution_allowed"] is False
    assert payload["device_control_execution_allowed"] is False
    assert payload["child_control_allowed"] is False
    assert payload["family_children_surface_allowed"] is False


def test_phone_screen_window_panel_rejects_direct_execution() -> None:
    with pytest.raises(ValueError, match="dashboard_direct_execution_allowed must be False"):
        PhoneScreenWindowPanelContract(
            panel_id="phone_screen_window_panel",
            panel_kind="phone_screen_window",
            dashboard_section="Phone Window",
            source_binding="mobile_screen_observer",
            read_model_binding="PhoneScreenWindowReadModel",
            read_only_default=True,
            can_show_frame_reference=True,
            can_show_consent_state=True,
            can_show_remote_assistance_intent=True,
            can_show_audit_state=True,
            dashboard_direct_execution_allowed=True,
            device_control_execution_allowed=False,
            child_control_allowed=False,
            family_children_surface_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )
