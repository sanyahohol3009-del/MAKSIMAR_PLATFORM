from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.self_readability.jarvis_memory_self_read_model import (
    JarvisMemorySelfReadModel,
)


def validate_jarvis_memory_self_read_model(model: JarvisMemorySelfReadModel) -> bool:
    if not model.self_read_ready:
        return False
    if model.canonical_write_allowed:
        return False
    if model.runtime_mutation_allowed:
        return False
    if not model.visibility.visibility_ready:
        return False
    if not model.boundary.boundary_ready:
        return False
    if not model.source_usage.source_usage_pack_ready:
        return False

    return (
        model.can_explain_where_searched
        and model.can_explain_sources_used
        and model.can_explain_constraints_applied
        and model.can_explain_evidence_pack
        and model.can_explain_preview_trace
    )
