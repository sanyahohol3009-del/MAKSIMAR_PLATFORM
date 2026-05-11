from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class JarvisMemorySourceUsageEntry:
    source_usage_id: str
    source_ref: str
    source_domain: str
    used_for: str
    attribution_required: bool
    evidence_required: bool
    source_usage_ready: bool

    def __post_init__(self) -> None:
        if not self.source_usage_id:
            raise ValueError("source_usage_id must be non-empty")
        if not self.source_ref:
            raise ValueError("source_ref must be non-empty")
        if not self.source_domain:
            raise ValueError("source_domain must be non-empty")
        if not self.used_for:
            raise ValueError("used_for must be non-empty")
        if not self.attribution_required:
            raise ValueError("attribution_required must be True")
        if not self.evidence_required:
            raise ValueError("evidence_required must be True")
        if not self.source_usage_ready:
            raise ValueError("source_usage_ready must be True")


@dataclass(frozen=True, slots=True)
class JarvisMemorySourceUsagePack:
    pack_id: str
    entries: Tuple[JarvisMemorySourceUsageEntry, ...]
    total_sources: int
    source_attribution_required: bool
    evidence_pack_required: bool
    source_usage_pack_ready: bool

    def __post_init__(self) -> None:
        if not self.pack_id:
            raise ValueError("pack_id must be non-empty")
        if self.total_sources != len(self.entries):
            raise ValueError("total_sources mismatch")
        if not self.entries:
            raise ValueError("entries must be non-empty")
        if not self.source_attribution_required:
            raise ValueError("source_attribution_required must be True")
        if not self.evidence_pack_required:
            raise ValueError("evidence_pack_required must be True")
        if not self.source_usage_pack_ready:
            raise ValueError("source_usage_pack_ready must be True")


def build_jarvis_memory_source_usage_pack() -> JarvisMemorySourceUsagePack:
    entries = (
        JarvisMemorySourceUsageEntry(
            source_usage_id="jarvis_memory_source_usage_001",
            source_ref="memory::project_notes::roadmap_v5",
            source_domain="project_notes",
            used_for="roadmap_reconciliation",
            attribution_required=True,
            evidence_required=True,
            source_usage_ready=True,
        ),
        JarvisMemorySourceUsageEntry(
            source_usage_id="jarvis_memory_source_usage_002",
            source_ref="memory::mempalace::read_only_routing",
            source_domain="conversational_memory",
            used_for="subordinate_read_only_memory_lookup",
            attribution_required=True,
            evidence_required=True,
            source_usage_ready=True,
        ),
        JarvisMemorySourceUsageEntry(
            source_usage_id="jarvis_memory_source_usage_003",
            source_ref="memory::drift_detection::candidate_report",
            source_domain="memory_drift_candidates",
            used_for="contradiction_candidate_visibility",
            attribution_required=True,
            evidence_required=True,
            source_usage_ready=True,
        ),
    )

    return JarvisMemorySourceUsagePack(
        pack_id="jarvis_memory_source_usage_pack_001",
        entries=entries,
        total_sources=len(entries),
        source_attribution_required=True,
        evidence_pack_required=True,
        source_usage_pack_ready=True,
    )
