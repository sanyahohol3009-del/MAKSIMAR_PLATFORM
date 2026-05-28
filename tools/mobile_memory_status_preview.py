from __future__ import annotations

import json
from typing import Any

from MAKSIMAR_CORE_LIB.mobile_bridge.mobile_memory_status_read_model import MobileMemoryStatusReadModel


def _json_safe(payload: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(payload, sort_keys=True))


def build_mobile_memory_status_preview_payload() -> dict[str, Any]:
    model = MobileMemoryStatusReadModel.safe_default()
    payload = {
        "preview_id": "mobile_memory_status_preview_default",
        "preview_kind": "read_only_mobile_memory_status",
        "schema_version": "1.0",
        "data": model.to_read_model(),
    }
    return _json_safe(payload)


def render_mobile_memory_status_preview_text() -> str:
    payload = build_mobile_memory_status_preview_payload()
    return json.dumps(payload, sort_keys=True, indent=2)


def main() -> None:
    print(render_mobile_memory_status_preview_text())


if __name__ == "__main__":
    main()
