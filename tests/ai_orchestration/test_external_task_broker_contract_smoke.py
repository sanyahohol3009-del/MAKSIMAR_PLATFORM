from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.external_task_broker_contract import (
    EXTERNAL_TASK_BROKER_FORBIDDEN_CAPABILITIES,
    EXTERNAL_TASK_BROKER_IDS,
    EXTERNAL_TASK_BROKER_MODES,
    EXTERNAL_TASK_BROKER_TASK_CATEGORIES,
    ExternalTaskBrokerBinding,
    assert_external_broker_not_executor,
    build_external_task_broker_contract,
    is_external_broker_allowed,
)


def test_external_task_broker_contract_declares_codex_and_gemini_only() -> None:
    read_model = build_external_task_broker_contract().to_read_model()

    assert read_model["broker_ids"] == ("codex", "gemini")
    assert read_model["broker_ids"] == EXTERNAL_TASK_BROKER_IDS
    assert read_model["broker_modes"] == EXTERNAL_TASK_BROKER_MODES
    assert read_model["allowed_task_categories"] == EXTERNAL_TASK_BROKER_TASK_CATEGORIES
    assert read_model["forbidden_capabilities"] == EXTERNAL_TASK_BROKER_FORBIDDEN_CAPABILITIES


def test_external_task_brokers_are_proposal_only_and_gated() -> None:
    read_model = build_external_task_broker_contract().to_read_model()

    for broker in read_model["brokers"]:
        assert broker["owner_command_required"] is True
        assert broker["approval_required"] is True
        assert broker["audit_required"] is True
        assert broker["preview_required"] is True
        assert broker["allowlist_required"] is True
        assert broker["proposal_only"] is True
        assert broker["direct_execution_allowed"] is False
        assert broker["local_mutation_allowed"] is False
        assert broker["runtime_start_allowed"] is False
        assert broker["model_download_allowed"] is False
        assert broker["pc_control_allowed"] is False


def test_invalid_broker_id_and_dangerous_flags_raise() -> None:
    with pytest.raises(ValueError, match="broker_id"):
        is_external_broker_allowed("")
    with pytest.raises(ValueError, match="unsupported external task broker"):
        assert_external_broker_not_executor("unknown")
    with pytest.raises(ValueError, match="must remain disabled"):
        ExternalTaskBrokerBinding(
            broker_id="codex",
            broker_modes=EXTERNAL_TASK_BROKER_MODES,
            allowed_task_categories=EXTERNAL_TASK_BROKER_TASK_CATEGORIES,
            forbidden_capabilities=EXTERNAL_TASK_BROKER_FORBIDDEN_CAPABILITIES,
            direct_execution_allowed=True,
        )
    with pytest.raises(ValueError, match="must remain required"):
        ExternalTaskBrokerBinding(
            broker_id="codex",
            broker_modes=EXTERNAL_TASK_BROKER_MODES,
            allowed_task_categories=EXTERNAL_TASK_BROKER_TASK_CATEGORIES,
            forbidden_capabilities=EXTERNAL_TASK_BROKER_FORBIDDEN_CAPABILITIES,
            approval_required=False,
        )

