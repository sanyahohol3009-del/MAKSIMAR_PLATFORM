from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_button_intent_contract import (
    PhoneScreenButtonIntentContract,
)
from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_window_panel_contract import (
    PhoneScreenWindowPanelContract,
)
from MAKSIMAR_CORE_LIB.mobile_screen_observer.phone_screen_window_read_model import (
    build_default_phone_screen_window_read_model,
)


def build_phone_screen_window_preview_payload() -> dict[str, object]:
    panel = PhoneScreenWindowPanelContract.default(panel_id="phone_screen_window_panel")
    read_model = build_default_phone_screen_window_read_model(
        window_id="phone_screen_window_001",
        panel_id=panel.panel_id,
        device_id="android_device_001",
        owner_identity_id="owner_001",
        platform="android",
        frame_ref="artifact://mobile-screen/frame/latest",
    )
    remote_assistance_intent = PhoneScreenButtonIntentContract.remote_assistance_request(
        intent_id="phone_screen_remote_assistance_request_001",
        panel_id=panel.panel_id,
        device_id="android_device_001",
        owner_identity_id="owner_001",
    )

    return {
        "preview_id": "phone_screen_window_preview_v1",
        "dashboard_section": "Phone Window",
        "read_only": True,
        "direct_execution_allowed": False,
        "child_control_surface": False,
        "family_children_surface": "Family / Children",
        "panel": panel.to_dict(),
        "read_model": read_model.to_dict(),
        "remote_assistance_intent": remote_assistance_intent.to_dict(),
    }


def main() -> None:
    print(json.dumps(build_phone_screen_window_preview_payload(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
