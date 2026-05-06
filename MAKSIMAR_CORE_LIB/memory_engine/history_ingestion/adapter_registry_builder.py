from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.adapter_registry_models import (
    AdapterRegistry,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.html_adapter import (
    build_html_adapter_capability,
    build_html_adapter_protocol,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.json_adapter import (
    build_json_adapter_capability,
    build_json_adapter_protocol,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.md_adapter import (
    build_md_adapter_capability,
    build_md_adapter_protocol,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.pdf_adapter import (
    build_pdf_adapter_capability,
    build_pdf_adapter_protocol,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.source_type_models import (
    ArchiveSourceType,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.txt_adapter import (
    build_txt_adapter_capability,
    build_txt_adapter_protocol,
)


def build_default_adapter_registry() -> AdapterRegistry:
    return AdapterRegistry(
        capabilities=(
            build_html_adapter_capability(),
            build_pdf_adapter_capability(),
            build_txt_adapter_capability(),
            build_md_adapter_capability(),
            build_json_adapter_capability(),
        ),
        protocols=(
            build_html_adapter_protocol(),
            build_pdf_adapter_protocol(),
            build_txt_adapter_protocol(),
            build_md_adapter_protocol(),
            build_json_adapter_protocol(),
        ),
    )


def build_adapter_registry_preview() -> Dict[str, object]:
    registry = build_default_adapter_registry()
    return {
        "supported_source_type_matrix": registry.supported_source_type_matrix,
        "parallel_safe_registry": registry.parallel_safe_registry,
        "deterministic_registry": registry.deterministic_registry,
        "adapter_index": registry.as_index(),
    }


def build_format_selection_preview(
    source_type: ArchiveSourceType,
) -> Dict[str, object]:
    registry = build_default_adapter_registry()
    capability = registry.get_capability_for_source_type(source_type)
    protocol = registry.get_protocol_for_source_type(source_type)

    return {
        "source_type": source_type,
        "selected_adapter_id": capability.adapter_id,
        "text_first_input": capability.text_first_input,
        "binary_input_supported": capability.binary_input_supported,
        "deterministic_output_required": capability.deterministic_output_required,
        "parallel_safe_by_design": capability.parallel_safe_by_design,
        "required_output_kinds": protocol.required_output_kinds,
        "selection_ready": True,
    }
