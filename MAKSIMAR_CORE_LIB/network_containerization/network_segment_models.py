from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


NetworkSegmentId = Literal[
    "net_core_safety",
    "net_control",
    "net_security",
    "net_governance",
    "net_data",
    "net_ai",
    "net_products",
    "net_observability",
    "net_update",
]


REQUIRED_NETWORK_SEGMENTS: tuple[NetworkSegmentId, ...] = (
    "net_core_safety",
    "net_control",
    "net_security",
    "net_governance",
    "net_data",
    "net_ai",
    "net_products",
    "net_observability",
    "net_update",
)


@dataclass(frozen=True, slots=True)
class NetworkSegmentModel:
    segment_id: NetworkSegmentId
    title: str
    public_exposure_allowed: bool
    runtime_network_mutation_allowed: bool
    internal_only: bool
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_segment_id(self.segment_id)
        _validate_non_empty("title", self.title)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_false("runtime_network_mutation_allowed", self.runtime_network_mutation_allowed)
        _validate_true("internal_only", self.internal_only)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "segment_id": self.segment_id,
            "title": self.title,
            "public_exposure_allowed": self.public_exposure_allowed,
            "runtime_network_mutation_allowed": self.runtime_network_mutation_allowed,
            "internal_only": self.internal_only,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_network_segment_model(segment_id: NetworkSegmentId) -> NetworkSegmentModel:
    _validate_segment_id(segment_id)
    title = segment_id.replace("_", " ").title()
    return NetworkSegmentModel(
        segment_id=segment_id,
        title=title,
        public_exposure_allowed=False,
        runtime_network_mutation_allowed=False,
        internal_only=True,
        dashboard_safe=True,
        reason_codes=(
            "network_segment_model_declared",
            "no_public_exposure_by_default",
            "no_runtime_network_mutation",
        ),
    )


def build_default_network_segments() -> tuple[NetworkSegmentModel, ...]:
    return tuple(build_network_segment_model(segment_id) for segment_id in REQUIRED_NETWORK_SEGMENTS)


def _validate_segment_id(segment_id: str) -> None:
    if segment_id not in REQUIRED_NETWORK_SEGMENTS:
        raise ValueError(f"unknown network segment: {segment_id}")


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_false(field_name: str, value: bool) -> None:
    if value:
        raise ValueError(f"{field_name} must remain false")


def _validate_true(field_name: str, value: bool) -> None:
    if not value:
        raise ValueError(f"{field_name} must remain true")


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        _validate_non_empty("reason_code", reason_code)
