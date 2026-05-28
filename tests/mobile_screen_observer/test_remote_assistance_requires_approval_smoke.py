from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_button_intent_contract import (
    PhoneScreenButtonIntentContract,
)
from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_window_read_model import (
    build_default_phone_screen_window_read_model,
)
from tools.phone_screen_window_preview import build_phone_screen_window_preview_payload


def test_remote_assistance_requires_approval_smoke() -> None:
    read_model = build_default_phone_screen_window_read_model(
        window_id="phone_screen_window_001",
        panel_id="phone_screen_window_panel",
        device_id="android_device_001",
        owner_identity_id="owner_001",
        platform="android",
        frame_ref="artifact://mobile-screen/frame/latest",
    )
    intent = PhoneScreenButtonIntentContract.remote_assistance_request(
        intent_id="phone_screen_remote_assistance_request_001",
        panel_id="phone_screen_window_panel",
        device_id="android_device_001",
        owner_identity_id="owner_001",
    )
    preview = build_phone_screen_window_preview_payload()

    assert read_model.remote_assistance_requires_approval is True
    assert intent.approval_required is True
    assert intent.remote_assistance_requires_approval is True
    assert intent.dashboard_direct_execution_allowed is False
    assert intent.device_control_execution_allowed is False
    assert preview["remote_assistance_intent"]["approval_required"] is True
    assert preview["remote_assistance_intent"]["device_control_execution_allowed"] is False
