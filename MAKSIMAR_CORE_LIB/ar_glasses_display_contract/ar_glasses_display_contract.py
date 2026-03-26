from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.optics_light_field_engine import (
    build_optics_light_field_engine_contract,
)
from MAKSIMAR_CORE_LIB.wrist_terminal_contract import (
    build_wrist_terminal_contract,
)


ArGlassesDisplayId = Literal[
    "ar_glasses_display_core_001",
]

DisplayPrivacyMode = Literal[
    "private_display",
]

AnchorMode = Literal[
    "spatial_anchor_required",
]

OverlayMode = Literal[
    "explanation_overlay_required",
]

GestureBindingMode = Literal[
    "gesture_linked_interface",
]

DisplayTransportMode = Literal[
    "wrist_proxy_handoff",
]

ArDisplayStatus = Literal[
    "defined",
]


_DISPLAY_ID_PATTERN = re.compile(r"^ar_[a-z][a-z0-9_]*$")
_ENGINE_ID_PATTERN = re.compile(r"^opticsengine_[a-z][a-z0-9_]*$")
_WRIST_ID_PATTERN = re.compile(r"^wrist_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class ArGlassesDisplayEntry:
    """Canonical AR glasses display contract entry."""

    ar_display_id: ArGlassesDisplayId
    linked_optics_engine_id: str
    linked_wrist_terminal_id: str
    display_privacy_mode: DisplayPrivacyMode
    anchor_mode: AnchorMode
    overlay_mode: OverlayMode
    gesture_binding_mode: GestureBindingMode
    display_transport_mode: DisplayTransportMode
    private_render_required: bool
    explanation_overlay_required: bool
    spatial_anchor_required: bool
    production_path_allowed: bool
    display_status: ArDisplayStatus
    description: str

    def __post_init__(self) -> None:
        """Validate AR glasses display invariants."""
        if not _DISPLAY_ID_PATTERN.fullmatch(self.ar_display_id):
            raise ValueError(f"Invalid ar_display_id: {self.ar_display_id}")

        if not _ENGINE_ID_PATTERN.fullmatch(self.linked_optics_engine_id):
            raise ValueError(
                f"Invalid linked_optics_engine_id: {self.linked_optics_engine_id}"
            )

        if not _WRIST_ID_PATTERN.fullmatch(self.linked_wrist_terminal_id):
            raise ValueError(
                f"Invalid linked_wrist_terminal_id: {self.linked_wrist_terminal_id}"
            )

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.ar_display_id}")

        if self.display_privacy_mode != "private_display":
            raise ValueError(
                f"AR glasses must use private_display: {self.ar_display_id}"
            )

        if self.anchor_mode != "spatial_anchor_required":
            raise ValueError(
                f"AR glasses must require spatial anchors: {self.ar_display_id}"
            )

        if self.overlay_mode != "explanation_overlay_required":
            raise ValueError(
                f"AR glasses must require explanation overlay: {self.ar_display_id}"
            )

        if self.gesture_binding_mode != "gesture_linked_interface":
            raise ValueError(
                f"AR glasses must use gesture_linked_interface: {self.ar_display_id}"
            )

        if self.display_transport_mode != "wrist_proxy_handoff":
            raise ValueError(
                f"AR glasses must use wrist_proxy_handoff: {self.ar_display_id}"
            )

        if not self.private_render_required:
            raise ValueError(
                f"private_render_required must be True: {self.ar_display_id}"
            )

        if not self.explanation_overlay_required:
            raise ValueError(
                f"explanation_overlay_required must be True: {self.ar_display_id}"
            )

        if not self.spatial_anchor_required:
            raise ValueError(
                f"spatial_anchor_required must be True: {self.ar_display_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.ar_display_id}"
            )

        if self.display_status != "defined":
            raise ValueError(
                f"display_status must be defined: {self.ar_display_id}"
            )

        if self.ar_display_id == "ar_glasses_display_core_001":
            if self.linked_optics_engine_id != "opticsengine_ar_glasses_projection_001":
                raise ValueError(
                    "ar_glasses_display_core_001 must link opticsengine_ar_glasses_projection_001"
                )
            if self.linked_wrist_terminal_id != "wrist_terminal_core_001":
                raise ValueError(
                    "ar_glasses_display_core_001 must link wrist_terminal_core_001"
                )


@dataclass(frozen=True, slots=True)
class ArGlassesDisplayContract:
    """Unified AR glasses display contract."""

    total_entries: int
    private_display_entries: int
    anchor_required_entries: int
    production_allowed_entries: int
    defined_entries: int
    entries: tuple[ArGlassesDisplayEntry, ...]

    def __post_init__(self) -> None:
        """Validate AR glasses display contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        private_display_entries = sum(
            1 for entry in self.entries if entry.display_privacy_mode == "private_display"
        )
        anchor_required_entries = sum(
            1 for entry in self.entries if entry.spatial_anchor_required
        )
        production_allowed_entries = sum(
            1 for entry in self.entries if entry.production_path_allowed
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.display_status == "defined"
        )

        if self.private_display_entries != private_display_entries:
            raise ValueError("private_display_entries must match computed count")

        if self.anchor_required_entries != anchor_required_entries:
            raise ValueError("anchor_required_entries must match computed count")

        if self.production_allowed_entries != production_allowed_entries:
            raise ValueError("production_allowed_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.ar_display_id for entry in self.entries)
        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate ar_display_id values detected")


def build_ar_glasses_display_contract() -> ArGlassesDisplayContract:
    """Build canonical AR glasses display contract."""
    optics_contract = build_optics_light_field_engine_contract()
    wrist_contract = build_wrist_terminal_contract()

    optics_ids = {entry.engine_entry_id for entry in optics_contract.entries}
    wrist_ids = {entry.wrist_terminal_id for entry in wrist_contract.entries}

    if "opticsengine_ar_glasses_projection_001" not in optics_ids:
        raise ValueError(
            "Expected opticsengine_ar_glasses_projection_001 in optics engine contract"
        )

    if "wrist_terminal_core_001" not in wrist_ids:
        raise ValueError(
            "Expected wrist_terminal_core_001 in wrist terminal contract"
        )

    entries = (
        ArGlassesDisplayEntry(
            ar_display_id="ar_glasses_display_core_001",
            linked_optics_engine_id="opticsengine_ar_glasses_projection_001",
            linked_wrist_terminal_id="wrist_terminal_core_001",
            display_privacy_mode="private_display",
            anchor_mode="spatial_anchor_required",
            overlay_mode="explanation_overlay_required",
            gesture_binding_mode="gesture_linked_interface",
            display_transport_mode="wrist_proxy_handoff",
            private_render_required=True,
            explanation_overlay_required=True,
            spatial_anchor_required=True,
            production_path_allowed=True,
            display_status="defined",
            description="Canonical AR glasses display contract for private anchored explainable rendering.",
        ),
    )

    private_display_entries = sum(
        1 for entry in entries if entry.display_privacy_mode == "private_display"
    )
    anchor_required_entries = sum(
        1 for entry in entries if entry.spatial_anchor_required
    )
    production_allowed_entries = sum(
        1 for entry in entries if entry.production_path_allowed
    )
    defined_entries = sum(
        1 for entry in entries if entry.display_status == "defined"
    )

    return ArGlassesDisplayContract(
        total_entries=len(entries),
        private_display_entries=private_display_entries,
        anchor_required_entries=anchor_required_entries,
        production_allowed_entries=production_allowed_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
