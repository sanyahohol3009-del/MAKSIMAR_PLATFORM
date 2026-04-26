from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_vocabulary_models import (
    PanelVocabularyContract,
    PanelVocabularyEntry,
)


def test_panel_vocabulary_entry_smoke() -> None:
    entry = PanelVocabularyEntry(
        panel_id="system_status",
        title="System Status",
        description="Runtime health visibility.",
        panel_family="foundation",
        panel_kind="status",
        display_priority=0,
    )

    assert entry.panel_id == "system_status"
    assert entry.title == "System Status"


def test_panel_vocabulary_entry_rejects_empty_title() -> None:
    with pytest.raises(ValueError, match="title must not be empty"):
        PanelVocabularyEntry(
            panel_id="system_status",
            title="",
            description="Runtime health visibility.",
            panel_family="foundation",
            panel_kind="status",
            display_priority=0,
        )


def test_panel_vocabulary_entry_rejects_empty_description() -> None:
    with pytest.raises(ValueError, match="description must not be empty"):
        PanelVocabularyEntry(
            panel_id="system_status",
            title="System Status",
            description="",
            panel_family="foundation",
            panel_kind="status",
            display_priority=0,
        )


def test_panel_vocabulary_entry_rejects_negative_priority() -> None:
    with pytest.raises(ValueError, match="display_priority must be >= 0"):
        PanelVocabularyEntry(
            panel_id="system_status",
            title="System Status",
            description="Runtime health visibility.",
            panel_family="foundation",
            panel_kind="status",
            display_priority=-1,
        )


def test_panel_vocabulary_contract_rejects_duplicate_ids() -> None:
    entry_a = PanelVocabularyEntry(
        panel_id="system_status",
        title="System Status",
        description="Runtime health visibility.",
        panel_family="foundation",
        panel_kind="status",
        display_priority=0,
    )
    entry_b = PanelVocabularyEntry(
        panel_id="system_status",
        title="System Status Copy",
        description="Duplicate id example.",
        panel_family="foundation",
        panel_kind="status",
        display_priority=1,
    )

    with pytest.raises(ValueError, match="duplicate panel_id detected"):
        PanelVocabularyContract(entries=(entry_a, entry_b))


def test_panel_vocabulary_contract_rejects_duplicate_priorities() -> None:
    entry_a = PanelVocabularyEntry(
        panel_id="system_status",
        title="System Status",
        description="Runtime health visibility.",
        panel_family="foundation",
        panel_kind="status",
        display_priority=0,
    )
    entry_b = PanelVocabularyEntry(
        panel_id="guard_chain",
        title="Guard Chain",
        description="Guard chain visibility.",
        panel_family="foundation",
        panel_kind="guard",
        display_priority=0,
    )

    with pytest.raises(
        ValueError, match="display_priority values must be unique"
    ):
        PanelVocabularyContract(entries=(entry_a, entry_b))
