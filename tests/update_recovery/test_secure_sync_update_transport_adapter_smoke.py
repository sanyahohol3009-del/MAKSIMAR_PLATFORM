from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_SERVER.UPDATE_RECOVERY.adapters.secure_sync_update_transport_adapter import (
    SECURE_SYNC_UPDATE_TRANSPORT_ADAPTER_ID,
    SecureSyncUpdateTransportAdapterReadModel,
    build_secure_sync_update_transport_adapter_read_model,
)


def test_secure_sync_update_transport_adapter_is_dashboard_safe_wrapper() -> None:
    read_model = build_secure_sync_update_transport_adapter_read_model(project_root=Path.cwd())

    assert read_model.adapter_id == SECURE_SYNC_UPDATE_TRANSPORT_ADAPTER_ID
    assert read_model.adapter_bound is True
    assert read_model.replaces_existing_transport is False
    assert read_model.move_allowed is False
    assert read_model.delete_allowed is False
    assert read_model.migration_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.runtime_apply_allowed is False
    assert read_model.canonical_write_allowed is False
    assert read_model.dashboard_execution_allowed is False
    assert read_model.facade_read_model.existing_transport_bound is True


def test_secure_sync_update_transport_adapter_rejects_replacement() -> None:
    base = build_secure_sync_update_transport_adapter_read_model(project_root=Path.cwd())

    with pytest.raises(ValueError, match="replaces_existing_transport"):
        SecureSyncUpdateTransportAdapterReadModel(
            adapter_id=SECURE_SYNC_UPDATE_TRANSPORT_ADAPTER_ID,
            source_path=base.source_path,
            facade_read_model=base.facade_read_model,
            source_exists=base.source_exists,
            adapter_bound=True,
            replaces_existing_transport=True,
            move_allowed=False,
            delete_allowed=False,
            migration_allowed=False,
            reason_codes=("bad",),
        )
