from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_window_panel_contract import (
    PhoneScreenWindowPanelContract,
)
from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_window_read_model import (
    build_default_phone_screen_window_read_model,
)


def test_phone_screen_dashboard_read_only_default_smoke() -> None:
    panel = PhoneScreenWindowPanelContract.default(panel_id="phone_screen_window_panel")
    read_model = build_default_phone_screen_window_read_model(
        window_id="phone_screen_window_001",
        panel_id=panel.panel_id,
        device_id="ios_device_001",
        owner_identity_id="owner_001",
        platform="ios",
        frame_ref="artifact://mobile-screen/frame/latest",
    )

    assert panel.read_only_default is True
    assert panel.dashboard_direct_execution_allowed is False
    assert panel.device_control_execution_allowed is False
    assert panel.child_control_allowed is False
    assert read_model.read_only is True
    assert read_model.dashboard_control_allowed is False
    assert read_model.direct_execution_allowed is False
    assert read_model.child_control_surface is False
