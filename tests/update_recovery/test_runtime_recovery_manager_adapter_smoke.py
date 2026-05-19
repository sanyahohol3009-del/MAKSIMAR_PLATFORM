from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_SERVER.UPDATE_RECOVERY.adapters.runtime_recovery_manager_adapter import (
    RUNTIME_RECOVERY_MANAGER_ADAPTER_ID,
    RuntimeRecoveryManagerAdapterReadModel,
    build_runtime_recovery_manager_adapter_read_model,
)


def test_runtime_recovery_manager_adapter_preserves_existing_manager() -> None:
    read_model = build_runtime_recovery_manager_adapter_read_model(project_root=Path.cwd())

    assert read_model.adapter_id == RUNTIME_RECOVERY_MANAGER_ADAPTER_ID
    assert read_model.source_path == "RUNTIME/recovery_manager.py"
    assert read_model.adapter_bound is True
    assert read_model.recovery_manager_preserved is True
    assert read_model.replaces_existing_manager is False
    assert read_model.move_allowed is False
    assert read_model.delete_allowed is False
    assert read_model.migration_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.runtime_apply_allowed is False
    assert read_model.canonical_write_allowed is False
    assert read_model.dashboard_execution_allowed is False


def test_runtime_recovery_manager_adapter_rejects_source_move() -> None:
    base = build_runtime_recovery_manager_adapter_read_model(project_root=Path.cwd())

    with pytest.raises(ValueError, match="move_allowed"):
        RuntimeRecoveryManagerAdapterReadModel(
            adapter_id=RUNTIME_RECOVERY_MANAGER_ADAPTER_ID,
            source_path=base.source_path,
            source_exists=base.source_exists,
            adapter_bound=True,
            recovery_manager_preserved=True,
            replaces_existing_manager=False,
            move_allowed=True,
            delete_allowed=False,
            migration_allowed=False,
            reason_codes=("bad",),
        )
