from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_shell_handoff_contract import (
    build_visual_first_shell_handoff_contract,
)


PresentableResultMode = Literal[
    "first_presentable_result",
]

PresentableResultStatus = Literal[
    "presentable_result_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstPresentableResultEntry:
    """Canonical first presentable result entry."""

    presentable_result_id: str
    shell_handoff_id: str
    presentable_result_mode: PresentableResultMode
    presentable_result_status: PresentableResultStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    shell_handoff_ready: bool
    presentable_result_ready: bool
    truth_bound_presentable_result: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstPresentableResultContract:
    """Canonical first presentable result contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstPresentableResultEntry, ...]


def build_visual_first_presentable_result_contract(
) -> VisualFirstPresentableResultContract:
    """Build canonical first presentable result contract."""
    shell_handoff_contract = build_visual_first_shell_handoff_contract()
    shell_handoff_entry = shell_handoff_contract.entries[0]

    entries = (
        VisualFirstPresentableResultEntry(
            presentable_result_id="visual_first_presentable_result_001",
            shell_handoff_id=shell_handoff_entry.shell_handoff_id,
            presentable_result_mode="first_presentable_result",
            presentable_result_status="presentable_result_ready",
            renderer_surface_id=shell_handoff_entry.renderer_surface_id,
            theme_id=shell_handoff_entry.theme_id,
            screen_id=shell_handoff_entry.screen_id,
            preview_artifact_id=shell_handoff_entry.preview_artifact_id,
            shell_handoff_ready=shell_handoff_entry.shell_handoff_ready,
            presentable_result_ready=True,
            truth_bound_presentable_result=True,
            read_only=True,
            description=(
                "Canonical first presentable result entry after assembly of "
                "the first truth-preserving shell handoff."
            ),
        ),
    )

    return VisualFirstPresentableResultContract(
        contract_id="visual_first_presentable_result_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.presentable_result_status == "presentable_result_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
