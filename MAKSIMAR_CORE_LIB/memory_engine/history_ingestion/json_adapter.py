from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.adapter_base import (
    ArchiveAdapterCapability,
    ArchiveAdapterProtocolContract,
)


def build_json_adapter_capability() -> ArchiveAdapterCapability:
    return ArchiveAdapterCapability(
        adapter_id="HADAPTER-JSON-001",
        source_type="json",
        text_first_input=True,
        binary_input_supported=False,
        deterministic_output_required=True,
        parallel_safe_by_design=True,
    )


def build_json_adapter_protocol() -> ArchiveAdapterProtocolContract:
    return ArchiveAdapterProtocolContract(
        adapter_name="json_adapter",
        supported_source_type="json",
        required_output_kinds=("raw_document", "structured_text"),
        stateless_adapter_required=True,
        side_effect_free_selection_required=True,
    )
