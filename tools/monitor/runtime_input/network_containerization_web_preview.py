from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.monitor.runtime_input.network_containerization_terminal_preview import (
    build_network_containerization_preview_read_model,
)


def build_network_containerization_web_preview_payload(
    project_root: Path | None = None,
) -> dict[str, Any]:
    read_model = build_network_containerization_preview_read_model(project_root)
    return {
        "preview_id": "network_containerization_web_preview_v1",
        "kind": "network_containerization_preview",
        "read_model": read_model.to_dict(),
        "rendering": {
            "dashboard_safe": True,
            "read_only": True,
            "blocked_edges_visible": bool(read_model.blocked_edges),
            "missing_contracts_visible": True,
            "deployment_action_available": False,
        },
    }


def render_network_containerization_web_preview_json(
    project_root: Path | None = None,
) -> str:
    return json.dumps(
        build_network_containerization_web_preview_payload(project_root),
        indent=2,
        sort_keys=True,
    )


def main() -> int:
    print(render_network_containerization_web_preview_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
