from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_display_output_contract import (
    build_visual_first_display_output_contract,
)


ShellHandoffMode = Literal[
    "first_shell_handoff",
]

ShellHandoffStatus = Literal[
    "shell_handoff_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstShellHandoffEntry:
    """Canonical first shell handoff entry."""

    shell_handoff_id: str
    display_output_id: str
    shell_handoff_mode: ShellHandoffMode
    shell_handoff_status: ShellHandoffStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    display_output_ready: bool
    shell_handoff_ready: bool
    truth_bound_shell_handoff: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstShellHandoffContract:
    """Canonical first shell handoff contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstShellHandoffEntry, ...]


def build_visual_first_shell_handoff_contract() -> VisualFirstShellHandoffContract:
    """Build canonical first shell handoff contract."""
    display_output_contract = build_visual_first_display_output_contract()
    display_output_entry = display_output_contract.entries[0]

    entries = (
        VisualFirstShellHandoffEntry(
            shell_handoff_id="visual_first_shell_handoff_001",
            display_output_id=display_output_entry.display_output_id,
            shell_handoff_mode="first_shell_handoff",
            shell_handoff_status="shell_handoff_ready",
            renderer_surface_id=display_output_entry.renderer_surface_id,
            theme_id=display_output_entry.theme_id,
            screen_id=display_output_entry.screen_id,
            preview_artifact_id=display_output_entry.preview_artifact_id,
            display_output_ready=display_output_entry.display_output_ready,
            shell_handoff_ready=True,
            truth_bound_shell_handoff=True,
            read_only=True,
            description=(
                "Canonical first shell handoff entry after assembly of the "
                "first truth-preserving display output."
            ),
        ),
    )

    return VisualFirstShellHandoffContract(
        contract_id="visual_first_shell_handoff_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.shell_handoff_status == "shell_handoff_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
