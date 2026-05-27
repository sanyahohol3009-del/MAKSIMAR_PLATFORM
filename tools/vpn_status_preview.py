from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.vpn_dashboard_read_model_builder import (
    build_vpn_dashboard_read_model,
)


def build_vpn_status_preview_payload() -> dict[str, Any]:
    read_model = build_vpn_dashboard_read_model()
    payload = read_model.to_dict()
    payload["preview_id"] = "phase_2_vpn_status_preview"
    payload["preview_mode"] = "read_only"
    payload["operator_message"] = (
        "VPN runtime is policy-gated. Dashboard controls are disabled until "
        "control-plane handoff and approval gates are implemented."
    )
    return payload


def main() -> None:
    print(json.dumps(build_vpn_status_preview_payload(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
