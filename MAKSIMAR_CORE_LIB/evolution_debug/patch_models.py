from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PatchCandidate:
    """One structured patch candidate derived from debug hypothesis."""

    patch_id: str
    hypothesis_id: str
    patch_scope: str
    sandbox_only: bool
    core_write_allowed: bool


@dataclass(frozen=True, slots=True)
class PatchCandidateContract:
    """Unified patch candidate contract for evolution debug layer."""

    total_candidates: int
    candidates: tuple[PatchCandidate, ...]
    auto_deploy_allowed: bool
