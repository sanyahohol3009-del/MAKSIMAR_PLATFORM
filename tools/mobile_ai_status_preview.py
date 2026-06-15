from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ANDROID_SHELL.local_ai_runtime.android_model_runtime_status import (
    build_android_model_runtime_status,
)
from IOS_SHELL.local_ai_runtime.ios_model_runtime_status import (
    build_ios_model_runtime_status,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.mobile_capability_summary_builder import (
    build_mobile_ai_status_read_model,
    build_mobile_capability_summary,
)


def _json_safe(payload: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(payload, sort_keys=True))


def build_mobile_ai_status_preview_payload() -> dict[str, Any]:
    status_read_model = build_mobile_ai_status_read_model().to_read_model()
    capability_summary = build_mobile_capability_summary()
    payload = {
        "preview_id": "mobile_ai_status_preview_default",
        "preview_kind": "read_only_mobile_ai_status",
        "schema_version": "1.0",
        "phase_id": "PHASE_9",
        "mobile_junior_status": status_read_model,
        "app_safe_core_mirror_status": {
            "app_safe_core_mirror_read_only": status_read_model[
                "app_safe_core_mirror_read_only"
            ],
            "feedback_is_proposal_only": status_read_model["feedback_is_proposal_only"],
            "junior_sync_authority": status_read_model["junior_sync_authority"],
        },
        "local_ai_runtime_bridge_status": {
            "android": build_android_model_runtime_status().to_read_model(),
            "ios": build_ios_model_runtime_status().to_read_model(),
        },
        "data": {
            "phase_id": "PHASE_9",
            **status_read_model,
            "server_remains_canonical_core": capability_summary[
                "server_remains_canonical_core"
            ],
            "mobile_junior_is_subordinate": capability_summary[
                "sync_is_server_senior_to_mobile_junior_only"
            ],
            "network_sync_start_allowed": capability_summary[
                "network_sync_start_allowed"
            ],
            "deployment_allowed": capability_summary["deployment_allowed"],
            "shell_execution_allowed": capability_summary["shell_execution_allowed"],
            "canonical_write_allowed": capability_summary["canonical_write_allowed"],
            "pc_control_allowed": capability_summary["pc_control_allowed"],
        },
    }
    return _json_safe(payload)


def render_mobile_ai_status_preview_text() -> str:
    payload = build_mobile_ai_status_preview_payload()
    return json.dumps(payload, sort_keys=True, indent=2)


def main() -> None:
    print(render_mobile_ai_status_preview_text())


if __name__ == "__main__":
    main()
