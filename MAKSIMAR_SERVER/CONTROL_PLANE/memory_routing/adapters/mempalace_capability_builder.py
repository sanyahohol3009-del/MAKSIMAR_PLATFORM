from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_adapter_models import (
    build_mempalace_adapter_contract,
)

MemPalaceDomain = Literal[
    "conversational_memory",
    "project_notes",
    "owner_context",
    "tenant_conversational_context",
]


@dataclass(frozen=True, slots=True)
class MemPalaceCapabilityEntry:
    domain: MemPalaceDomain
    retrieval_allowed: bool
    write_request_allowed: bool
    canonical_truth_allowed: bool
    regulatory_memory_allowed: bool
    enterprise_policy_memory_allowed: bool
    technical_truth_allowed: bool
    audit_truth_allowed: bool
    approval_truth_allowed: bool
    auto_promotion_allowed: bool
    auto_conflict_resolution_allowed: bool
    runtime_mutation_allowed: bool
    capability_ready: bool

    def __post_init__(self) -> None:
        for field_name in (
            "retrieval_allowed",
            "write_request_allowed",
            "canonical_truth_allowed",
            "regulatory_memory_allowed",
            "enterprise_policy_memory_allowed",
            "technical_truth_allowed",
            "audit_truth_allowed",
            "approval_truth_allowed",
            "auto_promotion_allowed",
            "auto_conflict_resolution_allowed",
            "runtime_mutation_allowed",
            "capability_ready",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, bool):
                raise ValueError(f"{field_name} must be bool")

        if not self.retrieval_allowed:
            raise ValueError("retrieval_allowed must be True for allowed MemPalace domains")
        if self.canonical_truth_allowed:
            raise ValueError("canonical_truth_allowed must be False")
        if self.regulatory_memory_allowed:
            raise ValueError("regulatory_memory_allowed must be False")
        if self.enterprise_policy_memory_allowed:
            raise ValueError("enterprise_policy_memory_allowed must be False")
        if self.technical_truth_allowed:
            raise ValueError("technical_truth_allowed must be False")
        if self.audit_truth_allowed:
            raise ValueError("audit_truth_allowed must be False")
        if self.approval_truth_allowed:
            raise ValueError("approval_truth_allowed must be False")
        if self.auto_promotion_allowed:
            raise ValueError("auto_promotion_allowed must be False")
        if self.auto_conflict_resolution_allowed:
            raise ValueError("auto_conflict_resolution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.capability_ready:
            raise ValueError("capability_ready must be True")


@dataclass(frozen=True, slots=True)
class MemPalaceCapabilityContract:
    total_capabilities: int
    ready_capabilities: int
    retrieval_allowed_capabilities: int
    write_request_allowed_capabilities: int
    canonical_truth_allowed_capabilities: int
    regulatory_memory_allowed_capabilities: int
    enterprise_policy_memory_allowed_capabilities: int
    technical_truth_allowed_capabilities: int
    audit_truth_allowed_capabilities: int
    approval_truth_allowed_capabilities: int
    auto_promotion_allowed_capabilities: int
    auto_conflict_resolution_allowed_capabilities: int
    runtime_mutation_allowed_capabilities: int
    entries: tuple[MemPalaceCapabilityEntry, ...]

    def __post_init__(self) -> None:
        if self.total_capabilities != len(self.entries):
            raise ValueError("total_capabilities must match entries length")
        if self.total_capabilities != 4:
            raise ValueError("MemPalace capability contract must contain exactly 4 allowed domains")

        expected = {
            "ready_capabilities": sum(1 for entry in self.entries if entry.capability_ready),
            "retrieval_allowed_capabilities": sum(1 for entry in self.entries if entry.retrieval_allowed),
            "write_request_allowed_capabilities": sum(1 for entry in self.entries if entry.write_request_allowed),
            "canonical_truth_allowed_capabilities": sum(1 for entry in self.entries if entry.canonical_truth_allowed),
            "regulatory_memory_allowed_capabilities": sum(1 for entry in self.entries if entry.regulatory_memory_allowed),
            "enterprise_policy_memory_allowed_capabilities": sum(1 for entry in self.entries if entry.enterprise_policy_memory_allowed),
            "technical_truth_allowed_capabilities": sum(1 for entry in self.entries if entry.technical_truth_allowed),
            "audit_truth_allowed_capabilities": sum(1 for entry in self.entries if entry.audit_truth_allowed),
            "approval_truth_allowed_capabilities": sum(1 for entry in self.entries if entry.approval_truth_allowed),
            "auto_promotion_allowed_capabilities": sum(1 for entry in self.entries if entry.auto_promotion_allowed),
            "auto_conflict_resolution_allowed_capabilities": sum(1 for entry in self.entries if entry.auto_conflict_resolution_allowed),
            "runtime_mutation_allowed_capabilities": sum(1 for entry in self.entries if entry.runtime_mutation_allowed),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if build_mempalace_adapter_contract().source_of_truth_adapters != 0:
            raise ValueError("MemPalace adapter must not be source of truth")
        if self.ready_capabilities != self.total_capabilities:
            raise ValueError("all MemPalace capabilities must be ready")
        if self.retrieval_allowed_capabilities != self.total_capabilities:
            raise ValueError("all allowed MemPalace domains must allow retrieval")
        if self.canonical_truth_allowed_capabilities != 0:
            raise ValueError("MemPalace canonical truth capability must remain blocked")
        if self.regulatory_memory_allowed_capabilities != 0:
            raise ValueError("MemPalace regulatory memory capability must remain blocked")
        if self.enterprise_policy_memory_allowed_capabilities != 0:
            raise ValueError("MemPalace enterprise policy capability must remain blocked")
        if self.technical_truth_allowed_capabilities != 0:
            raise ValueError("MemPalace technical truth capability must remain blocked")
        if self.audit_truth_allowed_capabilities != 0:
            raise ValueError("MemPalace audit truth capability must remain blocked")
        if self.approval_truth_allowed_capabilities != 0:
            raise ValueError("MemPalace approval truth capability must remain blocked")
        if self.auto_promotion_allowed_capabilities != 0:
            raise ValueError("MemPalace auto-promotion must remain blocked")
        if self.auto_conflict_resolution_allowed_capabilities != 0:
            raise ValueError("MemPalace auto-conflict-resolution must remain blocked")
        if self.runtime_mutation_allowed_capabilities != 0:
            raise ValueError("MemPalace runtime mutation must remain blocked")


def build_mempalace_capability_contract() -> MemPalaceCapabilityContract:
    entries = tuple(
        MemPalaceCapabilityEntry(
            domain=domain,
            retrieval_allowed=True,
            write_request_allowed=domain in {"conversational_memory", "project_notes", "owner_context"},
            canonical_truth_allowed=False,
            regulatory_memory_allowed=False,
            enterprise_policy_memory_allowed=False,
            technical_truth_allowed=False,
            audit_truth_allowed=False,
            approval_truth_allowed=False,
            auto_promotion_allowed=False,
            auto_conflict_resolution_allowed=False,
            runtime_mutation_allowed=False,
            capability_ready=True,
        )
        for domain in (
            "conversational_memory",
            "project_notes",
            "owner_context",
            "tenant_conversational_context",
        )
    )

    return MemPalaceCapabilityContract(
        total_capabilities=len(entries),
        ready_capabilities=sum(1 for entry in entries if entry.capability_ready),
        retrieval_allowed_capabilities=sum(1 for entry in entries if entry.retrieval_allowed),
        write_request_allowed_capabilities=sum(1 for entry in entries if entry.write_request_allowed),
        canonical_truth_allowed_capabilities=sum(1 for entry in entries if entry.canonical_truth_allowed),
        regulatory_memory_allowed_capabilities=sum(1 for entry in entries if entry.regulatory_memory_allowed),
        enterprise_policy_memory_allowed_capabilities=sum(1 for entry in entries if entry.enterprise_policy_memory_allowed),
        technical_truth_allowed_capabilities=sum(1 for entry in entries if entry.technical_truth_allowed),
        audit_truth_allowed_capabilities=sum(1 for entry in entries if entry.audit_truth_allowed),
        approval_truth_allowed_capabilities=sum(1 for entry in entries if entry.approval_truth_allowed),
        auto_promotion_allowed_capabilities=sum(1 for entry in entries if entry.auto_promotion_allowed),
        auto_conflict_resolution_allowed_capabilities=sum(1 for entry in entries if entry.auto_conflict_resolution_allowed),
        runtime_mutation_allowed_capabilities=sum(1 for entry in entries if entry.runtime_mutation_allowed),
        entries=entries,
    )
