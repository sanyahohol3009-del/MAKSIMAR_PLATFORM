from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.offline_import_gate_contract import OfflineImportCandidate
from MAKSIMAR_CORE_LIB.update_recovery.rollback_manager_contract import RollbackPlanReference
from MAKSIMAR_CORE_LIB.update_recovery.snapshot_manager_contract import SnapshotReference
from MAKSIMAR_SERVER.UPDATE_RECOVERY.adapters.runtime_recovery_manager_adapter import (
    build_runtime_recovery_manager_adapter_read_model,
)
from MAKSIMAR_SERVER.UPDATE_RECOVERY.adapters.secure_sync_update_transport_adapter import (
    build_secure_sync_update_transport_adapter_read_model,
)
from MAKSIMAR_SERVER.UPDATE_RECOVERY.offline_import_gate import run_offline_import_gate
from MAKSIMAR_SERVER.UPDATE_RECOVERY.recovery_service import run_recovery_service_ready
from MAKSIMAR_SERVER.UPDATE_RECOVERY.rollback_manager import run_rollback_manager_ready
from MAKSIMAR_SERVER.UPDATE_RECOVERY.snapshot_manager import run_snapshot_manager_ready
from MAKSIMAR_SERVER.UPDATE_RECOVERY.update_recovery_health import build_update_recovery_health_read_model
from MAKSIMAR_SERVER.UPDATE_RECOVERY.update_recovery_read_model_builder import (
    build_update_recovery_runtime_read_model,
)

ONE = "1" * 64
TWO = "2" * 64


def build_update_recovery_preview_payload(project_root: Path | None = None) -> dict[str, Any]:
    package_id = "update-package-preview-001"
    root = Path.cwd() if project_root is None else project_root

    snapshot_runtime = run_snapshot_manager_ready(
        package_id=package_id,
        snapshot_reference=SnapshotReference(
            snapshot_id="snapshot-preview-001",
            snapshot_uri="snapshot://update-package-preview-001/snapshot-preview-001",
            snapshot_sha256=ONE,
            created_at_utc="2026-01-01T00:00:00Z",
            immutable=True,
            state_manifest_present=True,
            rollback_compatible=True,
        ),
    )
    rollback_runtime = run_rollback_manager_ready(
        package_id=package_id,
        rollback_plan_reference=RollbackPlanReference(
            rollback_plan_id="rollback-preview-001",
            rollback_uri="rollback://update-package-preview-001/rollback-preview-001",
            rollback_sha256=TWO,
            target_snapshot_id="snapshot-preview-001",
            tested=True,
            reversible=True,
        ),
        snapshot_readiness=snapshot_runtime.read_model,
    )
    recovery_runtime = run_recovery_service_ready(
        package_id=package_id,
        snapshot_readiness=snapshot_runtime.read_model,
        rollback_readiness=rollback_runtime.read_model,
    )
    offline_import_runtime = run_offline_import_gate(
        OfflineImportCandidate(
            import_id="offline-import-preview-001",
            package_id=package_id,
            source_uri="offline-media://preview/update-package-preview-001",
            package_sha256=ONE,
            created_at_utc="2026-01-01T00:00:00Z",
            signature_present=True,
            air_gap_transfer_confirmed=True,
            media_quarantined=True,
            operator_approval_present=True,
        )
    )
    runtime_read_model = build_update_recovery_runtime_read_model(
        package_id=package_id,
        secure_sync_transport_adapter=build_secure_sync_update_transport_adapter_read_model(project_root=root),
        runtime_recovery_manager_adapter=build_runtime_recovery_manager_adapter_read_model(project_root=root),
        snapshot_runtime=snapshot_runtime,
        rollback_runtime=rollback_runtime,
        recovery_runtime=recovery_runtime,
        offline_import_runtime=offline_import_runtime,
    )
    health = build_update_recovery_health_read_model(runtime_read_model)

    return {
        "preview_id": "update_recovery_terminal_preview_v1",
        "dashboard_safe": True,
        "runtime_apply_allowed": False,
        "canonical_write_allowed": False,
        "dashboard_execution_allowed": False,
        "health": health.to_dict(),
    }


def render_update_recovery_terminal_preview(project_root: Path | None = None) -> str:
    payload = build_update_recovery_preview_payload(project_root=project_root)
    return json.dumps(payload, indent=2, sort_keys=True)


def main() -> None:
    print(render_update_recovery_terminal_preview())


if __name__ == "__main__":
    main()
