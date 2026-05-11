from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.self_readability.jarvis_memory_self_read_model import (
    build_jarvis_memory_self_read_model,
)


def build_jarvis_memory_self_read_preview() -> Dict[str, object]:
    model = build_jarvis_memory_self_read_model()

    return {
        "self_read_id": model.self_read_id,
        "preview_ready": model.self_read_ready,
        "where_searched": model.visibility.visible_domains,
        "hidden_domains": model.visibility.hidden_domains,
        "sources_used": tuple(entry.source_ref for entry in model.source_usage.entries),
        "constraints_applied": model.boundary.policy_constraints,
        "evidence_pack": model.evidence_pack,
        "preview_trace": model.preview_trace,
        "can_explain_where_searched": model.can_explain_where_searched,
        "can_explain_sources_used": model.can_explain_sources_used,
        "can_explain_constraints_applied": model.can_explain_constraints_applied,
        "can_explain_evidence_pack": model.can_explain_evidence_pack,
        "can_explain_preview_trace": model.can_explain_preview_trace,
        "canonical_write_allowed": model.canonical_write_allowed,
        "runtime_mutation_allowed": model.runtime_mutation_allowed,
        "flow": (
            "memory_visibility",
            "memory_boundary",
            "source_usage_pack",
            "self_read_model",
            "self_read_preview",
        ),
    }
