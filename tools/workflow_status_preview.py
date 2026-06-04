from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_status_bridge import (
    build_workflow_dashboard_read_only_projection,
    build_workflow_status_bridge_read_model,
)


def build_workflow_status_preview_payload() -> dict[str, object]:
    read_model = build_workflow_status_bridge_read_model()
    return {
        "preview_id": "phase6.workflow.status.preview.v1",
        "preview_read_only": True,
        "dashboard_read_only": True,
        "runtime_execution_allowed": False,
        "direct_core_write_allowed": False,
        "direct_server_canonical_write_allowed": False,
        "network_socket_tunnel_allowed": False,
        "workflow_status": read_model.to_read_model(),
        "dashboard_projection": build_workflow_dashboard_read_only_projection(),
    }


def main() -> None:
    print(json.dumps(build_workflow_status_preview_payload(), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
