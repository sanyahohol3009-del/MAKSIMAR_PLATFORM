from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class JarvisMemorySelfReadBoundary:
    boundary_id: str
    allowed_read_domains: Tuple[str, ...]
    denied_domains: Tuple[str, ...]
    policy_constraints: Tuple[str, ...]
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    auto_promotion_allowed: bool
    auto_conflict_resolution_allowed: bool
    secrets_access_allowed: bool
    boundary_ready: bool

    def __post_init__(self) -> None:
        if not self.boundary_id:
            raise ValueError("boundary_id must be non-empty")
        if not self.allowed_read_domains:
            raise ValueError("allowed_read_domains must be non-empty")
        if not self.denied_domains:
            raise ValueError("denied_domains must be non-empty")
        if not self.policy_constraints:
            raise ValueError("policy_constraints must be non-empty")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.auto_promotion_allowed:
            raise ValueError("auto_promotion_allowed must be False")
        if self.auto_conflict_resolution_allowed:
            raise ValueError("auto_conflict_resolution_allowed must be False")
        if self.secrets_access_allowed:
            raise ValueError("secrets_access_allowed must be False")
        if not self.boundary_ready:
            raise ValueError("boundary_ready must be True")


def build_jarvis_memory_self_read_boundary() -> JarvisMemorySelfReadBoundary:
    return JarvisMemorySelfReadBoundary(
        boundary_id="jarvis_memory_self_read_boundary_001",
        allowed_read_domains=(
            "conversational_memory",
            "project_notes",
            "owner_context",
            "tenant_conversational_context",
            "project_artifact_memory",
            "memory_drift_candidates",
        ),
        denied_domains=(
            "secrets",
            "credentials",
            "runtime_state",
            "canonical_write_paths",
            "approval_private_payloads",
        ),
        policy_constraints=(
            "source_attribution_required",
            "evidence_pack_required",
            "preview_trace_required",
            "no_canonical_write",
            "no_runtime_mutation",
            "no_auto_truth_resolution",
        ),
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        auto_promotion_allowed=False,
        auto_conflict_resolution_allowed=False,
        secrets_access_allowed=False,
        boundary_ready=True,
    )
