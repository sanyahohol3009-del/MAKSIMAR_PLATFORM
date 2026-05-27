import pytest

from MAKSIMAR_CORE_LIB.chat_command.message_encryption_contract import MessageEncryptionContract


def test_message_encryption_contract_smoke() -> None:
    encryption = MessageEncryptionContract(
        encryption_id="enc_001",
        message_id="msg_001",
        encryption_mode="end_to_end_required",
        key_scope="owner_device",
        rotation_required=True,
        plaintext_storage_allowed=False,
        external_key_provider_allowed=False,
        runtime_mutation_allowed=False,
    )

    assert encryption.rotation_required is True
    assert encryption.plaintext_storage_allowed is False


def test_message_encryption_rejects_plaintext_storage() -> None:
    with pytest.raises(ValueError, match="plaintext_storage_allowed must be False"):
        MessageEncryptionContract(
            encryption_id="enc_bad",
            message_id="msg_001",
            encryption_mode="at_rest_required",
            key_scope="server_tenant",
            rotation_required=True,
            plaintext_storage_allowed=True,
            external_key_provider_allowed=False,
            runtime_mutation_allowed=False,
        )
