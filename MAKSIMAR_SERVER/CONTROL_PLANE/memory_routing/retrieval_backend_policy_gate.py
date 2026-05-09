from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


RetrievalBackendCandidate = Literal[
    "mgrep",
    "sqlite_vec",
    "local_memory_registry",
    "history_ingestion",
    "storage_registry",
    "media_memory",
]


_BACKEND_ID_PATTERN = re.compile(r"^retrieval_backend_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True, slots=True)
class RetrievalBackendPolicyEntry:
    backend_id: str
    backend_candidate: RetrievalBackendCandidate
    backend_kind: str
    approved_for_phase_1_7: bool
    adapter_required: bool
    external_execution_required: bool
    policy_gate_required: bool
    reason: str

    def __post_init__(self) -> None:
        backend_id = _ensure_non_empty_str(self.backend_id, "backend_id")
        backend_kind = _ensure_non_empty_str(self.backend_kind, "backend_kind")
        reason = _ensure_non_empty_str(self.reason, "reason")

        if not _BACKEND_ID_PATTERN.fullmatch(backend_id):
            raise ValueError(f"Invalid backend_id: {backend_id}")

        for field_name in (
            "approved_for_phase_1_7",
            "adapter_required",
            "external_execution_required",
            "policy_gate_required",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.policy_gate_required:
            raise ValueError("policy_gate_required must be True")

        if self.backend_candidate in ("mgrep", "sqlite_vec"):
            if self.approved_for_phase_1_7:
                raise ValueError(f"{self.backend_candidate} must not be approved in PHASE 1.7")
            if not self.adapter_required:
                raise ValueError(f"{self.backend_candidate} requires adapter boundary")
            if not self.external_execution_required:
                raise ValueError(f"{self.backend_candidate} requires external execution boundary")

        object.__setattr__(self, "backend_id", backend_id)
        object.__setattr__(self, "backend_kind", backend_kind)
        object.__setattr__(self, "reason", reason)


@dataclass(frozen=True, slots=True)
class RetrievalBackendPolicyGate:
    total_backends: int
    approved_backends: int
    blocked_backends: int
    adapter_required_backends: int
    external_execution_backends: int
    mgrep_blocked: bool
    sqlite_vec_blocked: bool
    backend_execution_allowed: bool
    policy_gate_ready: bool
    entries: tuple[RetrievalBackendPolicyEntry, ...]

    def __post_init__(self) -> None:
        total_backends = _ensure_non_negative_int(self.total_backends, "total_backends")
        approved_backends = _ensure_non_negative_int(self.approved_backends, "approved_backends")
        blocked_backends = _ensure_non_negative_int(self.blocked_backends, "blocked_backends")
        adapter_required_backends = _ensure_non_negative_int(
            self.adapter_required_backends,
            "adapter_required_backends",
        )
        external_execution_backends = _ensure_non_negative_int(
            self.external_execution_backends,
            "external_execution_backends",
        )

        if total_backends != len(self.entries):
            raise ValueError("total_backends must match entries length")
        if total_backends <= 0:
            raise ValueError("total_backends must be >= 1")
        if approved_backends != sum(1 for entry in self.entries if entry.approved_for_phase_1_7):
            raise ValueError("approved_backends must match computed count")
        if blocked_backends != sum(1 for entry in self.entries if not entry.approved_for_phase_1_7):
            raise ValueError("blocked_backends must match computed count")
        if adapter_required_backends != sum(1 for entry in self.entries if entry.adapter_required):
            raise ValueError("adapter_required_backends must match computed count")
        if external_execution_backends != sum(1 for entry in self.entries if entry.external_execution_required):
            raise ValueError("external_execution_backends must match computed count")

        for field_name in (
            "mgrep_blocked",
            "sqlite_vec_blocked",
            "backend_execution_allowed",
            "policy_gate_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.mgrep_blocked:
            raise ValueError("mgrep_blocked must be True")
        if not self.sqlite_vec_blocked:
            raise ValueError("sqlite_vec_blocked must be True")
        if self.backend_execution_allowed:
            raise ValueError("backend_execution_allowed must be False in PHASE 1.7")
        if not self.policy_gate_ready:
            raise ValueError("policy_gate_ready must be True")

        object.__setattr__(self, "total_backends", total_backends)
        object.__setattr__(self, "approved_backends", approved_backends)
        object.__setattr__(self, "blocked_backends", blocked_backends)
        object.__setattr__(self, "adapter_required_backends", adapter_required_backends)
        object.__setattr__(self, "external_execution_backends", external_execution_backends)


def build_retrieval_backend_policy_gate() -> RetrievalBackendPolicyGate:
    entries = (
        RetrievalBackendPolicyEntry(
            backend_id="retrieval_backend_local_memory_registry",
            backend_candidate="local_memory_registry",
            backend_kind="accepted_internal_contract",
            approved_for_phase_1_7=True,
            adapter_required=False,
            external_execution_required=False,
            policy_gate_required=True,
            reason="Internal accepted registry contract is allowed as routing source.",
        ),
        RetrievalBackendPolicyEntry(
            backend_id="retrieval_backend_history_ingestion",
            backend_candidate="history_ingestion",
            backend_kind="accepted_internal_contract",
            approved_for_phase_1_7=True,
            adapter_required=False,
            external_execution_required=False,
            policy_gate_required=True,
            reason="Internal accepted history ingestion contract is allowed as routing source.",
        ),
        RetrievalBackendPolicyEntry(
            backend_id="retrieval_backend_storage_registry",
            backend_candidate="storage_registry",
            backend_kind="accepted_internal_contract",
            approved_for_phase_1_7=True,
            adapter_required=False,
            external_execution_required=False,
            policy_gate_required=True,
            reason="Internal accepted storage registry contract is allowed as routing source.",
        ),
        RetrievalBackendPolicyEntry(
            backend_id="retrieval_backend_media_memory",
            backend_candidate="media_memory",
            backend_kind="accepted_internal_contract",
            approved_for_phase_1_7=True,
            adapter_required=False,
            external_execution_required=False,
            policy_gate_required=True,
            reason="Internal accepted media memory contract is allowed as routing source.",
        ),
        RetrievalBackendPolicyEntry(
            backend_id="retrieval_backend_mgrep",
            backend_candidate="mgrep",
            backend_kind="future_experimental_backend",
            approved_for_phase_1_7=False,
            adapter_required=True,
            external_execution_required=True,
            policy_gate_required=True,
            reason="mgrep is future backend adapter only, not PHASE 1.7 core.",
        ),
        RetrievalBackendPolicyEntry(
            backend_id="retrieval_backend_sqlite_vec",
            backend_candidate="sqlite_vec",
            backend_kind="future_experimental_backend",
            approved_for_phase_1_7=False,
            adapter_required=True,
            external_execution_required=True,
            policy_gate_required=True,
            reason="sqlite-vec is future vector backend adapter only, not PHASE 1.7 core.",
        ),
    )

    mgrep_blocked = any(
        entry.backend_candidate == "mgrep" and not entry.approved_for_phase_1_7
        for entry in entries
    )
    sqlite_vec_blocked = any(
        entry.backend_candidate == "sqlite_vec" and not entry.approved_for_phase_1_7
        for entry in entries
    )

    return RetrievalBackendPolicyGate(
        total_backends=len(entries),
        approved_backends=sum(1 for entry in entries if entry.approved_for_phase_1_7),
        blocked_backends=sum(1 for entry in entries if not entry.approved_for_phase_1_7),
        adapter_required_backends=sum(1 for entry in entries if entry.adapter_required),
        external_execution_backends=sum(1 for entry in entries if entry.external_execution_required),
        mgrep_blocked=mgrep_blocked,
        sqlite_vec_blocked=sqlite_vec_blocked,
        backend_execution_allowed=False,
        policy_gate_ready=True,
        entries=entries,
    )
