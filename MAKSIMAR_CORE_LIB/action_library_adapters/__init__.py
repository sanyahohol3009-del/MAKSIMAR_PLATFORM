from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_RISK_CLASSES = {"read_only", "safe_direct", "risk_gate"}


@dataclass(frozen=True, slots=True)
class ActionWorkerAdapterContract:
    capability_id: str
    adapter_kind: str
    risk_class: str
    read_only: bool
    side_effects: tuple[str, ...]
    requires_verified_owner: bool
    safe_direct_allowed: bool
    recording_required: bool
    replay_preview_required: bool

    def __post_init__(self) -> None:
        for field_name in ("capability_id", "adapter_kind", "risk_class"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.risk_class not in _RISK_CLASSES:
            raise ValueError(f"unsupported risk_class: {self.risk_class!r}")
        if not self.side_effects:
            raise ValueError("side_effects must not be empty")
        if self.safe_direct_allowed and self.requires_verified_owner is not True:
            raise ValueError("safe_direct_allowed requires verified owner")
        if self.recording_required is not True:
            raise ValueError("recording_required must be True")
        if self.replay_preview_required is not True:
            raise ValueError("replay_preview_required must be True")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "adapter_kind": self.adapter_kind,
            "risk_class": self.risk_class,
            "read_only": self.read_only,
            "side_effects": self.side_effects,
            "requires_verified_owner": self.requires_verified_owner,
            "safe_direct_allowed": self.safe_direct_allowed,
            "recording_required": self.recording_required,
            "replay_preview_required": self.replay_preview_required,
        }


__all__ = ["ActionWorkerAdapterContract"]
