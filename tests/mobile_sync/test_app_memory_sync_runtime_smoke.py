import pytest

from MAKSIMAR_SERVER.MOBILE_SYNC_RUNTIME.app_memory_sync_runtime import (
    AppMemorySyncDecision,
    AppMemorySyncRuntime,
)
from MAKSIMAR_SERVER.MOBILE_SYNC_RUNTIME.mobile_sync_session_registry import MobileSyncSessionRegistry
from shared_mobile_core.mobile_sync_models.mobile_sync_cursor_contract import MobileSyncCursorContract
from shared_mobile_core.mobile_sync_models.mobile_sync_envelope_contract import MobileSyncEnvelopeContract
from shared_mobile_core.mobile_sync_models.mobile_sync_policy import MobileSyncPolicy


def _policy() -> MobileSyncPolicy:
    return MobileSyncPolicy.strict_default(policy_id="mobile_sync_policy_001")


def _session():
    return MobileSyncSessionRegistry(registry_id="registry_001").create_session(
        session_id="sync_session_001",
        owner_identity_id="owner_001",
        device_id="device_001",
        app_id="maksimar_mobile",
        policy=_policy(),
        created_at_epoch_ms=1000,
    )


def _app_envelope() -> MobileSyncEnvelopeContract:
    return MobileSyncEnvelopeContract.for_app_memory(
        envelope_id="app_env_001",
        source_device_id="device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        record_refs=("app-memory://device_001/records/app-record-001",),
        cursor_ref="cursor://device_001/app_memory/2",
        policy_ref="policy://mobile_sync_policy_001",
        audit_ref="audit://app_env_001",
    )


def _app_cursor() -> MobileSyncCursorContract:
    return MobileSyncCursorContract.advance(
        cursor_id="app_cursor_001",
        memory_domain="app_memory",
        source_device_id="device_001",
        previous_sequence=1,
        accepted_sequence=2,
    )


def test_app_memory_sync_runtime_accepts_only_app_memory_envelope() -> None:
    runtime = AppMemorySyncRuntime.default(runtime_id="app_sync_runtime_001", policy=_policy())
    decision = runtime.evaluate(session=_session(), envelope=_app_envelope(), cursor=_app_cursor())

    assert decision.decision_status == "accepted_reference_sync"
    assert decision.success_requires_evidence is True
    assert decision.silent_success_allowed is False
    assert decision.read_only is True
    assert decision.core_write_allowed is False
    assert decision.direct_server_write_allowed is False
    assert decision.network_allowed is False
    assert decision.socket_allowed is False
    assert decision.tunnel_allowed is False
    assert decision.mutates_app_memory_store is False
    assert decision.mutates_chat_memory_store is False


def test_app_memory_sync_runtime_rejects_chat_memory_envelope() -> None:
    runtime = AppMemorySyncRuntime.default(runtime_id="app_sync_runtime_001", policy=_policy())
    chat_envelope = MobileSyncEnvelopeContract.for_chat_memory(
        envelope_id="chat_env_001",
        source_device_id="device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        record_refs=("chat-memory://device_001/records/chat-record-001",),
        cursor_ref="cursor://device_001/chat_memory/2",
        policy_ref="policy://mobile_sync_policy_001",
        audit_ref="audit://chat_env_001",
    )
    chat_cursor = MobileSyncCursorContract.advance(
        cursor_id="chat_cursor_001",
        memory_domain="chat_memory",
        source_device_id="device_001",
        previous_sequence=1,
        accepted_sequence=2,
    )

    with pytest.raises(ValueError, match="app memory runtime accepts only app_memory envelopes"):
        runtime.evaluate(session=_session(), envelope=chat_envelope, cursor=chat_cursor)


def test_app_memory_sync_runtime_rejects_store_mutation_claim() -> None:
    with pytest.raises(ValueError, match="mutates_app_memory_store must be False"):
        AppMemorySyncDecision(
            decision_id="bad_decision",
            session=_session(),
            envelope=_app_envelope(),
            cursor=_app_cursor(),
            policy=_policy(),
            decision_status="accepted_reference_sync",
            decision_reason="bad_mutation",
            success_requires_evidence=True,
            silent_success_allowed=False,
            read_only=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            runtime_mutation_allowed=False,
            mutates_app_memory_store=True,
            mutates_chat_memory_store=False,
        )
