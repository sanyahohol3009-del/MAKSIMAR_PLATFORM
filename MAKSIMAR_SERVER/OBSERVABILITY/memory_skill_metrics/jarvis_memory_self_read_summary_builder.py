from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.self_readability import (
    build_jarvis_memory_self_read_model,
    build_jarvis_memory_self_read_preview,
    validate_jarvis_memory_self_read_model,
)


def build_jarvis_memory_self_read_summary() -> Dict[str, object]:
    model = build_jarvis_memory_self_read_model()
    preview = build_jarvis_memory_self_read_preview()

    summary_ready = (
        validate_jarvis_memory_self_read_model(model)
        and preview["preview_ready"] is True
        and preview["canonical_write_allowed"] is False
        and preview["runtime_mutation_allowed"] is False
    )

    return {
        "summary_id": "jarvis_memory_self_read_summary_001",
        "summary_ready": summary_ready,
        "preview_ready": preview["preview_ready"],
        "can_explain_where_searched": preview["can_explain_where_searched"],
        "can_explain_sources_used": preview["can_explain_sources_used"],
        "can_explain_constraints_applied": preview["can_explain_constraints_applied"],
        "can_explain_evidence_pack": preview["can_explain_evidence_pack"],
        "can_explain_preview_trace": preview["can_explain_preview_trace"],
        "source_count": len(preview["sources_used"]),
        "constraint_count": len(preview["constraints_applied"]),
        "canonical_write_allowed": preview["canonical_write_allowed"],
        "runtime_mutation_allowed": preview["runtime_mutation_allowed"],
    }
