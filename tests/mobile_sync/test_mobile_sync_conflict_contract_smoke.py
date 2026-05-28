import pytest

from shared_mobile_core.mobile_sync_models.mobile_sync_conflict_contract import MobileSyncConflictContract


def test_mobile_sync_conflict_decision_is_deterministic() -> None:
    first = MobileSyncConflictContract.decide(
        conflict_id="conflict_001",
        memory_domain="chat_memory",
        local_record_ref="chat-memory://device_001/records/chat-record-001",
        server_record_ref="chat-memory://server/records/chat-record-001",
        local_sequence=7,
        server_sequence=6,
        local_updated_at_epoch_ms=1200,
        server_updated_at_epoch_ms=1300,
        conflict_policy_ref="policy://mobile_sync_conflict_default",
    )
    second = MobileSyncConflictContract.decide(
        conflict_id="conflict_001",
        memory_domain="chat_memory",
        local_record_ref="chat-memory://device_001/records/chat-record-001",
        server_record_ref="chat-memory://server/records/chat-record-001",
        local_sequence=7,
        server_sequence=6,
        local_updated_at_epoch_ms=1200,
        server_updated_at_epoch_ms=1300,
        conflict_policy_ref="policy://mobile_sync_conflict_default",
    )

    assert first.decision == "keep_local_reference"
    assert first.decision == second.decision
    assert first.deterministic_evidence_hash == second.deterministic_evidence_hash
    assert first.mutates_records is False
    assert first.direct_server_write_allowed is False
    assert first.network_allowed is False


def test_mobile_sync_conflict_rejects_non_deterministic_decision_claim() -> None:
    base = MobileSyncConflictContract.decide(
        conflict_id="conflict_002",
        memory_domain="app_memory",
        local_record_ref="app-memory://device_001/records/app-record-001",
        server_record_ref="app-memory://server/records/app-record-001",
        local_sequence=3,
        server_sequence=4,
        local_updated_at_epoch_ms=1000,
        server_updated_at_epoch_ms=900,
        conflict_policy_ref="policy://mobile_sync_conflict_default",
    )

    with pytest.raises(ValueError, match="decision must match deterministic conflict decision"):
        MobileSyncConflictContract(
            conflict_id="bad_conflict_002",
            memory_domain=base.memory_domain,
            local_record_ref=base.local_record_ref,
            server_record_ref=base.server_record_ref,
            local_sequence=base.local_sequence,
            server_sequence=base.server_sequence,
            local_updated_at_epoch_ms=base.local_updated_at_epoch_ms,
            server_updated_at_epoch_ms=base.server_updated_at_epoch_ms,
            conflict_policy_ref=base.conflict_policy_ref,
            decision="keep_local_reference",
            decision_reason=base.decision_reason,
            deterministic_evidence_hash=base.deterministic_evidence_hash,
            deterministic_decision_required=True,
            mutates_records=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
        )


def test_mobile_sync_conflict_rejects_record_mutation() -> None:
    base = MobileSyncConflictContract.decide(
        conflict_id="conflict_003",
        memory_domain="app_memory",
        local_record_ref="app-memory://device_001/records/app-record-003",
        server_record_ref="app-memory://server/records/app-record-003",
        local_sequence=5,
        server_sequence=5,
        local_updated_at_epoch_ms=1100,
        server_updated_at_epoch_ms=1200,
        conflict_policy_ref="policy://mobile_sync_conflict_default",
    )

    with pytest.raises(ValueError, match="mutates_records must be False"):
        MobileSyncConflictContract(
            conflict_id="bad_conflict_003",
            memory_domain=base.memory_domain,
            local_record_ref=base.local_record_ref,
            server_record_ref=base.server_record_ref,
            local_sequence=base.local_sequence,
            server_sequence=base.server_sequence,
            local_updated_at_epoch_ms=base.local_updated_at_epoch_ms,
            server_updated_at_epoch_ms=base.server_updated_at_epoch_ms,
            conflict_policy_ref=base.conflict_policy_ref,
            decision=base.decision,
            decision_reason=base.decision_reason,
            deterministic_evidence_hash=base.deterministic_evidence_hash,
            deterministic_decision_required=True,
            mutates_records=True,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
        )
