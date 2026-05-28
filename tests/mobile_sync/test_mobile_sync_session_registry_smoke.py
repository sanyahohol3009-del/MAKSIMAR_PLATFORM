import pytest

from MAKSIMAR_SERVER.MOBILE_SYNC_RUNTIME.mobile_sync_session_registry import (
    MobileSyncSessionRegistry,
    MobileSyncSessionState,
)
from shared_mobile_core.mobile_sync_models.mobile_sync_policy import MobileSyncPolicy


def _policy() -> MobileSyncPolicy:
    return MobileSyncPolicy.strict_default(policy_id="mobile_sync_policy_001")


def test_mobile_sync_session_registry_creates_read_only_session_state() -> None:
    registry = MobileSyncSessionRegistry(registry_id="mobile_sync_registry_001")
    session = registry.create_session(
        session_id="sync_session_001",
        owner_identity_id="owner_001",
        device_id="device_001",
        app_id="maksimar_mobile",
        policy=_policy(),
        created_at_epoch_ms=1000,
    )

    assert session.read_only_state is True
    assert session.canonical_truth is False
    assert session.core_write_allowed is False
    assert session.direct_server_write_allowed is False
    assert session.network_allowed is False
    assert session.socket_allowed is False
    assert session.tunnel_allowed is False
    assert session.mutates_app_memory_store is False
    assert session.mutates_chat_memory_store is False
    assert registry.get_session("sync_session_001") == session


def test_mobile_sync_session_registry_rejects_duplicate_session_ids() -> None:
    registry = MobileSyncSessionRegistry(registry_id="mobile_sync_registry_001")
    registry.create_session(
        session_id="sync_session_001",
        owner_identity_id="owner_001",
        device_id="device_001",
        app_id="maksimar_mobile",
        policy=_policy(),
        created_at_epoch_ms=1000,
    )

    with pytest.raises(ValueError, match="duplicate mobile sync session id"):
        registry.create_session(
            session_id="sync_session_001",
            owner_identity_id="owner_001",
            device_id="device_001",
            app_id="maksimar_mobile",
            policy=_policy(),
            created_at_epoch_ms=1001,
        )


def test_mobile_sync_session_state_rejects_core_write() -> None:
    with pytest.raises(ValueError, match="core_write_allowed must be False"):
        MobileSyncSessionState(
            session_id="bad_session",
            owner_identity_id="owner_001",
            device_id="device_001",
            app_id="maksimar_mobile",
            policy=_policy(),
            created_at_epoch_ms=1000,
            session_ref="session://bad_session",
            read_only_state=True,
            canonical_truth=False,
            core_write_allowed=True,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            canonical_state_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )
