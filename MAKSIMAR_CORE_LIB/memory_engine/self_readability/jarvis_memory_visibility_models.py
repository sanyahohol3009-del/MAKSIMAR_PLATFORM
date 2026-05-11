from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class JarvisMemoryVisibilityEntry:
    visibility_id: str
    query_scope: str
    visible_domains: Tuple[str, ...]
    hidden_domains: Tuple[str, ...]
    source_attribution_required: bool
    evidence_pack_required: bool
    preview_trace_required: bool
    visibility_ready: bool

    def __post_init__(self) -> None:
        if not self.visibility_id:
            raise ValueError("visibility_id must be non-empty")
        if not self.query_scope:
            raise ValueError("query_scope must be non-empty")
        if not self.visible_domains:
            raise ValueError("visible_domains must be non-empty")
        if not self.hidden_domains:
            raise ValueError("hidden_domains must be non-empty")
        if not self.source_attribution_required:
            raise ValueError("source_attribution_required must be True")
        if not self.evidence_pack_required:
            raise ValueError("evidence_pack_required must be True")
        if not self.preview_trace_required:
            raise ValueError("preview_trace_required must be True")
        if not self.visibility_ready:
            raise ValueError("visibility_ready must be True")


def build_jarvis_memory_visibility_entry() -> JarvisMemoryVisibilityEntry:
    return JarvisMemoryVisibilityEntry(
        visibility_id="jarvis_memory_visibility_001",
        query_scope="memory_self_readability",
        visible_domains=(
            "conversational_memory",
            "project_notes",
            "owner_context",
            "tenant_conversational_context",
            "project_artifact_memory",
        ),
        hidden_domains=(
            "secrets",
            "credentials",
            "runtime_state",
            "canonical_truth_write_paths",
        ),
        source_attribution_required=True,
        evidence_pack_required=True,
        preview_trace_required=True,
        visibility_ready=True,
    )
