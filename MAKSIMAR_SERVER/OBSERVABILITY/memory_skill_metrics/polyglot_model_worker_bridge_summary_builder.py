from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE.polyglot_bridge_preview_builder import (
    build_polyglot_model_worker_preview,
)


def build_polyglot_model_worker_bridge_summary() -> Dict[str, object]:
    preview = build_polyglot_model_worker_preview()

    return {
        "summary_id": "polyglot_model_worker_bridge_summary_phase_6_7_001",
        "summary_ready": preview["preview_ready"],
        "roadmap_family": "memory_roadmap_v5_1",
        "phase_id": "PHASE 6.7",
        "track_scope": "polyglot_model_worker_bridge",
        "artifact_language_models_ready": preview["artifact_language_models_ready"],
        "language_bridge_models_ready": preview["language_bridge_models_ready"],
        "model_worker_bridge_models_ready": preview["model_worker_bridge_models_ready"],
        "build_test_bridge_required": preview["build_test_bridge_required"],
        "human_review_required": preview["human_review_required"],
        "direct_model_mutation_allowed": preview["direct_model_mutation_allowed"],
        "runtime_mutation_allowed": preview["runtime_mutation_allowed"],
        "deployment_allowed": preview["deployment_allowed"],
        "productization_allowed_now": preview["productization_allowed_now"],
        "productization_allowed_next": preview["productization_allowed_next"],
    }
