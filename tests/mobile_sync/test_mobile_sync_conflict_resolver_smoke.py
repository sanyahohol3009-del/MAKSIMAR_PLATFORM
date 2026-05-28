import pytest

from MAKSIMAR_SERVER.MOBILE_SYNC_RUNTIME.mobile_sync_conflict_resolver import (
    MobileSyncConflictResolution,
    MobileSyncConflictResolver,
)


def test_mobile_sync_conflict_resolver_is_deterministic_and_evidence_hash_backed() -> None:
    resolver = MobileSyncConflictResolver.default(resolver_id="mobile_sync_conflict_resolver_001")

    first = resolver.resolve(
        conflict_id="conflict_001",
        memory_domain="app_memory",
        local_record_ref="app-memory://device_001/records/app-record-001",
        server_record_ref="app-memory://server/records/app-record-001",
        local_sequence=4,
        server_sequence=5,
        local_updated_at_epoch_ms=1000,
        server_updated_at_epoch_ms=1100,
        conflict_policy_ref="policy://mobile_sync_conflict_default",
    )
    second = resolver.resolve(
        conflict_id="conflict_001",
        memory_domain="app_memory",
        local_record_ref="app-memory://device_001/records/app-record-001",
        server_record_ref="app-memory://server/records/app-record-001",
        local_sequence=4,
        server_sequence=5,
        local_updated_at_epoch_ms=1000,
        server_updated_at_epoch_ms=1100,
        conflict_policy_ref="policy://mobile_sync_conflict_default",
    )

    assert first.conflict.decision == "keep_server_reference"
    assert first.evidence_hash == second.evidence_hash
    assert first.deterministic is True
    assert first.success_requires_evidence is True
    assert first.silent_success_allowed is False
    assert first.mutates_records is False
    assert first.direct_server_write_allowed is False
    assert first.network_allowed is False


def test_mobile_sync_conflict_resolver_rejects_runtime_mutation_flags() -> None:
    with pytest.raises(ValueError, match="network_allowed must be False"):
        MobileSyncConflictResolver(
            resolver_id="bad_resolver",
            deterministic_only=True,
            read_only_runtime=True,
            mutates_records=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=True,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            runtime_mutation_allowed=False,
        )


def test_mobile_sync_conflict_resolution_rejects_silent_success() -> None:
    resolver = MobileSyncConflictResolver.default(resolver_id="mobile_sync_conflict_resolver_001")
    resolution = resolver.resolve(
        conflict_id="conflict_002",
        memory_domain="chat_memory",
        local_record_ref="chat-memory://device_001/records/chat-record-001",
        server_record_ref="chat-memory://server/records/chat-record-001",
        local_sequence=7,
        server_sequence=7,
        local_updated_at_epoch_ms=1300,
        server_updated_at_epoch_ms=1300,
        conflict_policy_ref="policy://mobile_sync_conflict_default",
    )

    with pytest.raises(ValueError, match="silent_success_allowed must be False"):
        MobileSyncConflictResolution(
            resolution_id="bad_resolution",
            conflict=resolution.conflict,
            deterministic=True,
            evidence_hash=resolution.evidence_hash,
            success_requires_evidence=True,
            silent_success_allowed=True,
            mutates_records=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            runtime_mutation_allowed=False,
        )
