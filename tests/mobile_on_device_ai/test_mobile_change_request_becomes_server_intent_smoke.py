from __future__ import annotations

from shared_mobile_core.intent_parser.mobile_intent_parser_contract import (
    build_mobile_intent_parser_contract,
)


def test_mobile_change_request_becomes_server_intent_only() -> None:
    read_model = build_mobile_intent_parser_contract().to_read_model()

    assert read_model["mobile_change_request_becomes_server_intent"] is True
    assert read_model["server_jARVIS_remains_senior_authority"] is True
    assert read_model["direct_execution_allowed"] is False
    assert read_model["canonical_mutation_allowed"] is False
    assert read_model["deployment_allowed"] is False
