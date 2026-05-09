from __future__ import annotations

import re
from dataclasses import dataclass


_POLICY_ID_PATTERN = re.compile(r"^storage_policy_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True, slots=True)
class StoragePortabilityPolicy:
    """Portability policy for memory/artifact/model storage.

    This policy is read-only metadata. It does not move files and does not write
    runtime storage state.
    """

    policy_id: str
    storage_node_portable: bool
    root_relocation_allowed: bool
    nas_ready_required: bool
    external_media_allowed: bool
    model_weights_external: bool
    retrieval_index_rebuild_allowed: bool
    atomic_snapshot_required: bool

    def __post_init__(self) -> None:
        policy_id = _ensure_non_empty_str(self.policy_id, "policy_id")

        if not _POLICY_ID_PATTERN.fullmatch(policy_id):
            raise ValueError(f"Invalid policy_id: {policy_id}")

        for field_name in (
            "storage_node_portable",
            "root_relocation_allowed",
            "nas_ready_required",
            "external_media_allowed",
            "model_weights_external",
            "retrieval_index_rebuild_allowed",
            "atomic_snapshot_required",
        ):
            if not isinstance(getattr(self, field_name), bool):
                raise ValueError(f"{field_name} must be bool")

        object.__setattr__(self, "policy_id", policy_id)
