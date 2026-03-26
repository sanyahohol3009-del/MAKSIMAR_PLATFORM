from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FoundationImmutableCoreBindingEntry:
    """Read-only immutable-core binding entry for foundation dashboards."""

    binding_entry_id: str
    core_artifact_id: str
    artifact_path: str
    immutable_candidate: bool
    integrity_visible: bool
    dashboard_visible: bool
    mutation_allowed_from_dashboard: bool
    verification_required_before_start: bool
    description: str


@dataclass(frozen=True)
class FoundationImmutableCoreBindingView:
    """Read-only immutable-core binding view for foundation dashboards."""

    view_id: str
    total_entries: int
    immutable_candidate_entries: int
    integrity_visible_entries: int
    dashboard_visible_entries: int
    verification_required_entries: int
    mutation_forbidden_entries: int
    entries: tuple[FoundationImmutableCoreBindingEntry, ...]


def build_foundation_immutable_core_binding_view() -> (
    FoundationImmutableCoreBindingView
):
    """Build read-only immutable-core binding view for foundation dashboards."""
    entries = (
        FoundationImmutableCoreBindingEntry(
            binding_entry_id="foundationimmutable_stop_gate_001",
            core_artifact_id="core_stop_gate_001",
            artifact_path="CORE_ROOT/stop_gate.py",
            immutable_candidate=True,
            integrity_visible=True,
            dashboard_visible=True,
            mutation_allowed_from_dashboard=False,
            verification_required_before_start=True,
            description="Immutable-core binding entry for STOP-GATE script.",
        ),
        FoundationImmutableCoreBindingEntry(
            binding_entry_id="foundationimmutable_stop_gate_watcher_001",
            core_artifact_id="core_stop_gate_watcher_001",
            artifact_path="CORE_ROOT/stop_gate_watcher.py",
            immutable_candidate=True,
            integrity_visible=True,
            dashboard_visible=True,
            mutation_allowed_from_dashboard=False,
            verification_required_before_start=True,
            description="Immutable-core binding entry for STOP-GATE watcher.",
        ),
        FoundationImmutableCoreBindingEntry(
            binding_entry_id="foundationimmutable_core_guard_001",
            core_artifact_id="core_core_guard_001",
            artifact_path="CORE_ROOT/core_guard.py",
            immutable_candidate=True,
            integrity_visible=True,
            dashboard_visible=True,
            mutation_allowed_from_dashboard=False,
            verification_required_before_start=True,
            description="Immutable-core binding entry for core guard.",
        ),
        FoundationImmutableCoreBindingEntry(
            binding_entry_id="foundationimmutable_integrity_verifier_001",
            core_artifact_id="core_integrity_verifier_001",
            artifact_path="CORE_ROOT/core_integrity_verifier.py",
            immutable_candidate=True,
            integrity_visible=True,
            dashboard_visible=True,
            mutation_allowed_from_dashboard=False,
            verification_required_before_start=True,
            description="Immutable-core binding entry for integrity verifier.",
        ),
        FoundationImmutableCoreBindingEntry(
            binding_entry_id="foundationimmutable_genesis_hash_001",
            core_artifact_id="core_genesis_hash_001",
            artifact_path="CORE_ROOT/genesis_hash.bin",
            immutable_candidate=True,
            integrity_visible=True,
            dashboard_visible=True,
            mutation_allowed_from_dashboard=False,
            verification_required_before_start=True,
            description="Immutable-core binding entry for genesis hash baseline.",
        ),
    )

    return FoundationImmutableCoreBindingView(
        view_id="foundation_immutable_core_binding_view_001",
        total_entries=len(entries),
        immutable_candidate_entries=sum(
            1 for entry in entries if entry.immutable_candidate
        ),
        integrity_visible_entries=sum(1 for entry in entries if entry.integrity_visible),
        dashboard_visible_entries=sum(1 for entry in entries if entry.dashboard_visible),
        verification_required_entries=sum(
            1 for entry in entries if entry.verification_required_before_start
        ),
        mutation_forbidden_entries=sum(
            1 for entry in entries if not entry.mutation_allowed_from_dashboard
        ),
        entries=entries,
    )
