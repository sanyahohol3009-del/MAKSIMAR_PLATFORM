from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.optics_light_field_engine import (
    build_optics_light_field_engine_contract,
)
from MAKSIMAR_CORE_LIB.wrist_psc_display_integration import (
    build_wrist_psc_display_integration_contract,
)


AirDisplayResearchMode = Literal[
    "projection_assisted_research",
    "controlled_scattering_research",
    "beam_intersection_research",
]

ResearchMaturity = Literal[
    "experimental_only",
]

ExecutionEligibility = Literal[
    "forbidden_for_production_execution",
]

VisibilityMode = Literal[
    "public_research_visibility",
]

SafetyEnvelopeClass = Literal[
    "bounded_research_envelope",
]

ResearchSlotStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^airdisplay_[a-z][a-z0-9_]*$")
_ENGINE_ID_PATTERN = re.compile(r"^opticsengine_[a-z][a-z0-9_]*$")
_INTEGRATION_ID_PATTERN = re.compile(r"^wristdisplayint_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class AirDisplayResearchSlotEntry:
    """Canonical air display research slot entry."""

    research_entry_id: str
    research_mode: AirDisplayResearchMode
    linked_optics_engine_id: str
    linked_integration_entry_id: str
    research_maturity: ResearchMaturity
    execution_eligibility: ExecutionEligibility
    visibility_mode: VisibilityMode
    safety_envelope_class: SafetyEnvelopeClass
    explainable_required: bool
    research_only: bool
    production_path_allowed: bool
    slot_status: ResearchSlotStatus
    description: str

    def __post_init__(self) -> None:
        """Validate air display research slot invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.research_entry_id):
            raise ValueError(f"Invalid research_entry_id: {self.research_entry_id}")

        if not _ENGINE_ID_PATTERN.fullmatch(self.linked_optics_engine_id):
            raise ValueError(
                f"Invalid linked_optics_engine_id: {self.linked_optics_engine_id}"
            )

        if not _INTEGRATION_ID_PATTERN.fullmatch(self.linked_integration_entry_id):
            raise ValueError(
                f"Invalid linked_integration_entry_id: {self.linked_integration_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.research_entry_id}"
            )

        if self.research_maturity != "experimental_only":
            raise ValueError(
                f"research_maturity must be experimental_only: {self.research_entry_id}"
            )

        if self.execution_eligibility != "forbidden_for_production_execution":
            raise ValueError(
                f"execution_eligibility must be forbidden_for_production_execution: {self.research_entry_id}"
            )

        if self.visibility_mode != "public_research_visibility":
            raise ValueError(
                f"visibility_mode must be public_research_visibility: {self.research_entry_id}"
            )

        if self.safety_envelope_class != "bounded_research_envelope":
            raise ValueError(
                f"safety_envelope_class must be bounded_research_envelope: {self.research_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.research_entry_id}"
            )

        if not self.research_only:
            raise ValueError(
                f"research_only must be True: {self.research_entry_id}"
            )

        if self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be False: {self.research_entry_id}"
            )

        if self.slot_status != "defined":
            raise ValueError(
                f"slot_status must be defined: {self.research_entry_id}"
            )

        if self.research_mode == "projection_assisted_research":
            if self.linked_optics_engine_id != "opticsengine_projection_assisted_spatial_001":
                raise ValueError(
                    "projection_assisted_research must link opticsengine_projection_assisted_spatial_001"
                )
            if self.linked_integration_entry_id != "wristdisplayint_engineering_001":
                raise ValueError(
                    "projection_assisted_research must link wristdisplayint_engineering_001"
                )

        if self.research_mode == "controlled_scattering_research":
            if self.linked_optics_engine_id != "opticsengine_controlled_scattering_research_001":
                raise ValueError(
                    "controlled_scattering_research must link opticsengine_controlled_scattering_research_001"
                )
            if self.linked_integration_entry_id != "wristdisplayint_ar_001":
                raise ValueError(
                    "controlled_scattering_research must link wristdisplayint_ar_001"
                )

        if self.research_mode == "beam_intersection_research":
            if self.linked_optics_engine_id != "opticsengine_beam_intersection_research_001":
                raise ValueError(
                    "beam_intersection_research must link opticsengine_beam_intersection_research_001"
                )
            if self.linked_integration_entry_id != "wristdisplayint_ar_001":
                raise ValueError(
                    "beam_intersection_research must link wristdisplayint_ar_001"
                )


@dataclass(frozen=True, slots=True)
class AirDisplayResearchSlotContract:
    """Unified air display research slot contract."""

    total_entries: int
    research_only_entries: int
    production_forbidden_entries: int
    explainable_entries: int
    defined_entries: int
    entries: tuple[AirDisplayResearchSlotEntry, ...]

    def __post_init__(self) -> None:
        """Validate air display research slot contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        research_only_entries = sum(
            1 for entry in self.entries if entry.research_only
        )
        production_forbidden_entries = sum(
            1 for entry in self.entries if not entry.production_path_allowed
        )
        explainable_entries = sum(
            1 for entry in self.entries if entry.explainable_required
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.slot_status == "defined"
        )

        if self.research_only_entries != research_only_entries:
            raise ValueError("research_only_entries must match computed count")

        if self.production_forbidden_entries != production_forbidden_entries:
            raise ValueError(
                "production_forbidden_entries must match computed count"
            )

        if self.explainable_entries != explainable_entries:
            raise ValueError("explainable_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.research_entry_id for entry in self.entries)
        modes = tuple(entry.research_mode for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate research_entry_id values detected")

        if len(set(modes)) != len(modes):
            raise ValueError("Duplicate research_mode values detected")


def build_air_display_research_slot_contract() -> AirDisplayResearchSlotContract:
    """Build canonical air display research slot contract."""
    optics_contract = build_optics_light_field_engine_contract()
    integration_contract = build_wrist_psc_display_integration_contract()

    optics_ids = {entry.engine_entry_id for entry in optics_contract.entries}
    integration_ids = {entry.integration_entry_id for entry in integration_contract.entries}

    required_optics_ids = {
        "opticsengine_projection_assisted_spatial_001",
        "opticsengine_controlled_scattering_research_001",
        "opticsengine_beam_intersection_research_001",
    }
    required_integration_ids = {
        "wristdisplayint_engineering_001",
        "wristdisplayint_ar_001",
    }

    missing_optics = required_optics_ids - optics_ids
    if missing_optics:
        raise ValueError(f"Missing optics ids: {sorted(missing_optics)}")

    missing_integrations = required_integration_ids - integration_ids
    if missing_integrations:
        raise ValueError(
            f"Missing integration ids: {sorted(missing_integrations)}"
        )

    entries = (
        AirDisplayResearchSlotEntry(
            research_entry_id="airdisplay_projection_assisted_001",
            research_mode="projection_assisted_research",
            linked_optics_engine_id="opticsengine_projection_assisted_spatial_001",
            linked_integration_entry_id="wristdisplayint_engineering_001",
            research_maturity="experimental_only",
            execution_eligibility="forbidden_for_production_execution",
            visibility_mode="public_research_visibility",
            safety_envelope_class="bounded_research_envelope",
            explainable_required=True,
            research_only=True,
            production_path_allowed=False,
            slot_status="defined",
            description="Projection-assisted air display research slot.",
        ),
        AirDisplayResearchSlotEntry(
            research_entry_id="airdisplay_controlled_scattering_001",
            research_mode="controlled_scattering_research",
            linked_optics_engine_id="opticsengine_controlled_scattering_research_001",
            linked_integration_entry_id="wristdisplayint_ar_001",
            research_maturity="experimental_only",
            execution_eligibility="forbidden_for_production_execution",
            visibility_mode="public_research_visibility",
            safety_envelope_class="bounded_research_envelope",
            explainable_required=True,
            research_only=True,
            production_path_allowed=False,
            slot_status="defined",
            description="Controlled scattering air display research slot.",
        ),
        AirDisplayResearchSlotEntry(
            research_entry_id="airdisplay_beam_intersection_001",
            research_mode="beam_intersection_research",
            linked_optics_engine_id="opticsengine_beam_intersection_research_001",
            linked_integration_entry_id="wristdisplayint_ar_001",
            research_maturity="experimental_only",
            execution_eligibility="forbidden_for_production_execution",
            visibility_mode="public_research_visibility",
            safety_envelope_class="bounded_research_envelope",
            explainable_required=True,
            research_only=True,
            production_path_allowed=False,
            slot_status="defined",
            description="Beam intersection air display research slot.",
        ),
    )

    research_only_entries = sum(
        1 for entry in entries if entry.research_only
    )
    production_forbidden_entries = sum(
        1 for entry in entries if not entry.production_path_allowed
    )
    explainable_entries = sum(
        1 for entry in entries if entry.explainable_required
    )
    defined_entries = sum(
        1 for entry in entries if entry.slot_status == "defined"
    )

    return AirDisplayResearchSlotContract(
        total_entries=len(entries),
        research_only_entries=research_only_entries,
        production_forbidden_entries=production_forbidden_entries,
        explainable_entries=explainable_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
