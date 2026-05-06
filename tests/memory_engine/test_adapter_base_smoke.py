from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.adapter_base import (
    ArchiveAdapterCapability,
    ArchiveAdapterProtocolContract,
)


def test_adapter_base_smoke() -> None:
    capability = ArchiveAdapterCapability(
        adapter_id="HADAPTER-HTML-001",
        source_type="html",
        text_first_input=True,
        binary_input_supported=False,
        deterministic_output_required=True,
        parallel_safe_by_design=True,
    )
    protocol = ArchiveAdapterProtocolContract(
        adapter_name="html_adapter",
        supported_source_type="html",
        required_output_kinds=("raw_document", "structured_text"),
        stateless_adapter_required=True,
        side_effect_free_selection_required=True,
    )

    assert capability.adapter_id == "HADAPTER-HTML-001"
    assert protocol.adapter_name == "html_adapter"


def test_adapter_capability_rejects_non_deterministic_contract() -> None:
    with pytest.raises(ValueError, match="deterministic_output_required must be True"):
        ArchiveAdapterCapability(
            adapter_id="BAD-001",
            source_type="html",
            text_first_input=True,
            binary_input_supported=False,
            deterministic_output_required=False,
            parallel_safe_by_design=True,
        )


def test_adapter_protocol_rejects_empty_output_kinds() -> None:
    with pytest.raises(ValueError, match="required_output_kinds must not be empty"):
        ArchiveAdapterProtocolContract(
            adapter_name="bad_adapter",
            supported_source_type="txt",
            required_output_kinds=(),
            stateless_adapter_required=True,
            side_effect_free_selection_required=True,
        )
