from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_boot_restore_sequence_contract import (
    build_dashboard_boot_restore_sequence_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_session_restore_contract import (
    build_dashboard_session_restore_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (
    build_display_assignment_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_restore_contract import (
    build_display_assignment_restore_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_conflict_resolution_contract import (
    build_display_conflict_resolution_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_continuity_snapshot_contract import (
    build_display_continuity_snapshot_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_restore_continuity_contract import (
    build_display_restore_continuity_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.input_mode_restore_contract import (
    build_input_mode_restore_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_inventory_contract import (
    build_monitor_inventory_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_placement_restore_contract import (
    build_panel_placement_restore_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_restore_contract import (
    build_workspace_restore_contract,
)


def test_dashboard_restore_integration_cold_boot_path_is_ready() -> None:
    """Cold boot should restore workspace, input mode, and boot sequence."""
    workspace_restore_contract = build_workspace_restore_contract()
    input_mode_restore_contract = build_input_mode_restore_contract()
    dashboard_boot_restore_sequence_contract = (
        build_dashboard_boot_restore_sequence_contract()
    )

    workspace_restore_entry = workspace_restore_contract.entries[0]
    input_mode_restore_entry = input_mode_restore_contract.entries[0]
    boot_restore_entry = dashboard_boot_restore_sequence_contract.entries[0]

    assert workspace_restore_entry.workspace_restore_state == "workspace_restore_ready"
    assert input_mode_restore_entry.input_mode_restore_state == "input_mode_restore_ready"
    assert (
        boot_restore_entry.dashboard_boot_restore_sequence_state
        == "dashboard_boot_restore_sequence_ready"
    )

    assert workspace_restore_entry.workspace_id == "workspace_foundation_monitoring"
    assert input_mode_restore_entry.workspace_id == workspace_restore_entry.workspace_id
    assert boot_restore_entry.workspace_id == workspace_restore_entry.workspace_id


def test_dashboard_restore_integration_crash_restart_preserves_restore_continuity() -> None:
    """Crash restart path should preserve continuity across restore layers."""
    display_assignment_restore_contract = build_display_assignment_restore_contract()
    display_restore_continuity_contract = build_display_restore_continuity_contract()
    dashboard_session_restore_contract = build_dashboard_session_restore_contract()

    restore_by_assignment_id = {
        entry.assignment_id: entry for entry in display_assignment_restore_contract.entries
    }

    continuity_entries = display_restore_continuity_contract.entries
    session_entry = dashboard_session_restore_contract.entries[0]

    assert session_entry.dashboard_session_restore_state == "dashboard_session_restore_ready"
    assert session_entry.display_restore_continuity_ready is True

    for continuity_entry in continuity_entries:
        restore_entry = restore_by_assignment_id[continuity_entry.assignment_id]

        assert continuity_entry.restore_continuity_state == "restore_continuity_preserved"
        assert continuity_entry.workspace_id == restore_entry.workspace_id

        if restore_entry.restore_decision == "restore_direct":
            assert (
                continuity_entry.restore_continuity_class
                == "direct_restore_continuity"
            )
        else:
            assert (
                continuity_entry.restore_continuity_class
                == "shared_surface_restore_continuity"
            )


def test_dashboard_restore_integration_monitor_loss_return_keeps_snapshot_consistent() -> None:
    """Monitor inventory and continuity snapshot must remain aligned."""
    monitor_inventory_contract = build_monitor_inventory_contract()
    continuity_snapshot_contract = build_display_continuity_snapshot_contract()

    inventory_by_display_target_id = {
        entry.display_target_id: entry for entry in monitor_inventory_contract.entries
    }

    assert continuity_snapshot_contract.total_entries == 3

    for snapshot_entry in continuity_snapshot_contract.entries:
        inventory_entry = inventory_by_display_target_id[snapshot_entry.display_target_id]

        assert snapshot_entry.snapshot_state == "snapshot_ready"
        assert snapshot_entry.operator_visible is True
        assert snapshot_entry.active_assignments == inventory_entry.active_assignments
        assert snapshot_entry.shared_surface == inventory_entry.shared_surface
        assert snapshot_entry.selected_assignment_present is True


def test_dashboard_restore_integration_reassignment_matches_panel_restore_chain() -> None:
    """Reassignment path should remain aligned across session and panel placement restore."""
    dashboard_session_restore_contract = build_dashboard_session_restore_contract()
    panel_placement_restore_contract = build_panel_placement_restore_contract()
    display_assignment_restore_contract = build_display_assignment_restore_contract()

    session_entry = dashboard_session_restore_contract.entries[0]
    panel_restore_entry = panel_placement_restore_contract.entries[0]

    assert session_entry.dashboard_session_restore_state == "dashboard_session_restore_ready"
    assert panel_restore_entry.panel_placement_restore_state == "panel_placement_restore_ready"

    assert session_entry.workspace_id == panel_restore_entry.workspace_id
    assert panel_restore_entry.dashboard_session_restore_ready is True
    assert panel_restore_entry.display_assignment_restore_ready is True

    assert display_assignment_restore_contract.total_entries >= 1
    assert display_assignment_restore_contract.operator_visible_entries == (
        display_assignment_restore_contract.total_entries
    )


def test_dashboard_restore_integration_stale_continuity_snapshot_is_not_allowed() -> None:
    """Continuity snapshot must remain aligned with active assignment registry."""
    display_assignment_registry_contract = build_display_assignment_registry_contract()
    continuity_snapshot_contract = build_display_continuity_snapshot_contract()

    active_assignments_by_display_target_id: dict[str, int] = {}
    for entry in display_assignment_registry_contract.entries:
        active_assignments_by_display_target_id[entry.display_target_id] = (
            active_assignments_by_display_target_id.get(entry.display_target_id, 0) + 1
        )

    for snapshot_entry in continuity_snapshot_contract.entries:
        assert snapshot_entry.snapshot_state == "snapshot_ready"
        assert snapshot_entry.active_assignments == active_assignments_by_display_target_id[
            snapshot_entry.display_target_id
        ]


def test_dashboard_restore_integration_conflict_resolution_stays_restore_safe() -> None:
    """Conflict resolution must stay aligned with restore and boot-ready chain."""
    display_conflict_resolution_contract = build_display_conflict_resolution_contract()
    display_assignment_restore_contract = build_display_assignment_restore_contract()
    dashboard_boot_restore_sequence_contract = (
        build_dashboard_boot_restore_sequence_contract()
    )

    restore_assignment_ids = {
        entry.assignment_id for entry in display_assignment_restore_contract.entries
    }
    boot_entry = dashboard_boot_restore_sequence_contract.entries[0]

    assert (
        boot_entry.dashboard_boot_restore_sequence_state
        == "dashboard_boot_restore_sequence_ready"
    )
    assert boot_entry.input_mode_restore_ready is True
    assert boot_entry.workspace_restore_ready is True

    for conflict_entry in display_conflict_resolution_contract.entries:
        assert conflict_entry.operator_visible is True
        assert conflict_entry.incumbent_assignment_id in restore_assignment_ids

        if conflict_entry.conflict_decision == "retain_pinned_surface":
            assert conflict_entry.candidate_display_target_id is None
            assert conflict_entry.conflict_class == "pinned_primary_conflict"
        else:
            assert conflict_entry.candidate_display_target_id is not None
            assert (
                conflict_entry.conflict_class
                == "replaceable_secondary_conflict"
            )
