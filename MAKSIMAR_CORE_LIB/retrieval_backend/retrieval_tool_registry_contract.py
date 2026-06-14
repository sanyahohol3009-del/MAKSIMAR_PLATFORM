from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.retrieval_backend.retrieval_tool_contract import (
    RetrievalToolContract,
    build_retrieval_tool_contracts,
)


RETRIEVAL_TOOL_REGISTRY_ID = "retrieval_tool_registry_contract_v1"


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class RetrievalToolRegistryContract:
    registry_id: str
    tools: tuple[RetrievalToolContract, ...]
    read_only: bool = True
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    output_requires_normalization: bool = True
    source_of_truth: bool = False
    canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    direct_execution_allowed: bool = False
    network_allowed_by_default: bool = False
    readonly_router_registration_enabled: bool = True
    auto_routing_readonly_enabled: bool = True
    runtime_registration_enabled: bool = False
    auto_routing_runtime_enabled: bool = False

    def __post_init__(self) -> None:
        registry_id = _require_text(self.registry_id, "registry_id")
        if not isinstance(self.tools, tuple):
            raise TypeError("tools must be a tuple")
        if len(self.tools) != 3:
            raise ValueError("tools must include mgrep_readonly, sqlite_vec_readonly and qdrant_readonly")
        if not all(isinstance(tool, RetrievalToolContract) for tool in self.tools):
            raise TypeError("tools entries must be RetrievalToolContract")
        if tuple(tool.tool_kind for tool in self.tools) != ("mgrep_readonly", "sqlite_vec_readonly", "qdrant_readonly"):
            raise ValueError("tools must be ordered as mgrep_readonly, sqlite_vec_readonly, qdrant_readonly")

        for field_name in (
            "read_only",
            "source_ref_required",
            "evidence_binding_required",
            "output_requires_normalization",
            "source_of_truth",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "direct_execution_allowed",
            "network_allowed_by_default",
            "readonly_router_registration_enabled",
            "auto_routing_readonly_enabled",
            "runtime_registration_enabled",
            "auto_routing_runtime_enabled",
        ):
            _require_bool(getattr(self, field_name), field_name)
        for field_name in (
            "read_only",
            "source_ref_required",
            "evidence_binding_required",
            "output_requires_normalization",
            "readonly_router_registration_enabled",
            "auto_routing_readonly_enabled",
        ):
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} must be True")
        for field_name in (
            "source_of_truth",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "direct_execution_allowed",
            "network_allowed_by_default",
            "runtime_registration_enabled",
            "auto_routing_runtime_enabled",
        ):
            if getattr(self, field_name):
                raise ValueError(f"{field_name} must be False")
        if any(tool.runtime_enabled or tool.registered_with_jarvis_runtime for tool in self.tools):
            raise ValueError("tool runtime registration must remain disabled")
        if not all(tool.registered_with_jarvis_readonly_router for tool in self.tools):
            raise ValueError("all tools must be registered with the read-only router")

        object.__setattr__(self, "registry_id", registry_id)

    def to_read_model(self) -> dict[str, object]:
        return {
            "registry_id": self.registry_id,
            "read_only": self.read_only,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "output_requires_normalization": self.output_requires_normalization,
            "source_of_truth": self.source_of_truth,
            "canonical_write_allowed": self.canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "readonly_router_registration_enabled": self.readonly_router_registration_enabled,
            "auto_routing_readonly_enabled": self.auto_routing_readonly_enabled,
            "runtime_registration_enabled": self.runtime_registration_enabled,
            "auto_routing_runtime_enabled": self.auto_routing_runtime_enabled,
            "tools": tuple(tool.to_read_model() for tool in self.tools),
        }


def build_retrieval_tool_registry_contract() -> RetrievalToolRegistryContract:
    return RetrievalToolRegistryContract(
        registry_id=RETRIEVAL_TOOL_REGISTRY_ID,
        tools=build_retrieval_tool_contracts(),
    )


__all__ = [
    "RETRIEVAL_TOOL_REGISTRY_ID",
    "RetrievalToolRegistryContract",
    "build_retrieval_tool_registry_contract",
]
