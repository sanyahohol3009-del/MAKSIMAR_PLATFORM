from __future__ import annotations

from shared_mobile_core.intent_parser.mobile_intent_parser_contract import (
    build_mobile_intent_parser_contract,
)


def test_mobile_intent_parser_contract_is_intent_only() -> None:
    read_model = build_mobile_intent_parser_contract().to_read_model()

    assert read_model["text_intent_only"] is True
    assert read_model["app_safe_only"] is True
    assert read_model["sends_to_server_as_intent_candidate"] is True
    assert read_model["local_command_execution_allowed"] is False
    assert read_model["core_action_execution_allowed"] is False
    assert read_model["direct_phone_control_allowed"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["approval_required_for_actions"] is True
    assert read_model["proposal_only"] is True
