from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.update_recovery.secure_sync_update_facade_contract import (
    SECURE_SYNC_UPDATE_FACADE_CONTRACT_ID,
    SecureSyncUpdateFacadeReadModel,
    build_secure_sync_update_facade_read_model,
)


def test_secure_sync_update_facade_preserves_existing_transport() -> None:
    read_model = build_secure_sync_update_facade_read_model()

    assert read_model.contract_id == SECURE_SYNC_UPDATE_FACADE_CONTRACT_ID
    assert read_model.source_surface == "secure_sync_update_transport"
    assert read_model.facade_surface == "UPDATE_RECOVERY"
    assert read_model.existing_transport_bound is True
    assert read_model.replaces_existing_transport is False
    assert read_model.transport_move_allowed is False
    assert read_model.transport_delete_allowed is False
    assert read_model.migration_allowed is False
    assert read_model.signed_update_required is True
    assert read_model.direct_apply_allowed is False


def test_secure_sync_update_facade_rejects_transport_replacement() -> None:
    with pytest.raises(ValueError, match="replaces_existing_transport"):
        SecureSyncUpdateFacadeReadModel(
            read_model_id="secure_sync_update_facade_read_model_v1",
            contract_id=SECURE_SYNC_UPDATE_FACADE_CONTRACT_ID,
            source_surface="secure_sync_update_transport",
            source_path="MAKSIMAR_CORE_LIB/secure_sync_update_transport/secure_sync_update_transport_contract.py",
            facade_surface="UPDATE_RECOVERY",
            existing_transport_bound=True,
            replaces_existing_transport=True,
            transport_move_allowed=False,
            transport_delete_allowed=False,
            migration_allowed=False,
            signed_update_required=True,
            reason_codes=("bad",),
        )
