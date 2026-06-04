from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


ALLOWED_WORKFLOW_EDGE_KINDS: Tuple[str, ...] = (
    "main",
    "conditional",
    "error",
    "approval",
    "audit",
    "handoff",
)

ALLOWED_N8N_CONNECTION_TYPES: Tuple[str, ...] = (
    "main",
    "ai_tool",
    "error",
    "trigger",
    "metadata",
    "approval",
)


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_allowed(value: str, field_name: str, allowed_values: Tuple[str, ...]) -> str:
    normalized = _require_non_empty_text(value, field_name)
    if normalized not in allowed_values:
        raise ValueError(f"{field_name} must be one of {allowed_values}")
    return normalized


@dataclass(frozen=True)
class WorkflowEdgeContract:
    edge_id: str
    source_node_id: str
    target_node_id: str
    source_handle: str = "main"
    target_handle: str = "main"
    edge_kind: str = "main"
    n8n_connection_type: str = "main"
    condition_ref: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "edge_id", _require_non_empty_text(self.edge_id, "edge_id"))
        object.__setattr__(self, "source_node_id", _require_non_empty_text(self.source_node_id, "source_node_id"))
        object.__setattr__(self, "target_node_id", _require_non_empty_text(self.target_node_id, "target_node_id"))
        object.__setattr__(self, "source_handle", _require_non_empty_text(self.source_handle, "source_handle"))
        object.__setattr__(self, "target_handle", _require_non_empty_text(self.target_handle, "target_handle"))
        object.__setattr__(
            self,
            "edge_kind",
            _require_allowed(self.edge_kind, "edge_kind", ALLOWED_WORKFLOW_EDGE_KINDS),
        )
        object.__setattr__(
            self,
            "n8n_connection_type",
            _require_allowed(
                self.n8n_connection_type,
                "n8n_connection_type",
                ALLOWED_N8N_CONNECTION_TYPES,
            ),
        )
        if self.condition_ref is not None:
            object.__setattr__(self, "condition_ref", _require_non_empty_text(self.condition_ref, "condition_ref"))
        if self.source_node_id == self.target_node_id:
            raise ValueError("workflow edge must not target the same node as its source")

    def referenced_node_ids(self) -> Tuple[str, str]:
        return (self.source_node_id, self.target_node_id)

    def to_read_model(self) -> dict[str, object]:
        return {
            "edge_id": self.edge_id,
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "source_handle": self.source_handle,
            "target_handle": self.target_handle,
            "edge_kind": self.edge_kind,
            "n8n_connection_type": self.n8n_connection_type,
            "condition_ref": self.condition_ref,
        }


def build_workflow_edge_contract(
    *,
    edge_id: str,
    source_node_id: str,
    target_node_id: str,
    source_handle: str = "main",
    target_handle: str = "main",
    edge_kind: str = "main",
    n8n_connection_type: str = "main",
    condition_ref: Optional[str] = None,
) -> WorkflowEdgeContract:
    return WorkflowEdgeContract(
        edge_id=edge_id,
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        source_handle=source_handle,
        target_handle=target_handle,
        edge_kind=edge_kind,
        n8n_connection_type=n8n_connection_type,
        condition_ref=condition_ref,
    )


__all__ = [
    "ALLOWED_N8N_CONNECTION_TYPES",
    "ALLOWED_WORKFLOW_EDGE_KINDS",
    "WorkflowEdgeContract",
    "build_workflow_edge_contract",
]
