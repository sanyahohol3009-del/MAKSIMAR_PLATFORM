from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.memory_policy import (
    MemoryFactClass,
)


AiRouterBindingStatus = Literal[
    "bound",
]

AiRouterRouteMode = Literal[
    "skill_plus_memory",
]

AiRouterLanguageCode = Literal[
    "en",
    "ru",
    "uk",
    "de",
]


_ROUTE_REQUEST_ID_PATTERN = re.compile(r"^route_[a-z][a-z0-9_]*$")
_SKILL_ID_PATTERN = re.compile(r"^skill_[a-z][a-z0-9_]*_[a-z][a-z0-9_]*$")
_MEMORY_TIER_ID_PATTERN = re.compile(r"^memory_[a-z][a-z0-9_]*$")
_WORKER_ID_PATTERN = re.compile(r"^worker_[a-z][a-z0-9_]*_001$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")
_SCOPE_ID_PATTERN = re.compile(r"^memscope_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class AiRouterMemorySkillBindingEntry:
    """Canonical AI router memory/skill binding entry."""

    route_request_id: str
    requested_fact_class: MemoryFactClass
    requested_language_code: AiRouterLanguageCode
    requested_script_name: str
    selected_skill_id: str
    selected_worker_id: str
    selected_memory_tier_id: str
    retrieval_scope_id: str
    selected_panel_id: str
    route_mode: AiRouterRouteMode
    route_status: AiRouterBindingStatus
    policy_compatible: bool
    explanation_available: bool
    active: bool
    description: str

    def __post_init__(self) -> None:
        """Validate AI router memory/skill binding invariants."""
        if not _ROUTE_REQUEST_ID_PATTERN.fullmatch(self.route_request_id):
            raise ValueError(f"Invalid route_request_id: {self.route_request_id}")

        if not _SKILL_ID_PATTERN.fullmatch(self.selected_skill_id):
            raise ValueError(f"Invalid selected_skill_id: {self.selected_skill_id}")

        if not _WORKER_ID_PATTERN.fullmatch(self.selected_worker_id):
            raise ValueError(f"Invalid selected_worker_id: {self.selected_worker_id}")

        if not _MEMORY_TIER_ID_PATTERN.fullmatch(self.selected_memory_tier_id):
            raise ValueError(
                f"Invalid selected_memory_tier_id: {self.selected_memory_tier_id}"
            )

        if not _SCOPE_ID_PATTERN.fullmatch(self.retrieval_scope_id):
            raise ValueError(f"Invalid retrieval_scope_id: {self.retrieval_scope_id}")

        if not _PANEL_ID_PATTERN.fullmatch(self.selected_panel_id):
            raise ValueError(f"Invalid selected_panel_id: {self.selected_panel_id}")

        if not self.requested_script_name.strip():
            raise ValueError(
                f"requested_script_name must not be empty: {self.route_request_id}"
            )

        if not self.description.strip():
            raise ValueError(f"description must not be empty: {self.route_request_id}")

        if self.route_mode != "skill_plus_memory":
            raise ValueError(
                f"AI router binding must use skill_plus_memory mode: {self.route_request_id}"
            )

        if self.route_status != "bound":
            raise ValueError(
                f"AI router binding must be bound: {self.route_request_id}"
            )

        if not self.policy_compatible:
            raise ValueError(
                f"AI router binding must be policy compatible: {self.route_request_id}"
            )

        if not self.explanation_available:
            raise ValueError(
                f"AI router binding must expose explanation path: {self.route_request_id}"
            )

        if not self.active:
            raise ValueError(
                f"AI router binding must target active registries: {self.route_request_id}"
            )


@dataclass(frozen=True, slots=True)
class AiRouterMemorySkillBindingContract:
    """Unified AI router memory/skill binding contract."""

    total_entries: int
    active_entries: int
    explanation_ready_entries: int
    policy_compatible_entries: int
    entries: tuple[AiRouterMemorySkillBindingEntry, ...]

    def __post_init__(self) -> None:
        """Validate AI router memory/skill binding contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        active_entries = sum(1 for entry in self.entries if entry.active)
        explanation_ready_entries = sum(
            1 for entry in self.entries if entry.explanation_available
        )
        policy_compatible_entries = sum(
            1 for entry in self.entries if entry.policy_compatible
        )

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        if self.explanation_ready_entries != explanation_ready_entries:
            raise ValueError("explanation_ready_entries must match computed count")

        if self.policy_compatible_entries != policy_compatible_entries:
            raise ValueError("policy_compatible_entries must match computed count")

        route_request_ids = tuple(entry.route_request_id for entry in self.entries)
        retrieval_scope_ids = tuple(entry.retrieval_scope_id for entry in self.entries)

        if len(set(route_request_ids)) != len(route_request_ids):
            raise ValueError("Duplicate route_request_id values detected")

        if len(set(retrieval_scope_ids)) != len(retrieval_scope_ids):
            raise ValueError("Duplicate retrieval_scope_id values detected")
