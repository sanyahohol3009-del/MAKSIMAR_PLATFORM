from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


FoundationLifecycleKind = Literal[
    "boot",
    "shutdown",
]

FoundationLifecycleStageState = Literal[
    "PENDING",
    "ACTIVE",
    "COMPLETED",
    "FAILED",
]


@dataclass(frozen=True)
class FoundationBootShutdownStageTruthEntry:
    """Canonical boot/shutdown stage truth entry for foundation dashboards."""

    stage_entry_id: str
    lifecycle_kind: FoundationLifecycleKind
    stage_order_index: int
    stage_id: str
    display_title: str
    stage_state: FoundationLifecycleStageState
    timeout_threshold_seconds: int
    waiting_condition: str | None
    failed_stage: bool
    read_only: bool
    description: str


@dataclass(frozen=True)
class FoundationBootShutdownStageTruthView:
    """Canonical boot/shutdown stage truth view for foundation dashboards."""

    view_id: str
    total_entries: int
    boot_entries: int
    shutdown_entries: int
    pending_entries: int
    active_entries: int
    completed_entries: int
    failed_entries: int
    entries: tuple[FoundationBootShutdownStageTruthEntry, ...]


def build_foundation_boot_shutdown_stage_truth_view() -> (
    FoundationBootShutdownStageTruthView
):
    """Build canonical boot/shutdown stage truth view for foundation dashboards."""
    entries = (
        FoundationBootShutdownStageTruthEntry(
            stage_entry_id="foundation_boot_stage_001",
            lifecycle_kind="boot",
            stage_order_index=1,
            stage_id="boot_integrity_check",
            display_title="Boot Integrity Check",
            stage_state="COMPLETED",
            timeout_threshold_seconds=15,
            waiting_condition=None,
            failed_stage=False,
            read_only=True,
            description="Canonical boot stage for integrity check.",
        ),
        FoundationBootShutdownStageTruthEntry(
            stage_entry_id="foundation_boot_stage_002",
            lifecycle_kind="boot",
            stage_order_index=2,
            stage_id="boot_runtime_start",
            display_title="Runtime Start",
            stage_state="COMPLETED",
            timeout_threshold_seconds=15,
            waiting_condition=None,
            failed_stage=False,
            read_only=True,
            description="Canonical boot stage for runtime startup.",
        ),
        FoundationBootShutdownStageTruthEntry(
            stage_entry_id="foundation_boot_stage_003",
            lifecycle_kind="boot",
            stage_order_index=3,
            stage_id="boot_guard_chain_start",
            display_title="Guard Chain Start",
            stage_state="COMPLETED",
            timeout_threshold_seconds=20,
            waiting_condition=None,
            failed_stage=False,
            read_only=True,
            description="Canonical boot stage for guard-chain startup.",
        ),
        FoundationBootShutdownStageTruthEntry(
            stage_entry_id="foundation_shutdown_stage_001",
            lifecycle_kind="shutdown",
            stage_order_index=1,
            stage_id="shutdown_kernel_guard_stop",
            display_title="Kernel Guard Stop",
            stage_state="PENDING",
            timeout_threshold_seconds=15,
            waiting_condition="Awaiting shutdown command.",
            failed_stage=False,
            read_only=True,
            description="Canonical shutdown stage for kernel guard stop.",
        ),
        FoundationBootShutdownStageTruthEntry(
            stage_entry_id="foundation_shutdown_stage_002",
            lifecycle_kind="shutdown",
            stage_order_index=2,
            stage_id="shutdown_guard_chain_stop",
            display_title="Guard Chain Stop",
            stage_state="PENDING",
            timeout_threshold_seconds=20,
            waiting_condition="Awaiting shutdown command.",
            failed_stage=False,
            read_only=True,
            description="Canonical shutdown stage for guard-chain stop.",
        ),
        FoundationBootShutdownStageTruthEntry(
            stage_entry_id="foundation_shutdown_stage_003",
            lifecycle_kind="shutdown",
            stage_order_index=3,
            stage_id="shutdown_runtime_stop",
            display_title="Runtime Stop",
            stage_state="PENDING",
            timeout_threshold_seconds=15,
            waiting_condition="Awaiting shutdown command.",
            failed_stage=False,
            read_only=True,
            description="Canonical shutdown stage for runtime stop.",
        ),
    )

    return FoundationBootShutdownStageTruthView(
        view_id="foundation_boot_shutdown_stage_truth_view_001",
        total_entries=len(entries),
        boot_entries=sum(1 for entry in entries if entry.lifecycle_kind == "boot"),
        shutdown_entries=sum(
            1 for entry in entries if entry.lifecycle_kind == "shutdown"
        ),
        pending_entries=sum(1 for entry in entries if entry.stage_state == "PENDING"),
        active_entries=sum(1 for entry in entries if entry.stage_state == "ACTIVE"),
        completed_entries=sum(
            1 for entry in entries if entry.stage_state == "COMPLETED"
        ),
        failed_entries=sum(1 for entry in entries if entry.stage_state == "FAILED"),
        entries=entries,
    )
