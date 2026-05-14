from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE.artifact_language_models import (
    build_artifact_language_contract,
)
from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE.language_bridge_models import (
    build_language_bridge_contract,
)
from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE.model_worker_bridge_models import (
    build_model_worker_bridge_preview,
)


def build_polyglot_model_worker_read_model() -> Dict[str, object]:
    artifact_language = build_artifact_language_contract()
    language_bridge = build_language_bridge_contract()
    model_worker = build_model_worker_bridge_preview()

    read_model_ready = (
        artifact_language.artifact_language_models_ready
        and language_bridge.language_bridge_models_ready
        and model_worker["preview_ready"] is True
        and model_worker["productization_allowed_now"] is False
    )

    return {
        "read_model_id": "polyglot_model_worker_read_model_phase_6_7_001",
        "read_model_ready": read_model_ready,
        "roadmap_family": "memory_roadmap_v5_1",
        "phase_id": "PHASE 6.7",
        "track_scope": "polyglot_model_worker_bridge",
        "artifact_language_models_ready": artifact_language.artifact_language_models_ready,
        "artifact_language_count": len(artifact_language.entries),
        "language_bridge_models_ready": language_bridge.language_bridge_models_ready,
        "language_bridge_count": len(language_bridge.bridges),
        "model_worker_bridge_models_ready": model_worker["preview_ready"],
        "model_worker_bridge_count": model_worker["bridge_count"],
        "build_test_bridge_required": model_worker["build_test_bridge_required"],
        "human_review_required": model_worker["human_review_required"],
        "direct_model_mutation_allowed": model_worker["direct_model_mutation_allowed"],
        "runtime_mutation_allowed": model_worker["runtime_mutation_allowed"],
        "deployment_allowed": model_worker["deployment_allowed"],
        "productization_allowed_now": model_worker["productization_allowed_now"],
        "productization_allowed_next": model_worker["productization_allowed_next"],
    }
