from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.retrieval_backend.retrieval_tool_result_contract import RetrievalToolKind


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
class RetrievalToolContract:
    tool_id: str
    tool_kind: RetrievalToolKind
    backend_kind: str
    policy_gate_ref: str
    source_ref: str
    read_only: bool = True
    auto_selection_allowed: bool = True
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    output_requires_normalization: bool = True
    source_of_truth: bool = False
    canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    direct_execution_allowed: bool = False
    network_allowed_by_default: bool = False
    approval_required_before_runtime: bool = True
    backend_runtime_enabled: bool = False
    runtime_enabled: bool = False
    registered_with_jarvis_readonly_router: bool = True
    registered_with_jarvis_runtime: bool = False

    def __post_init__(self) -> None:
        tool_id = _require_text(self.tool_id, "tool_id")
        tool_kind = _require_text(self.tool_kind, "tool_kind")
        backend_kind = _require_text(self.backend_kind, "backend_kind")
        policy_gate_ref = _require_text(self.policy_gate_ref, "policy_gate_ref")
        source_ref = _require_text(self.source_ref, "source_ref")
        if tool_kind not in RetrievalToolKind.__args__:
            raise ValueError(f"unsupported tool_kind: {tool_kind}")
        expected_backend = tool_kind.removesuffix("_readonly")
        if expected_backend == "sqlite_vec":
            expected_backend = "sqlite_vec"
        if backend_kind != expected_backend:
            raise ValueError("backend_kind must match tool_kind")

        for field_name in (
            "read_only",
            "auto_selection_allowed",
            "source_ref_required",
            "evidence_binding_required",
            "output_requires_normalization",
            "source_of_truth",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "direct_execution_allowed",
            "network_allowed_by_default",
            "approval_required_before_runtime",
            "backend_runtime_enabled",
            "runtime_enabled",
            "registered_with_jarvis_readonly_router",
            "registered_with_jarvis_runtime",
        ):
            _require_bool(getattr(self, field_name), field_name)

        for field_name in (
            "read_only",
            "auto_selection_allowed",
            "source_ref_required",
            "evidence_binding_required",
            "output_requires_normalization",
            "approval_required_before_runtime",
            "registered_with_jarvis_readonly_router",
        ):
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} must be True")
        for field_name in (
            "source_of_truth",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "direct_execution_allowed",
            "network_allowed_by_default",
            "backend_runtime_enabled",
            "runtime_enabled",
            "registered_with_jarvis_runtime",
        ):
            if getattr(self, field_name):
                raise ValueError(f"{field_name} must be False")

        object.__setattr__(self, "tool_id", tool_id)
        object.__setattr__(self, "tool_kind", tool_kind)
        object.__setattr__(self, "backend_kind", backend_kind)
        object.__setattr__(self, "policy_gate_ref", policy_gate_ref)
        object.__setattr__(self, "source_ref", source_ref)

    def to_read_model(self) -> dict[str, object]:
        return {
            "tool_id": self.tool_id,
            "tool_kind": self.tool_kind,
            "backend_kind": self.backend_kind,
            "policy_gate_ref": self.policy_gate_ref,
            "source_ref": self.source_ref,
            "read_only": self.read_only,
            "auto_selection_allowed": self.auto_selection_allowed,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "output_requires_normalization": self.output_requires_normalization,
            "source_of_truth": self.source_of_truth,
            "canonical_write_allowed": self.canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "approval_required_before_runtime": self.approval_required_before_runtime,
            "backend_runtime_enabled": self.backend_runtime_enabled,
            "runtime_enabled": self.runtime_enabled,
            "registered_with_jarvis_readonly_router": self.registered_with_jarvis_readonly_router,
            "registered_with_jarvis_runtime": self.registered_with_jarvis_runtime,
        }


def build_retrieval_tool_contracts() -> tuple[RetrievalToolContract, ...]:
    policy_ref = "MAKSIMAR_CORE_LIB/retrieval_backend/retrieval_tool_enablement_policy.py"
    return (
        RetrievalToolContract(
            tool_id="retrieval_tool_mgrep_readonly",
            tool_kind="mgrep_readonly",
            backend_kind="mgrep",
            policy_gate_ref=policy_ref,
            source_ref="MAKSIMAR_CORE_LIB/retrieval_backend/mgrep_adapter_contract.py",
        ),
        RetrievalToolContract(
            tool_id="retrieval_tool_sqlite_vec_readonly",
            tool_kind="sqlite_vec_readonly",
            backend_kind="sqlite_vec",
            policy_gate_ref=policy_ref,
            source_ref="MAKSIMAR_CORE_LIB/retrieval_backend/sqlite_vec_adapter_contract.py",
        ),
        RetrievalToolContract(
            tool_id="retrieval_tool_qdrant_readonly",
            tool_kind="qdrant_readonly",
            backend_kind="qdrant",
            policy_gate_ref=policy_ref,
            source_ref="MAKSIMAR_CORE_LIB/retrieval_backend/qdrant_adapter_contract.py",
        ),
    )


__all__ = [
    "RetrievalToolContract",
    "build_retrieval_tool_contracts",
]
