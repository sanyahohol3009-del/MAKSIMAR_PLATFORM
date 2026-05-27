import pytest

from MAKSIMAR_CORE_LIB.chat_command.chat_identity_contract import (
    ChatIdentityContract,
    build_owner_chat_identity,
)


def test_owner_chat_identity_contract_smoke() -> None:
    identity = build_owner_chat_identity(
        identity_id="identity_owner_001",
        display_name="Owner",
    )

    assert identity.identity_kind == "human_owner"
    assert identity.trust_level == "owner"
    assert identity.command_source_allowed is True
    assert identity.direct_execution_allowed is False


def test_external_adapter_identity_cannot_be_command_source() -> None:
    with pytest.raises(ValueError, match="external adapters must not be command sources"):
        ChatIdentityContract(
            identity_id="identity_openim_adapter",
            display_name="OpenIM Adapter",
            identity_kind="external_adapter",
            trust_level="adapter_read_only",
            command_source_allowed=True,
            direct_execution_allowed=False,
            external_adapter=True,
        )


def test_chat_identity_never_allows_direct_execution() -> None:
    with pytest.raises(ValueError, match="direct_execution_allowed must be False"):
        ChatIdentityContract(
            identity_id="identity_owner_002",
            display_name="Owner",
            identity_kind="human_owner",
            trust_level="owner",
            command_source_allowed=True,
            direct_execution_allowed=True,
        )
