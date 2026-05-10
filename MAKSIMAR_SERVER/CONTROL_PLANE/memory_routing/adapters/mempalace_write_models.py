from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_capability_builder import (
    MemPalaceDomain,
    build_mempalace_capability_contract,
)

_WRITE_ID_PATTERN = re.compile(r"^mempalace_write_request_[a-z][a-z0-9_]*_[0-9]{3}$")


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


@dataclass(frozen=True, slots=True)
class MemPalaceWriteRequestEntry:
    write_request_id: str
    domain: MemPalaceDomain
    adapter_id: str
    write_request_allowed: bool
    approval_required: bool
    approval_granted: bool
    sandbox_stage_required: bool
    diff_preview_required: bool
    risk_summary_required: bool
    canonical_write_allowed: bool
    auto_promotion_allowed: bool
    runtime_mutation_allowed: bool
    write_request_ready: bool
    description: str

    def __post_init__(self) -> None:
        write_request_id = _ensure_non_empty_str(self.write_request_id, "write_request_id")
        if not _WRITE_ID_PATTERN.fullmatch(write_request_id):
            raise ValueError(f"Invalid write_request_id: {write_request_id}")

        for field_name in ("adapter_id", "description"):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "write_request_allowed",
            "approval_required",
            "approval_granted",
            "sandbox_stage_required",
            "diff_preview_required",
            "risk_summary_required",
            "canonical_write_allowed",
            "auto_promotion_allowed",
            "runtime_mutation_allowed",
            "write_request_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.write_request_allowed and not self.approval_required:
            raise ValueError("approval_required must be True for allowed write requests")
        if self.write_request_allowed and not self.sandbox_stage_required:
            raise ValueError("sandbox_stage_required must be True for allowed write requests")
        if self.write_request_allowed and not self.diff_preview_required:
            raise ValueError("diff_preview_required must be True for allowed write requests")
        if self.write_request_allowed and not self.risk_summary_required:
            raise ValueError("risk_summary_required must be True for allowed write requests")
        if self.approval_granted:
            raise ValueError("approval_granted must be False in Batch 1")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.auto_promotion_allowed:
            raise ValueError("auto_promotion_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.write_request_ready:
            raise ValueError("write_request_ready must be True")


@dataclass(frozen=True, slots=True)
class MemPalaceWriteRequestContract:
    total_write_requests: int
    ready_write_requests: int
    allowed_write_requests: int
    approval_required_write_requests: int
    approval_granted_write_requests: int
    sandbox_stage_required_write_requests: int
    diff_preview_required_write_requests: int
    risk_summary_required_write_requests: int
    canonical_write_allowed_write_requests: int
    auto_promotion_allowed_write_requests: int
    runtime_mutation_allowed_write_requests: int
    entries: tuple[MemPalaceWriteRequestEntry, ...]

    def __post_init__(self) -> None:
        if self.total_write_requests != len(self.entries):
            raise ValueError("total_write_requests must match entries length")
        if self.total_write_requests != 4:
            raise ValueError("MemPalace write request contract must contain exactly 4 entries")

        expected = {
            "ready_write_requests": sum(1 for entry in self.entries if entry.write_request_ready),
            "allowed_write_requests": sum(1 for entry in self.entries if entry.write_request_allowed),
            "approval_required_write_requests": sum(1 for entry in self.entries if entry.approval_required),
            "approval_granted_write_requests": sum(1 for entry in self.entries if entry.approval_granted),
            "sandbox_stage_required_write_requests": sum(1 for entry in self.entries if entry.sandbox_stage_required),
            "diff_preview_required_write_requests": sum(1 for entry in self.entries if entry.diff_preview_required),
            "risk_summary_required_write_requests": sum(1 for entry in self.entries if entry.risk_summary_required),
            "canonical_write_allowed_write_requests": sum(1 for entry in self.entries if entry.canonical_write_allowed),
            "auto_promotion_allowed_write_requests": sum(1 for entry in self.entries if entry.auto_promotion_allowed),
            "runtime_mutation_allowed_write_requests": sum(1 for entry in self.entries if entry.runtime_mutation_allowed),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_write_requests != self.total_write_requests:
            raise ValueError("all MemPalace write request entries must be ready")
        if self.approval_granted_write_requests != 0:
            raise ValueError("MemPalace write approval must be false by default")
        if self.canonical_write_allowed_write_requests != 0:
            raise ValueError("MemPalace canonical write must remain blocked")
        if self.auto_promotion_allowed_write_requests != 0:
            raise ValueError("MemPalace auto-promotion must remain blocked")
        if self.runtime_mutation_allowed_write_requests != 0:
            raise ValueError("MemPalace runtime mutation must remain blocked")


def build_mempalace_write_request_contract() -> MemPalaceWriteRequestContract:
    capabilities = build_mempalace_capability_contract()

    entries = tuple(
        MemPalaceWriteRequestEntry(
            write_request_id=f"mempalace_write_request_{capability.domain}_001",
            domain=capability.domain,
            adapter_id="mempalace_adapter_memory_routing_001",
            write_request_allowed=capability.write_request_allowed,
            approval_required=capability.write_request_allowed,
            approval_granted=False,
            sandbox_stage_required=capability.write_request_allowed,
            diff_preview_required=capability.write_request_allowed,
            risk_summary_required=capability.write_request_allowed,
            canonical_write_allowed=False,
            auto_promotion_allowed=False,
            runtime_mutation_allowed=False,
            write_request_ready=True,
            description=f"Governed MemPalace write request contract for {capability.domain}.",
        )
        for capability in capabilities.entries
    )

    return MemPalaceWriteRequestContract(
        total_write_requests=len(entries),
        ready_write_requests=sum(1 for entry in entries if entry.write_request_ready),
        allowed_write_requests=sum(1 for entry in entries if entry.write_request_allowed),
        approval_required_write_requests=sum(1 for entry in entries if entry.approval_required),
        approval_granted_write_requests=sum(1 for entry in entries if entry.approval_granted),
        sandbox_stage_required_write_requests=sum(1 for entry in entries if entry.sandbox_stage_required),
        diff_preview_required_write_requests=sum(1 for entry in entries if entry.diff_preview_required),
        risk_summary_required_write_requests=sum(1 for entry in entries if entry.risk_summary_required),
        canonical_write_allowed_write_requests=sum(1 for entry in entries if entry.canonical_write_allowed),
        auto_promotion_allowed_write_requests=sum(1 for entry in entries if entry.auto_promotion_allowed),
        runtime_mutation_allowed_write_requests=sum(1 for entry in entries if entry.runtime_mutation_allowed),
        entries=entries,
    )
