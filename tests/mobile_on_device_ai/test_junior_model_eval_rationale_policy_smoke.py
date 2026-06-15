from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge.junior_model_eval_contract import (
    build_junior_model_eval_contract,
)


def test_junior_model_eval_requires_human_readable_rationale() -> None:
    read_model = build_junior_model_eval_contract().to_read_model()

    assert read_model["eval_required_before_runtime_enable"] is True
    assert read_model["eval_rationale_required"] is True
    assert read_model["eval_rationale_must_be_human_readable"] is True
    assert read_model["eval_may_not_enable_runtime"] is True
    assert read_model["eval_may_not_download_model"] is True
    assert read_model["eval_may_not_grant_core_actions"] is True
    assert read_model["owner_approval_required"] is True
