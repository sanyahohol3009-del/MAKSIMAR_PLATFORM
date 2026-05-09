from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict

from MAKSIMAR_CORE_LIB.evidence_memory import (
    build_evidence_memory_contract,
    build_evidence_memory_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.evidence_bound_memory_readiness_gate import (
    build_evidence_bound_memory_phase_readiness,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.evidence_source_chain_builder import (
    build_evidence_source_chain_contract,
)


_BINDING_ID_PATTERN = re.compile(r"^evidence_core_binding_[a-z][a-z0-9_]*$")
_EVIDENCE_ID_PATTERN = re.compile(r"^evidence_[a-z][a-z0-9_]*$")
_SOURCE_ID_PATTERN = re.compile(r"^retrieval_source_[a-z][a-z0-9_]*$")
_SOURCE_EVENT_ID_PATTERN = re.compile(r"^source_event_[a-z][a-z0-9_]*$")
_SOURCE_VERSION_ID_PATTERN = re.compile(r"^source_version_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class EvidenceMemoryCoreBindingEntry:
    binding_id: str
    evidence_id: str
    server_source_id: str
    core_source_event_id: str
    core_source_version_id: str
    artifact_ref: str
    server_chain_ready: bool
    core_evidence_ready: bool
    artifact_ref_match: bool
    citation_required: bool
    conflict_clear: bool
    memory_truth: bool
    knowledge_graph_projection_only: bool
    read_only: bool
    binding_ready: bool

    def __post_init__(self) -> None:
        binding_id = _ensure_non_empty_str(self.binding_id, "binding_id")
        evidence_id = _ensure_non_empty_str(self.evidence_id, "evidence_id")
        server_source_id = _ensure_non_empty_str(
            self.server_source_id,
            "server_source_id",
        )
        core_source_event_id = _ensure_non_empty_str(
            self.core_source_event_id,
            "core_source_event_id",
        )
        core_source_version_id = _ensure_non_empty_str(
            self.core_source_version_id,
            "core_source_version_id",
        )
        artifact_ref = _ensure_non_empty_str(self.artifact_ref, "artifact_ref")

        if not _BINDING_ID_PATTERN.fullmatch(binding_id):
            raise ValueError(f"Invalid binding_id: {binding_id}")
        if not _EVIDENCE_ID_PATTERN.fullmatch(evidence_id):
            raise ValueError(f"Invalid evidence_id: {evidence_id}")
        if not _SOURCE_ID_PATTERN.fullmatch(server_source_id):
            raise ValueError(f"Invalid server_source_id: {server_source_id}")
        if not _SOURCE_EVENT_ID_PATTERN.fullmatch(core_source_event_id):
            raise ValueError(f"Invalid core_source_event_id: {core_source_event_id}")
        if not _SOURCE_VERSION_ID_PATTERN.fullmatch(core_source_version_id):
            raise ValueError(
                f"Invalid core_source_version_id: {core_source_version_id}"
            )
        if not artifact_ref.startswith("artifact://"):
            raise ValueError("artifact_ref must start with artifact://")

        for field_name in (
            "server_chain_ready",
            "core_evidence_ready",
            "artifact_ref_match",
            "citation_required",
            "conflict_clear",
            "memory_truth",
            "knowledge_graph_projection_only",
            "read_only",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.server_chain_ready:
            raise ValueError("server_chain_ready must be True")
        if not self.core_evidence_ready:
            raise ValueError("core_evidence_ready must be True")
        if not self.artifact_ref_match:
            raise ValueError("artifact_ref_match must be True")
        if not self.citation_required:
            raise ValueError("citation_required must be True")
        if not self.conflict_clear:
            raise ValueError("conflict_clear must be True")
        if not self.memory_truth:
            raise ValueError("memory_truth must be True")
        if not self.knowledge_graph_projection_only:
            raise ValueError("knowledge_graph_projection_only must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "binding_id", binding_id)
        object.__setattr__(self, "evidence_id", evidence_id)
        object.__setattr__(self, "server_source_id", server_source_id)
        object.__setattr__(self, "core_source_event_id", core_source_event_id)
        object.__setattr__(self, "core_source_version_id", core_source_version_id)
        object.__setattr__(self, "artifact_ref", artifact_ref)


@dataclass(frozen=True, slots=True)
class EvidenceMemoryCoreBindingContract:
    total_bindings: int
    matched_evidence_items: int
    artifact_ref_matched_bindings: int
    citation_required_bindings: int
    conflict_clear_bindings: int
    memory_truth_bindings: int
    knowledge_graph_projection_bindings: int
    read_only_bindings: int
    ready_bindings: int
    server_phase_ready: bool
    core_preview_ready: bool
    mgrep_blocked: bool
    sqlite_vec_blocked: bool
    backend_execution_allowed: bool
    entries: tuple[EvidenceMemoryCoreBindingEntry, ...]

    def __post_init__(self) -> None:
        total_bindings = _ensure_non_negative_int(
            self.total_bindings,
            "total_bindings",
        )

        if total_bindings != len(self.entries):
            raise ValueError("total_bindings must match entries length")
        if total_bindings <= 0:
            raise ValueError("total_bindings must be >= 1")

        computed = {
            "matched_evidence_items": sum(1 for entry in self.entries if entry.evidence_id),
            "artifact_ref_matched_bindings": sum(
                1 for entry in self.entries if entry.artifact_ref_match
            ),
            "citation_required_bindings": sum(
                1 for entry in self.entries if entry.citation_required
            ),
            "conflict_clear_bindings": sum(
                1 for entry in self.entries if entry.conflict_clear
            ),
            "memory_truth_bindings": sum(
                1 for entry in self.entries if entry.memory_truth
            ),
            "knowledge_graph_projection_bindings": sum(
                1 for entry in self.entries if entry.knowledge_graph_projection_only
            ),
            "read_only_bindings": sum(1 for entry in self.entries if entry.read_only),
            "ready_bindings": sum(1 for entry in self.entries if entry.binding_ready),
        }

        for field_name, value in computed.items():
            if getattr(self, field_name) != value:
                raise ValueError(f"{field_name} must match computed count")

        for field_name in (
            "server_phase_ready",
            "core_preview_ready",
            "mgrep_blocked",
            "sqlite_vec_blocked",
            "backend_execution_allowed",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.matched_evidence_items != total_bindings:
            raise ValueError("all server evidence items must match CORE evidence")
        if self.artifact_ref_matched_bindings != total_bindings:
            raise ValueError("all artifact refs must match")
        if self.citation_required_bindings != total_bindings:
            raise ValueError("all bindings must require citation")
        if self.conflict_clear_bindings != total_bindings:
            raise ValueError("all bindings must be conflict-clear")
        if self.memory_truth_bindings != total_bindings:
            raise ValueError("all bindings must be memory truth")
        if self.knowledge_graph_projection_bindings != total_bindings:
            raise ValueError("all bindings must mark knowledge graph projection-only")
        if self.read_only_bindings != total_bindings:
            raise ValueError("all bindings must be read-only")
        if self.ready_bindings != total_bindings:
            raise ValueError("all bindings must be ready")
        if not self.server_phase_ready:
            raise ValueError("server_phase_ready must be True")
        if not self.core_preview_ready:
            raise ValueError("core_preview_ready must be True")
        if not self.mgrep_blocked:
            raise ValueError("mgrep_blocked must be True")
        if not self.sqlite_vec_blocked:
            raise ValueError("sqlite_vec_blocked must be True")
        if self.backend_execution_allowed:
            raise ValueError("backend_execution_allowed must be False")

        binding_ids = tuple(entry.binding_id for entry in self.entries)
        evidence_ids = tuple(entry.evidence_id for entry in self.entries)

        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("duplicate binding_id values detected")
        if len(set(evidence_ids)) != len(evidence_ids):
            raise ValueError("duplicate evidence_id values detected")


def _binding_id_from_evidence_id(evidence_id: str) -> str:
    suffix = evidence_id.removeprefix("evidence_").strip()
    if not suffix:
        raise ValueError("evidence_id must produce binding suffix")
    return f"evidence_core_binding_{suffix}"


def build_evidence_memory_core_binding_contract() -> EvidenceMemoryCoreBindingContract:
    core = build_evidence_memory_contract()
    core_preview = build_evidence_memory_preview()
    server_chain = build_evidence_source_chain_contract()
    server_readiness = build_evidence_bound_memory_phase_readiness()

    core_by_evidence_id = {record.evidence_id: record for record in core.records}

    entries = tuple(
        EvidenceMemoryCoreBindingEntry(
            binding_id=_binding_id_from_evidence_id(chain.evidence_id),
            evidence_id=chain.evidence_id,
            server_source_id=chain.source_id,
            core_source_event_id=core_by_evidence_id[chain.evidence_id].source_event_id,
            core_source_version_id=core_by_evidence_id[
                chain.evidence_id
            ].source_version_id,
            artifact_ref=chain.artifact_ref,
            server_chain_ready=chain.chain_ready,
            core_evidence_ready=core_by_evidence_id[chain.evidence_id].evidence_ready,
            artifact_ref_match=(
                chain.artifact_ref
                == core_by_evidence_id[chain.evidence_id].artifact_ref
            ),
            citation_required=(
                chain.citation_required
                and core_by_evidence_id[chain.evidence_id].citation_required
            ),
            conflict_clear=(
                not chain.conflict_marker
                and not core_by_evidence_id[chain.evidence_id].conflict_detected
            ),
            memory_truth=core_by_evidence_id[chain.evidence_id].memory_truth,
            knowledge_graph_projection_only=core_by_evidence_id[
                chain.evidence_id
            ].knowledge_graph_projection_only,
            read_only=core_by_evidence_id[chain.evidence_id].read_only,
            binding_ready=(
                chain.evidence_id in core_by_evidence_id
                and chain.chain_ready
                and core_by_evidence_id[chain.evidence_id].evidence_ready
                and chain.artifact_ref
                == core_by_evidence_id[chain.evidence_id].artifact_ref
                and chain.citation_required
                and core_by_evidence_id[chain.evidence_id].citation_required
                and not chain.conflict_marker
                and not core_by_evidence_id[chain.evidence_id].conflict_detected
                and core_by_evidence_id[chain.evidence_id].memory_truth
                and core_by_evidence_id[
                    chain.evidence_id
                ].knowledge_graph_projection_only
                and core_by_evidence_id[chain.evidence_id].read_only
            ),
        )
        for chain in server_chain.entries
    )

    return EvidenceMemoryCoreBindingContract(
        total_bindings=len(entries),
        matched_evidence_items=sum(1 for entry in entries if entry.evidence_id),
        artifact_ref_matched_bindings=sum(
            1 for entry in entries if entry.artifact_ref_match
        ),
        citation_required_bindings=sum(
            1 for entry in entries if entry.citation_required
        ),
        conflict_clear_bindings=sum(1 for entry in entries if entry.conflict_clear),
        memory_truth_bindings=sum(1 for entry in entries if entry.memory_truth),
        knowledge_graph_projection_bindings=sum(
            1 for entry in entries if entry.knowledge_graph_projection_only
        ),
        read_only_bindings=sum(1 for entry in entries if entry.read_only),
        ready_bindings=sum(1 for entry in entries if entry.binding_ready),
        server_phase_ready=server_readiness.phase_ready,
        core_preview_ready=bool(core_preview["phase_batch_ready"]),
        mgrep_blocked=server_readiness.mgrep_blocked,
        sqlite_vec_blocked=server_readiness.sqlite_vec_blocked,
        backend_execution_allowed=server_readiness.backend_execution_allowed,
        entries=entries,
    )


_EVIDENCE_MEMORY_CORE_BINDING_FLOW = (
    "core_evidence_memory",
    "server_evidence_source_chain",
    "evidence_id_match",
    "artifact_ref_match",
    "citation_gate",
    "conflict_clear_gate",
    "memory_truth_gate",
    "knowledge_graph_projection_gate",
    "read_only_gate",
    "backend_policy_gate",
    "core_server_binding_ready",
)


def build_evidence_memory_core_binding_preview() -> Dict[str, object]:
    contract = build_evidence_memory_core_binding_contract()

    return {
        "flow": _EVIDENCE_MEMORY_CORE_BINDING_FLOW,
        "total_bindings": contract.total_bindings,
        "matched_evidence_items": contract.matched_evidence_items,
        "artifact_ref_matched_bindings": contract.artifact_ref_matched_bindings,
        "citation_required_bindings": contract.citation_required_bindings,
        "conflict_clear_bindings": contract.conflict_clear_bindings,
        "memory_truth_bindings": contract.memory_truth_bindings,
        "knowledge_graph_projection_bindings": (
            contract.knowledge_graph_projection_bindings
        ),
        "read_only_bindings": contract.read_only_bindings,
        "ready_bindings": contract.ready_bindings,
        "server_phase_ready": contract.server_phase_ready,
        "core_preview_ready": contract.core_preview_ready,
        "mgrep_blocked": contract.mgrep_blocked,
        "sqlite_vec_blocked": contract.sqlite_vec_blocked,
        "backend_execution_allowed": contract.backend_execution_allowed,
        "evidence_ids": tuple(entry.evidence_id for entry in contract.entries),
        "preview_ready": True,
        "phase_batch_ready": True,
    }
