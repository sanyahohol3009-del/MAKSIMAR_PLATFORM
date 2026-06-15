from __future__ import annotations

from shared_mobile_core.intent_parser.mobile_intent_parser_contract import (
    build_mobile_intent_parser_contract,
)
from shared_mobile_core.llm_engine.local_llm_runtime_contract import (
    build_local_llm_runtime_contract,
)


def test_mobile_junior_model_cannot_execute_core_actions() -> None:
    parser = build_mobile_intent_parser_contract().to_read_model()
    runtime = build_local_llm_runtime_contract().to_read_model()

    assert parser["mobile_junior_may_not_execute_core_actions"] is True
    assert parser["core_action_execution_allowed"] is False
    assert parser["shell_execution_allowed"] is False
    assert runtime["pc_control_allowed"] is False
    assert runtime["canonical_memory_write_allowed"] is False
    assert runtime["server_mutation_allowed"] is False
    assert parser["owner_approval_bypass_allowed"] is False
