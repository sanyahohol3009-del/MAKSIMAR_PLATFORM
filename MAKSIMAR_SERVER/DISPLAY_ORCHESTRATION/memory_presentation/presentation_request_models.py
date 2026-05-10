from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


PresentationIntent = Literal[
    "show_memory",
    "show_simulation",
    "show_monitoring",
]

_PRESENTATION_REQUEST_ID_PATTERN = re.compile(
    r"^presentation_request_[a-z][a-z0-9_]*_[0-9]{3}$"
)


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
class PresentationRequestEntry:
    presentation_request_id: str
    command_intent: PresentationIntent
    requested_view_hint: str
    requester_surface: str
    requires_explanation: bool
    requires_multilingual_rendering: bool
    read_only: bool
    action_execution_allowed: bool
    direct_display_switching_allowed: bool
    request_ready: bool
    description: str

    def __post_init__(self) -> None:
        request_id = _ensure_non_empty_str(
            self.presentation_request_id,
            "presentation_request_id",
        )
        if not _PRESENTATION_REQUEST_ID_PATTERN.fullmatch(request_id):
            raise ValueError(f"Invalid presentation_request_id: {request_id}")

        for field_name in (
            "requested_view_hint",
            "requester_surface",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "requires_explanation",
            "requires_multilingual_rendering",
            "read_only",
            "action_execution_allowed",
            "direct_display_switching_allowed",
            "request_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.requires_explanation:
            raise ValueError("requires_explanation must be True")
        if not self.requires_multilingual_rendering:
            raise ValueError("requires_multilingual_rendering must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.action_execution_allowed:
            raise ValueError("action_execution_allowed must be False")
        if self.direct_display_switching_allowed:
            raise ValueError("direct_display_switching_allowed must be False")
        if not self.request_ready:
            raise ValueError("request_ready must be True")


@dataclass(frozen=True, slots=True)
class PresentationRequestContract:
    total_requests: int
    ready_requests: int
    explanation_required_requests: int
    multilingual_ready_requests: int
    read_only_requests: int
    action_execution_allowed_requests: int
    direct_display_switching_allowed_requests: int
    entries: tuple[PresentationRequestEntry, ...]

    def __post_init__(self) -> None:
        if self.total_requests != len(self.entries):
            raise ValueError("total_requests must match entries length")
        if self.total_requests <= 0:
            raise ValueError("total_requests must be >= 1")

        expected = {
            "ready_requests": sum(1 for entry in self.entries if entry.request_ready),
            "explanation_required_requests": sum(
                1 for entry in self.entries if entry.requires_explanation
            ),
            "multilingual_ready_requests": sum(
                1 for entry in self.entries if entry.requires_multilingual_rendering
            ),
            "read_only_requests": sum(1 for entry in self.entries if entry.read_only),
            "action_execution_allowed_requests": sum(
                1 for entry in self.entries if entry.action_execution_allowed
            ),
            "direct_display_switching_allowed_requests": sum(
                1 for entry in self.entries if entry.direct_display_switching_allowed
            ),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_requests != self.total_requests:
            raise ValueError("all presentation requests must be ready")
        if self.explanation_required_requests != self.total_requests:
            raise ValueError("all presentation requests must require explanation")
        if self.multilingual_ready_requests != self.total_requests:
            raise ValueError("all presentation requests must be multilingual-ready")
        if self.read_only_requests != self.total_requests:
            raise ValueError("all presentation requests must be read-only")
        if self.action_execution_allowed_requests != 0:
            raise ValueError("presentation requests must not execute actions")
        if self.direct_display_switching_allowed_requests != 0:
            raise ValueError("presentation requests must not switch displays directly")


def build_presentation_request_contract() -> PresentationRequestContract:
    entries = (
        PresentationRequestEntry(
            presentation_request_id="presentation_request_show_memory_001",
            command_intent="show_memory",
            requested_view_hint="memory_project_architecture",
            requester_surface="operator_or_voice_command",
            requires_explanation=True,
            requires_multilingual_rendering=True,
            read_only=True,
            action_execution_allowed=False,
            direct_display_switching_allowed=False,
            request_ready=True,
            description="Read-only presentation request for memory view.",
        ),
        PresentationRequestEntry(
            presentation_request_id="presentation_request_show_simulation_001",
            command_intent="show_simulation",
            requested_view_hint="simulation_skill_overview",
            requester_surface="operator_or_voice_command",
            requires_explanation=True,
            requires_multilingual_rendering=True,
            read_only=True,
            action_execution_allowed=False,
            direct_display_switching_allowed=False,
            request_ready=True,
            description="Read-only presentation request for simulation view.",
        ),
        PresentationRequestEntry(
            presentation_request_id="presentation_request_show_monitoring_001",
            command_intent="show_monitoring",
            requested_view_hint="monitoring_panel",
            requester_surface="operator_or_voice_command",
            requires_explanation=True,
            requires_multilingual_rendering=True,
            read_only=True,
            action_execution_allowed=False,
            direct_display_switching_allowed=False,
            request_ready=True,
            description="Read-only presentation request for monitoring view.",
        ),
    )

    return PresentationRequestContract(
        total_requests=len(entries),
        ready_requests=sum(1 for entry in entries if entry.request_ready),
        explanation_required_requests=sum(
            1 for entry in entries if entry.requires_explanation
        ),
        multilingual_ready_requests=sum(
            1 for entry in entries if entry.requires_multilingual_rendering
        ),
        read_only_requests=sum(1 for entry in entries if entry.read_only),
        action_execution_allowed_requests=sum(
            1 for entry in entries if entry.action_execution_allowed
        ),
        direct_display_switching_allowed_requests=sum(
            1 for entry in entries if entry.direct_display_switching_allowed
        ),
        entries=entries,
    )
