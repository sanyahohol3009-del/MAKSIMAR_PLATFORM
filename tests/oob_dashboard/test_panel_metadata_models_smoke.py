from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_models import (
    PanelMetadataContract,
    PanelMetadataEntry,
)


def test_panel_metadata_entry_smoke() -> None:
    entry = PanelMetadataEntry(
        panel_id="system_status",
        title="System Status",
        short_label="Status",
        description="Runtime health visibility.",
        panel_family="foundation",
        panel_kind="status",
        default_visible=True,
        operator_visible=True,
    )

    assert entry.panel_id == "system_status"
    assert entry.short_label == "Status"


def test_panel_metadata_entry_rejects_empty_title() -> None:
    with pytest.raises(ValueError, match="title must not be empty"):
        PanelMetadataEntry(
            panel_id="system_status",
            title="",
            short_label="Status",
            description="Runtime health visibility.",
            panel_family="foundation",
            panel_kind="status",
            default_visible=True,
            operator_visible=True,
        )


def test_panel_metadata_entry_rejects_empty_short_label() -> None:
    with pytest.raises(ValueError, match="short_label must not be empty"):
        PanelMetadataEntry(
            panel_id="system_status",
            title="System Status",
            short_label="",
            description="Runtime health visibility.",
            panel_family="foundation",
            panel_kind="status",
            default_visible=True,
            operator_visible=True,
        )


def test_panel_metadata_contract_rejects_duplicate_short_labels() -> None:
    entry_a = PanelMetadataEntry(
        panel_id="system_status",
        title="System Status",
        short_label="Status",
        description="Runtime health visibility.",
        panel_family="foundation",
        panel_kind="status",
        default_visible=True,
        operator_visible=True,
    )
    entry_b = PanelMetadataEntry(
        panel_id="guard_chain",
        title="Guard Chain",
        short_label="Status",
        description="Guard chain visibility.",
        panel_family="foundation",
        panel_kind="guard",
        default_visible=True,
        operator_visible=True,
    )

    with pytest.raises(ValueError, match="duplicate short_label detected"):
        PanelMetadataContract(entries=(entry_a, entry_b))
