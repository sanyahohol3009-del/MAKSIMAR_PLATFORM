from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE.build_test_bridge_read_model import (
    build_polyglot_model_worker_read_model,
)
from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE.model_worker_bridge_models import (
    build_model_worker_bridge_preview,
)


def build_polyglot_model_worker_preview() -> Dict[str, object]:
    read_model = build_polyglot_model_worker_read_model()
    model_worker = build_model_worker_bridge_preview()

    preview_path = (
        "artifact_language_models",
        "language_bridge_models",
        "model_worker_bridge_models",
        "build_test_bridge_read_model",
        "productization_next_only",
    )

    preview_ready = (
        read_model["read_model_ready"] is True
        and model_worker["preview_ready"] is True
        and read_model["productization_allowed_now"] is False
        and read_model["productization_allowed_next"] is True
    )

    return {
        "preview_id": "polyglot_model_worker_preview_phase_6_7_001",
        "preview_ready": preview_ready,
        "preview_path": preview_path,
        "read_model": read_model,
        "model_worker": model_worker,
        "artifact_language_models_ready": read_model["artifact_language_models_ready"],
        "language_bridge_models_ready": read_model["language_bridge_models_ready"],
        "model_worker_bridge_models_ready": read_model["model_worker_bridge_models_ready"],
        "build_test_bridge_required": read_model["build_test_bridge_required"],
        "human_review_required": read_model["human_review_required"],
        "direct_model_mutation_allowed": read_model["direct_model_mutation_allowed"],
        "runtime_mutation_allowed": read_model["runtime_mutation_allowed"],
        "deployment_allowed": read_model["deployment_allowed"],
        "productization_allowed_now": read_model["productization_allowed_now"],
        "productization_allowed_next": read_model["productization_allowed_next"],
    }
