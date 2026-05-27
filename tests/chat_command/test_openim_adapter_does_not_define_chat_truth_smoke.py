import pytest

from MAKSIMAR_CORE_LIB.chat_command.openim_reference_adapter_contract import OpenIMReferenceAdapterContract


def test_openim_adapter_does_not_define_chat_truth_smoke() -> None:
    with pytest.raises(ValueError, match="source_of_truth_allowed must be False"):
        OpenIMReferenceAdapterContract(
            adapter_id="openim_truth_bad",
            adapter_name="OpenIM",
            upstream_project_ref="external://openim/reference-only",
            adapter_state="reference_only",
            adapter_role="message_transport_reference",
            chat_truth_source_id="MAKSIMAR_CHAT_COMMAND_TRUTH",
            quarantine_required=True,
            policy_gate_required=True,
            external_download_allowed=False,
            runtime_execution_allowed=False,
            source_of_truth_allowed=True,
            direct_command_execution_allowed=False,
            core_import_allowed=False,
            network_access_allowed=False,
        )


def test_openim_adapter_must_bind_to_maksimar_chat_truth() -> None:
    with pytest.raises(ValueError, match="chat_truth_source_id must remain MAKSIMAR_CHAT_COMMAND_TRUTH"):
        OpenIMReferenceAdapterContract(
            adapter_id="openim_wrong_truth",
            adapter_name="OpenIM",
            upstream_project_ref="external://openim/reference-only",
            adapter_state="reference_only",
            adapter_role="message_transport_reference",
            chat_truth_source_id="OPENIM_TRUTH",
            quarantine_required=True,
            policy_gate_required=True,
            external_download_allowed=False,
            runtime_execution_allowed=False,
            source_of_truth_allowed=False,
            direct_command_execution_allowed=False,
            core_import_allowed=False,
            network_access_allowed=False,
        )
