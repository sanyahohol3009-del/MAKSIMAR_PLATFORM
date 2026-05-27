import pytest

from MAKSIMAR_CORE_LIB.chat_command.openim_reference_adapter_contract import (
    OpenIMReferenceAdapterContract,
    build_research_only_messenger_reference,
)


def test_openim_reference_adapter_contract_smoke() -> None:
    adapter = build_research_only_messenger_reference(
        adapter_id="openim_ref_001",
        adapter_name="OpenIM",
        upstream_project_ref="external://openim/reference-only",
    )

    assert adapter.adapter_state == "reference_only"
    assert adapter.adapter_role == "research_only"
    assert adapter.chat_truth_source_id == "MAKSIMAR_CHAT_COMMAND_TRUTH"
    assert adapter.runtime_execution_allowed is False
    assert adapter.source_of_truth_allowed is False


def test_openim_reference_adapter_rejects_runtime_execution() -> None:
    with pytest.raises(ValueError, match="runtime_execution_allowed must be False"):
        OpenIMReferenceAdapterContract(
            adapter_id="openim_bad",
            adapter_name="OpenIM",
            upstream_project_ref="external://openim/reference-only",
            adapter_state="adapter_contract_declared",
            adapter_role="runtime_adapter_candidate",
            chat_truth_source_id="MAKSIMAR_CHAT_COMMAND_TRUTH",
            quarantine_required=True,
            policy_gate_required=True,
            external_download_allowed=False,
            runtime_execution_allowed=True,
            source_of_truth_allowed=False,
            direct_command_execution_allowed=False,
            core_import_allowed=False,
            network_access_allowed=False,
        )
