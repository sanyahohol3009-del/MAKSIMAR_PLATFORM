from __future__ import annotations

import json
from typing import Any

from MAKSIMAR_SERVER.AI_ORCHESTRATION.ai_orchestration_read_model_builder import (
    build_ai_orchestration_runtime_read_model,
)


def build_ai_orchestration_terminal_preview_payload() -> dict[str, Any]:
    read_model = build_ai_orchestration_runtime_read_model()

    return {
        "preview_id": "ai_orchestration_terminal_preview_v1",
        "surface": "terminal",
        "read_only": True,
        "dashboard_safe": True,
        "runtime_mutation_allowed": False,
        "deployment_allowed": False,
        "public_exposure_allowed": False,
        "runtime_read_model": read_model.to_dict(),
        "reason_codes": (
            "terminal_preview_read_only",
            "ai_orchestration_runtime_visible",
            "runtime_mutation_blocked",
        ),
    }


def render_ai_orchestration_terminal_preview() -> str:
    payload = build_ai_orchestration_terminal_preview_payload()
    runtime = payload["runtime_read_model"]

    lines = (
        "AI_ORCHESTRATION TERMINAL PREVIEW",
        f"read_model_id: {runtime['read_model_id']}",
        f"proposal_only: {runtime['proposal_only']}",
        f"runtime_mutation_allowed: {runtime['runtime_mutation_allowed']}",
        f"deployment_allowed: {runtime['deployment_allowed']}",
        f"public_exposure_allowed: {runtime['public_exposure_allowed']}",
        f"dashboard_safe: {runtime['dashboard_safe']}",
    )
    return "\n".join(lines)


def main() -> None:
    print(json.dumps(build_ai_orchestration_terminal_preview_payload(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
