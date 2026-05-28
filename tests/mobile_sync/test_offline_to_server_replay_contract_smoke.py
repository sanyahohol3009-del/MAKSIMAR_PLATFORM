import pytest

from shared_mobile_core.mobile_sync_models.mobile_sync_cursor_contract import MobileSyncCursorContract
from shared_mobile_core.mobile_sync_models.mobile_sync_envelope_contract import MobileSyncEnvelopeContract
from shared_mobile_core.mobile_sync_models.mobile_sync_policy import MobileSyncPolicy
from shared_mobile_core.mobile_sync_models.offline_to_server_replay_contract import OfflineToServerReplayContract


def _policy() -> MobileSyncPolicy:
    return MobileSyncPolicy.strict_default(policy_id="mobile_sync_policy_001")


def _envelope() -> MobileSyncEnvelopeContract:
    return MobileSyncEnvelopeContract.for_chat_memory(
        envelope_id="sync_env_chat_001",
        source_device_id="device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        record_refs=("chat-memory://device_001/records/chat-record-001",),
        cursor_ref="cursor://device_001/chat_memory/2",
        policy_ref="policy://mobile_sync_policy_001",
        audit_ref="audit://sync_env_chat_001",
    )


def _cursor() -> MobileSyncCursorContract:
    return MobileSyncCursorContract.advance(
        cursor_id="cursor_chat_001",
        memory_domain="chat_memory",
        source_device_id="device_001",
        previous_sequence=1,
        accepted_sequence=2,
    )


def test_offline_to_server_replay_requires_policy_approvals_and_trusted_presence() -> None:
    replay = OfflineToServerReplayContract.approved_replay(
        replay_id="offline_replay_001",
        policy=_policy(),
        envelope=_envelope(),
        cursor=_cursor(),
    )

    assert replay.sync_policy_required is True
    assert replay.owner_approval_granted is True
    assert replay.device_approval_granted is True
    assert replay.trusted_server_presence is True
    assert replay.replay_ready is True
    assert replay.replay_execution_allowed is False
    assert replay.core_write_allowed is False
    assert replay.direct_server_write_allowed is False
    assert replay.network_allowed is False
    assert replay.socket_allowed is False
    assert replay.tunnel_allowed is False
    assert replay.mutates_app_memory_store is False
    assert replay.mutates_chat_memory_store is False


def test_offline_to_server_replay_rejects_missing_owner_approval_when_ready() -> None:
    with pytest.raises(ValueError, match="replay_ready requires owner_approval_granted"):
        OfflineToServerReplayContract(
            replay_id="bad_replay_owner",
            policy=_policy(),
            envelope=_envelope(),
            cursor=_cursor(),
            replay_record_refs=("chat-memory://device_001/records/chat-record-001",),
            replay_intent_ref="replay://bad_replay_owner",
            audit_ref="audit://bad_replay_owner",
            sync_policy_required=True,
            owner_approval_granted=False,
            device_approval_granted=True,
            trusted_server_presence=True,
            replay_ready=True,
            replay_execution_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )


def test_offline_to_server_replay_rejects_network_or_store_mutation() -> None:
    with pytest.raises(ValueError, match="network_allowed must be False"):
        OfflineToServerReplayContract(
            replay_id="bad_replay_network",
            policy=_policy(),
            envelope=_envelope(),
            cursor=_cursor(),
            replay_record_refs=("chat-memory://device_001/records/chat-record-001",),
            replay_intent_ref="replay://bad_replay_network",
            audit_ref="audit://bad_replay_network",
            sync_policy_required=True,
            owner_approval_granted=True,
            device_approval_granted=True,
            trusted_server_presence=True,
            replay_ready=True,
            replay_execution_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=True,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )
