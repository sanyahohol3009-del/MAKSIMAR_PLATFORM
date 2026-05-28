from pathlib import Path

from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_button_intent_contract import (
    PhoneScreenButtonIntentContract,
)
from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_window_panel_contract import (
    PhoneScreenWindowPanelContract,
)
from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_window_read_model import (
    build_default_phone_screen_window_read_model,
)
from tools.phone_screen_window_preview import build_phone_screen_window_preview_payload
from tools.project_readiness_control.roadmap_expected_files_registry import get_expected_batch


_PHASE_4_BATCHES: tuple[str, ...] = ("4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7")


def test_phase4_acceptance_expected_files_exist_smoke() -> None:
    missing: list[str] = []

    for batch_id in _PHASE_4_BATCHES:
        batch = get_expected_batch(batch_id)
        for expected_file in batch.expected_files:
            if not Path(expected_file.path).exists():
                missing.append(f"{batch_id}: {expected_file.path}")

    assert missing == []


def test_phase4_acceptance_normal_and_family_paths_are_separated_smoke() -> None:
    normal_paths = [
        Path("ANDROID_SHELL/screen_observer_client/android_screen_observer_client.py"),
        Path("ANDROID_SHELL/screen_observer_client/android_screen_consent_state.py"),
        Path("ANDROID_SHELL/screen_observer_client/android_screen_stream_bridge.py"),
        Path("ANDROID_SHELL/screen_observer_client/android_remote_assistance_intent_bridge.py"),
        Path("IOS_SHELL/screen_observer_client/ios_screen_observer_client.py"),
        Path("IOS_SHELL/screen_observer_client/ios_screen_consent_state.py"),
        Path("IOS_SHELL/screen_observer_client/ios_screen_stream_bridge.py"),
        Path("IOS_SHELL/screen_observer_client/ios_remote_assistance_intent_bridge.py"),
    ]

    family_paths = [
        Path("ANDROID_SHELL/family_child_device/android_child_device_profile_bridge.py"),
        Path("ANDROID_SHELL/family_child_device/android_guardian_authority_bridge.py"),
        Path("ANDROID_SHELL/family_child_device/android_family_child_device_policy_binding.py"),
        Path("IOS_SHELL/family_child_device/ios_child_device_profile_bridge.py"),
        Path("IOS_SHELL/family_child_device/ios_guardian_authority_bridge.py"),
        Path("IOS_SHELL/family_child_device/ios_family_child_device_policy_binding.py"),
    ]

    for source_path in normal_paths:
        text = source_path.read_text(encoding="utf-8")
        assert "family_child_device_control" not in text
        assert "Family / Children" not in text

    for source_path in family_paths:
        text = source_path.read_text(encoding="utf-8")
        assert "family_child_device_control" in text or "Family / Children" in text


def test_phase4_acceptance_phone_window_is_read_only_smoke() -> None:
    panel = PhoneScreenWindowPanelContract.default(panel_id="phone_screen_window_panel")
    read_model = build_default_phone_screen_window_read_model(
        window_id="phone_screen_window_001",
        panel_id=panel.panel_id,
        device_id="android_device_001",
        owner_identity_id="owner_001",
        platform="android",
        frame_ref="artifact://mobile-screen/frame/latest",
    )

    assert panel.read_only_default is True
    assert panel.dashboard_direct_execution_allowed is False
    assert panel.device_control_execution_allowed is False
    assert panel.child_control_allowed is False
    assert panel.family_children_surface_allowed is False

    assert read_model.read_only is True
    assert read_model.dashboard_control_allowed is False
    assert read_model.direct_execution_allowed is False
    assert read_model.child_control_surface is False
    assert read_model.family_children_surface_required is True
    assert read_model.remote_assistance_requires_approval is True


def test_phase4_acceptance_remote_assistance_requires_approval_smoke() -> None:
    intent = PhoneScreenButtonIntentContract.remote_assistance_request(
        intent_id="phone_screen_remote_assistance_request_001",
        panel_id="phone_screen_window_panel",
        device_id="android_device_001",
        owner_identity_id="owner_001",
    )

    assert intent.approval_required is True
    assert intent.audit_required is True
    assert intent.read_only_intent is True
    assert intent.remote_assistance_requires_approval is True
    assert intent.dashboard_direct_execution_allowed is False
    assert intent.device_control_execution_allowed is False
    assert intent.child_control_intent_allowed is False
    assert intent.runtime_mutation_allowed is False
    assert intent.core_write_allowed is False
    assert intent.source_of_truth_override_allowed is False


def test_phase4_acceptance_preview_payload_is_safe_smoke() -> None:
    preview = build_phone_screen_window_preview_payload()

    assert preview["preview_id"] == "phone_screen_window_preview_v1"
    assert preview["dashboard_section"] == "Phone Window"
    assert preview["read_only"] is True
    assert preview["direct_execution_allowed"] is False
    assert preview["child_control_surface"] is False
    assert preview["family_children_surface"] == "Family / Children"

    panel = preview["panel"]
    read_model = preview["read_model"]
    remote_assistance_intent = preview["remote_assistance_intent"]

    assert panel["dashboard_direct_execution_allowed"] is False
    assert panel["device_control_execution_allowed"] is False
    assert panel["child_control_allowed"] is False

    assert read_model["frame_reference_only"] is True
    assert read_model["read_only"] is True
    assert read_model["dashboard_control_allowed"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["child_control_surface"] is False

    assert remote_assistance_intent["approval_required"] is True
    assert remote_assistance_intent["dashboard_direct_execution_allowed"] is False
    assert remote_assistance_intent["device_control_execution_allowed"] is False


def test_phase4_acceptance_no_dangerous_runtime_markers_smoke() -> None:
    source_dirs = [
        Path("ANDROID_SHELL/screen_observer_client"),
        Path("ANDROID_SHELL/family_child_device"),
        Path("IOS_SHELL/screen_observer_client"),
        Path("IOS_SHELL/family_child_device"),
        Path("MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME"),
        Path("MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME"),
        Path("MAKSIMAR_CORE_LIB/mobile_screen_observer"),
        Path("MAKSIMAR_CORE_LIB/family_child_device_control"),
    ]

    forbidden_markers = [
        "subprocess",
        "socket.",
        "requests.",
        "urllib.",
        "http.client",
        "adb ",
        "uiautomator",
        "input tap",
        "input text",
        "screencap",
        "screenrecord",
        "MediaProjection",
        "AccessibilityService",
        "ReplayKit",
        "RPScreenRecorder",
        "AXUIElement",
        "UIAccessibility",
        "start_recording",
        "start_capture",
        "take_screenshot",
        "capture_screenshot",
    ]

    for source_dir in source_dirs:
        for source_path in source_dir.glob("*.py"):
            text = source_path.read_text(encoding="utf-8")
            for marker in forbidden_markers:
                assert marker not in text, f"{marker} found in {source_path}"
