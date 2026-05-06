from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.adapter_base import (
    ArchiveAdapterCapability,
    ArchiveAdapterProtocolContract,
)


def build_pdf_adapter_capability() -> ArchiveAdapterCapability:
    return ArchiveAdapterCapability(
        adapter_id="HADAPTER-PDF-001",
        source_type="pdf",
        text_first_input=False,
        binary_input_supported=True,
        deterministic_output_required=True,
        parallel_safe_by_design=True,
    )


def build_pdf_adapter_protocol() -> ArchiveAdapterProtocolContract:
    return ArchiveAdapterProtocolContract(
        adapter_name="pdf_adapter",
        supported_source_type="pdf",
        required_output_kinds=("raw_document", "binary_document"),
        stateless_adapter_required=True,
        side_effect_free_selection_required=True,
    )
