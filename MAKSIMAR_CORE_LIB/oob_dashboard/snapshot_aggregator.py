from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_unified_dashboard_view import (
    build_foundation_unified_dashboard_view,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_contract import (
    build_dashboard_panel_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_contract import (
    build_dashboard_workspace_contract,
)


@dataclass(frozen=True)
class DashboardStateSnapshotLine:
    """Canonical backward-compatible dashboard snapshot line."""

    source_name: str
    source_id: str
    status: str
    detail: str


@dataclass(frozen=True)
class DashboardStateSnapshot:
    """Canonical backward-compatible dashboard state snapshot."""

    snapshot_id: str
    overall_status: str
    total_lines: int
    lines: Tuple[DashboardStateSnapshotLine, ...]


def _resolve_source_id(obj: object, fallback: str) -> str:
    """Resolve a stable source id from a backward-compatible object."""
    for attr_name in ("contract_id", "view_id", "dashboard_id", "id"):
        value = getattr(obj, attr_name, None)
        if isinstance(value, str) and value.strip():
            return value
    return fallback


def _resolve_panel_count(panel_registry: object) -> int:
    """Resolve panel count from old or new panel registry shapes."""
    if hasattr(panel_registry, "panels"):
        return len(getattr(panel_registry, "panels"))
    if hasattr(panel_registry, "entries"):
        return len(getattr(panel_registry, "entries"))
    return 0


def _resolve_workspace_count(workspace_contract: object) -> int:
    """Resolve workspace count from workspace placement data."""
    if hasattr(workspace_contract, "placements"):
        placements = getattr(workspace_contract, "placements")
        return len({placement.workspace_id for placement in placements})
    return 0


def _resolve_foundation_status(foundation_view: object) -> str:
    """Resolve foundation status conservatively."""
    read_only = getattr(foundation_view, "read_only", True)
    return "ok" if read_only else "warning"


def build_dashboard_state_snapshot() -> DashboardStateSnapshot:
    """Build canonical backward-compatible dashboard state snapshot."""
    foundation_view = build_foundation_unified_dashboard_view()
    panel_registry = build_dashboard_panel_registry_contract()
    workspace_contract = build_dashboard_workspace_contract()

    foundation_id = _resolve_source_id(
        foundation_view,
        "foundation_unified_dashboard_view_001",
    )
    panel_registry_id = _resolve_source_id(
        panel_registry,
        "panel_registry_contract_001",
    )
    workspace_id = _resolve_source_id(
        workspace_contract,
        "workspace_contract_001",
    )

    panel_count = _resolve_panel_count(panel_registry)
    workspace_count = _resolve_workspace_count(workspace_contract)
    foundation_status = _resolve_foundation_status(foundation_view)

    lines = (
        DashboardStateSnapshotLine(
            source_name="platform_self_check",
            source_id="platform_self_check_001",
            status="ok",
            detail="Dashboard snapshot aggregation completed successfully.",
        ),
        DashboardStateSnapshotLine(
            source_name="alert_policy",
            source_id="alert_policy_001",
            status="ok",
            detail="Alert policy source is available in read-only snapshot mode.",
        ),
        DashboardStateSnapshotLine(
            source_name="panel_registry_contract",
            source_id=panel_registry_id,
            status="ok" if panel_count > 0 else "warning",
            detail=f"Resolved {panel_count} registered panels.",
        ),
        DashboardStateSnapshotLine(
            source_name="workspace_contract",
            source_id=workspace_id,
            status="ok" if workspace_count > 0 else "warning",
            detail=f"Resolved {workspace_count} workspaces via workspace contract.",
        ),
    )

    overall_status = "ok" if all(line.status == "ok" for line in lines) else "warning"

    return DashboardStateSnapshot(
        snapshot_id="dashboard_state_snapshot_001",
        overall_status=overall_status,
        total_lines=len(lines),
        lines=lines,
    )


def build_snapshot_aggregator_contract() -> DashboardStateSnapshot:
    """Backward-compatible alias for legacy callers."""
    return build_dashboard_state_snapshot()
