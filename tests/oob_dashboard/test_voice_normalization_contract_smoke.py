from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.voice_normalization_contract import (
    VoiceNormalizationEntry,
    build_voice_normalization_contract,
)


def test_voice_normalization_contract_builds() -> None:
    contract = build_voice_normalization_contract()
    assert contract.contract_id == "voice_normalization_contract_001"
    assert contract.total_entries == 3
    assert contract.normalized_entries == 3
    assert contract.valid_entries == 3
    assert contract.guarded_entries == 3


def test_voice_normalization_rejects_direct_execution() -> None:
    with pytest.raises(
        ValueError,
        match="direct_execution_allowed must remain false for canonical voice normalization entries.",
    ):
        VoiceNormalizationEntry(
            normalization_entry_id="bad_voice_normalization",
            raw_command_id="raw_voice_bad",
            voice_command_kind="voice_navigation_command",
            transcript_normalized=True,
            structurally_valid=True,
            direct_execution_allowed=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid voice normalization entry.",
        )
