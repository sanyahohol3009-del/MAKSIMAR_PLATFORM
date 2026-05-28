from shared_mobile_core.chat_memory import ChatMemoryStoreContract


def test_chat_memory_store_contract_is_shell_adapter_only() -> None:
    store = ChatMemoryStoreContract.default_mobile_chat_store(
        store_id="chat-store-1",
        device_id="device-1",
        app_id="maksimar-mobile",
        owner_identity_id="owner-1",
    )

    assert store.encrypted_at_rest_required is True
    assert store.retention_required is True
    assert store.offline_first is True
    assert store.shell_adapter_only is True
    assert store.openim_truth is False
    assert store.core_chat_truth is False
    assert store.canonical_truth is False
    assert store.core_write_allowed is False
    assert store.direct_server_write_allowed is False
    assert store.supported_record_kinds
