from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import build_dashboard_chat_contract


def test_dashboard_chat_contract_builds() -> None:
    """Dashboard chat contract should build successfully."""
    contract = build_dashboard_chat_contract()

    assert contract.total_messages == 3
    assert len(contract.messages) == 3
    assert contract.copy_enabled is True
    assert contract.input_enabled is True


def test_dashboard_chat_contract_contains_code_message() -> None:
    """Dashboard chat contract should contain copyable code message."""
    contract = build_dashboard_chat_contract()

    assert any(message.content_type == "code" for message in contract.messages)
    assert any(message.role == "jarvis" for message in contract.messages)
