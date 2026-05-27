from MAKSIMAR_CORE_LIB.chat_command.openim_reference_adapter_contract import build_research_only_messenger_reference


def test_spika_matrix_research_only_until_acceptance_smoke() -> None:
    references = (
        build_research_only_messenger_reference(
            adapter_id="spika_ref_001",
            adapter_name="Spika",
            upstream_project_ref="external://spika/reference-only",
        ),
        build_research_only_messenger_reference(
            adapter_id="matrix_ref_001",
            adapter_name="Matrix",
            upstream_project_ref="external://matrix/reference-only",
        ),
    )

    for reference in references:
        assert reference.adapter_role == "research_only"
        assert reference.external_download_allowed is False
        assert reference.runtime_execution_allowed is False
        assert reference.source_of_truth_allowed is False
        assert reference.core_import_allowed is False
        assert reference.network_access_allowed is False
