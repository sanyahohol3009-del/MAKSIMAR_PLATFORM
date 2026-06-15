from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.voice_perception.voice_perception_status_read_model import (
    build_voice_perception_status_read_model,
)


def _json_safe(payload: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(payload, sort_keys=True))


def build_voice_perception_status_preview_payload() -> dict[str, Any]:
    payload = {
        "preview_id": "voice_perception_status_preview_default",
        "preview_kind": "read_only_voice_perception_status",
        "schema_version": "1.0",
        "data": build_voice_perception_status_read_model().to_read_model(),
    }
    return _json_safe(payload)


def render_voice_perception_status_preview_text() -> str:
    payload = build_voice_perception_status_preview_payload()
    return json.dumps(payload, sort_keys=True, indent=2)


def main() -> None:
    print(render_voice_perception_status_preview_text())


if __name__ == "__main__":
    main()
