from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_content_models import (
    PanelContentContract,
    PanelContentEntry,
)


def test_panel_content_entry_smoke() -> None:
    entry = PanelContentEntry(
        panel_id="system_status",
        content_contract_name="system_status_panel_content_contract",
        content_kind="summary",
        content_scope="foundation",
        read_only=True,
        description="Content description.",
    )

    assert entry.panel_id == "system_status"


def test_panel_content_contract_rejects_duplicates() -> None:
    entry_a = PanelContentEntry(
        panel_id="system_status",
        content_contract_name="system_status_panel_content_contract",
        content_kind="summary",
        content_scope="foundation",
        read_only=True,
        description="A",
    )
    entry_b = PanelContentEntry(
        panel_id="system_status",
        content_contract_name="system_status_panel_content_contract",
        content_kind="summary",
        content_scope="foundation",
        read_only=True,
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate panel_id detected"):
        PanelContentContract(entries=(entry_a, entry_b))
