from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.memory_engine.self_readability.jarvis_memory_boundary_models import (
    JarvisMemorySelfReadBoundary,
    build_jarvis_memory_self_read_boundary,
)
from MAKSIMAR_CORE_LIB.memory_engine.self_readability.jarvis_memory_source_usage_models import (
    JarvisMemorySourceUsagePack,
    build_jarvis_memory_source_usage_pack,
)
from MAKSIMAR_CORE_LIB.memory_engine.self_readability.jarvis_memory_visibility_models import (
    JarvisMemoryVisibilityEntry,
    build_jarvis_memory_visibility_entry,
)


@dataclass(frozen=True, slots=True)
class JarvisMemorySelfReadModel:
    self_read_id: str
    visibility: JarvisMemoryVisibilityEntry
    boundary: JarvisMemorySelfReadBoundary
    source_usage: JarvisMemorySourceUsagePack
    evidence_pack: Tuple[str, ...]
    preview_trace: Tuple[str, ...]
    can_explain_where_searched: bool
    can_explain_sources_used: bool
    can_explain_constraints_applied: bool
    can_explain_evidence_pack: bool
    can_explain_preview_trace: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    self_read_ready: bool

    def __post_init__(self) -> None:
        if not self.self_read_id:
            raise ValueError("self_read_id must be non-empty")
        if not self.evidence_pack:
            raise ValueError("evidence_pack must be non-empty")
        if not self.preview_trace:
            raise ValueError("preview_trace must be non-empty")

        required_true = (
            "can_explain_where_searched",
            "can_explain_sources_used",
            "can_explain_constraints_applied",
            "can_explain_evidence_pack",
            "can_explain_preview_trace",
            "self_read_ready",
        )
        for field_name in required_true:
            if getattr(self, field_name) is not True:
                raise ValueError(f"{field_name} must be True")

        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")


def build_jarvis_memory_self_read_model() -> JarvisMemorySelfReadModel:
    visibility = build_jarvis_memory_visibility_entry()
    boundary = build_jarvis_memory_self_read_boundary()
    source_usage = build_jarvis_memory_source_usage_pack()

    return JarvisMemorySelfReadModel(
        self_read_id="jarvis_memory_self_read_001",
        visibility=visibility,
        boundary=boundary,
        source_usage=source_usage,
        evidence_pack=(
            "visibility::jarvis_memory_visibility_001",
            "boundary::jarvis_memory_self_read_boundary_001",
            "source_usage::jarvis_memory_source_usage_pack_001",
        ),
        preview_trace=(
            "query_scope_resolved",
            "visible_domains_selected",
            "denied_domains_applied",
            "sources_attributed",
            "evidence_pack_built",
            "preview_trace_returned",
        ),
        can_explain_where_searched=True,
        can_explain_sources_used=True,
        can_explain_constraints_applied=True,
        can_explain_evidence_pack=True,
        can_explain_preview_trace=True,
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        self_read_ready=True,
    )
