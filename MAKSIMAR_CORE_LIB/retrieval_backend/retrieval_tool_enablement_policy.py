from __future__ import annotations

"""Typed retrieval policy applied after Semantic Spine capability selection."""

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.retrieval_backend.retrieval_vendor_gate_contract import (
    RetrievalVendorGateContract,
    build_retrieval_vendor_gate_contract,
)


RETRIEVAL_TOOL_ENABLEMENT_POLICY_ID = "retrieval_tool_enablement_policy_v2"


@dataclass(frozen=True, slots=True)
class RetrievalToolEnablementPolicy:
    policy_id: str
    vendor_gate: RetrievalVendorGateContract
    read_only_tool_contracts_allowed: bool = True
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    output_requires_normalization: bool = True
    backend_runtime_enabled: bool = False
    runtime_tool_execution_enabled: bool = False
    canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    direct_execution_allowed: bool = False
    network_allowed_by_default: bool = False

    def __post_init__(self) -> None:
        if self.policy_id != RETRIEVAL_TOOL_ENABLEMENT_POLICY_ID:
            raise ValueError("policy_id must match canonical typed retrieval policy")
        if not isinstance(self.vendor_gate, RetrievalVendorGateContract):
            raise TypeError("vendor_gate must be RetrievalVendorGateContract")
        for field_name in (
            "read_only_tool_contracts_allowed", "source_ref_required",
            "evidence_binding_required", "output_requires_normalization",
        ):
            if getattr(self, field_name) is not True:
                raise ValueError(f"{field_name} must be True")
        for field_name in (
            "backend_runtime_enabled", "runtime_tool_execution_enabled",
            "canonical_write_allowed", "runtime_mutation_allowed",
            "direct_execution_allowed", "network_allowed_by_default",
        ):
            if getattr(self, field_name) is not False:
                raise ValueError(f"{field_name} must be False")
        if self.vendor_gate.runtime_enabled:
            raise ValueError("vendor gate runtime must remain disabled")

    def to_read_model(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "truth_owner": "canonical_semantic_spine",
            "selection_input": "typed_plan_step",
            "semantic_selection_performed": False,
            "read_only_tool_contracts_allowed": self.read_only_tool_contracts_allowed,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "output_requires_normalization": self.output_requires_normalization,
            "backend_runtime_enabled": self.backend_runtime_enabled,
            "runtime_tool_execution_enabled": self.runtime_tool_execution_enabled,
            "canonical_write_allowed": self.canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "vendor_gate": self.vendor_gate.to_read_model(),
        }


def build_retrieval_tool_enablement_policy() -> RetrievalToolEnablementPolicy:
    return RetrievalToolEnablementPolicy(
        policy_id=RETRIEVAL_TOOL_ENABLEMENT_POLICY_ID,
        vendor_gate=build_retrieval_vendor_gate_contract(),
    )


__all__ = [
    "RETRIEVAL_TOOL_ENABLEMENT_POLICY_ID",
    "RetrievalToolEnablementPolicy",
    "build_retrieval_tool_enablement_policy",
]
