import pytest

from shared_mobile_core.mobile_sync_models.mobile_sync_envelope_contract import MobileSyncEnvelopeContract


def test_mobile_sync_envelope_accepts_app_and_chat_refs_only() -> None:
    app_envelope = MobileSyncEnvelopeContract.for_app_memory(
        envelope_id="sync_env_app_001",
        source_device_id="device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        record_refs=("app-memory://device_001/records/app-record-001",),
        cursor_ref="cursor://device_001/app_memory/1",
        policy_ref="policy://mobile_sync_default",
        audit_ref="audit://sync_env_app_001",
    )
    chat_envelope = MobileSyncEnvelopeContract.for_chat_memory(
        envelope_id="sync_env_chat_001",
        source_device_id="device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        record_refs=("chat-memory://device_001/records/chat-record-001",),
        cursor_ref="cursor://device_001/chat_memory/1",
        policy_ref="policy://mobile_sync_default",
        audit_ref="audit://sync_env_chat_001",
    )

    assert app_envelope.reference_only is True
    assert chat_envelope.reference_only is True
    assert app_envelope.core_write_allowed is False
    assert chat_envelope.direct_server_write_allowed is False
    assert app_envelope.network_allowed is False
    assert chat_envelope.socket_allowed is False
    assert app_envelope.mutates_app_memory_store is False
    assert chat_envelope.mutates_chat_memory_store is False


def test_mobile_sync_envelope_rejects_inline_payload_and_wrong_domain_refs() -> None:
    with pytest.raises(ValueError, match="inline_payload_present must be False"):
        MobileSyncEnvelopeContract(
            envelope_id="bad_payload_env",
            memory_domain="app_memory",
            source_device_id="device_001",
            app_id="maksimar_mobile",
            owner_identity_id="owner_001",
            record_refs=("app-memory://device_001/records/app-record-001",),
            cursor_ref="cursor://device_001/app_memory/1",
            policy_ref="policy://mobile_sync_default",
            audit_ref="audit://bad_payload_env",
            idempotency_key="bad_payload_env:app_memory:device_001",
            reference_only=True,
            inline_payload_present=True,
            message_body_present=False,
            heavy_payload_present=False,
            embedded_secret_present=False,
            embedded_key_material_present=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            canonical_truth_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )

    with pytest.raises(ValueError, match="record_ref must start with"):
        MobileSyncEnvelopeContract.for_app_memory(
            envelope_id="bad_ref_env",
            source_device_id="device_001",
            app_id="maksimar_mobile",
            owner_identity_id="owner_001",
            record_refs=("chat-memory://device_001/records/chat-record-001",),
            cursor_ref="cursor://device_001/app_memory/1",
            policy_ref="policy://mobile_sync_default",
            audit_ref="audit://bad_ref_env",
        )


def test_mobile_sync_envelope_read_model_has_no_payload_fields() -> None:
    envelope = MobileSyncEnvelopeContract.for_chat_memory(
        envelope_id="sync_env_chat_002",
        source_device_id="device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        record_refs=("chat-memory://device_001/records/chat-record-002",),
        cursor_ref="cursor://device_001/chat_memory/2",
        policy_ref="policy://mobile_sync_default",
        audit_ref="audit://sync_env_chat_002",
    )

    read_model = envelope.to_read_model()

    assert "payload" not in read_model
    assert "message_body" not in read_model
    assert read_model["reference_only"] is True
    assert read_model["direct_server_write_allowed"] is False
