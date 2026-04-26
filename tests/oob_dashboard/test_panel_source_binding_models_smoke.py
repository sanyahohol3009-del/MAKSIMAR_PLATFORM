from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_source_binding_models import (
    PanelSourceBindingContract,
    PanelSourceBindingEntry,
)


def test_panel_source_binding_entry_smoke() -> None:
    entry = PanelSourceBindingEntry(
        panel_id="system_status",
        source_binding="runtime_summary",
        source_contract_name="system_status_panel_content_contract",
        source_scope="foundation",
        read_only=True,
        description="Source binding description.",
    )

    assert entry.panel_id == "system_status"


def test_panel_source_binding_contract_rejects_duplicates() -> None:
    entry_a = PanelSourceBindingEntry(
        panel_id="system_status",
        source_binding="runtime_summary",
        source_contract_name="system_status_panel_content_contract",
        source_scope="foundation",
        read_only=True,
        description="A",
    )
    entry_b = PanelSourceBindingEntry(
        panel_id="system_status",
        source_binding="runtime_summary",
        source_contract_name="system_status_panel_content_contract",
        source_scope="foundation",
        read_only=True,
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate panel_id detected"):
        PanelSourceBindingContract(entries=(entry_a, entry_b))
