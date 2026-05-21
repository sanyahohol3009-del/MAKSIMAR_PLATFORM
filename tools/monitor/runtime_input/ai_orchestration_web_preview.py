from __future__ import annotations

import json
from typing import Any

from MAKSIMAR_SERVER.AI_ORCHESTRATION.ai_orchestration_read_model_builder import (
    build_ai_orchestration_runtime_read_model,
)


def build_ai_orchestration_web_preview_payload() -> dict[str, Any]:
    read_model = build_ai_orchestration_runtime_read_model()

    return {
        "preview_id": "ai_orchestration_web_preview_v1",
        "surface": "web",
        "read_only": True,
        "dashboard_safe": True,
        "runtime_mutation_allowed": False,
        "deployment_allowed": False,
        "public_exposure_allowed": False,
        "web_server_started": False,
        "runtime_read_model": read_model.to_dict(),
        "reason_codes": (
            "web_preview_payload_only",
            "no_web_server_started",
            "runtime_mutation_blocked",
        ),
    }


def main() -> None:
    print(json.dumps(build_ai_orchestration_web_preview_payload(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
