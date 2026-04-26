from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.interaction_exposure_contract import (
    InteractionExposureEntry,
    build_interaction_exposure_contract,
)


def test_interaction_exposure_contract_builds() -> None:
    contract = build_interaction_exposure_contract()
    assert contract.contract_id == "interaction_exposure_contract_001"
    assert contract.total_entries == 2
    assert contract.policy_bound_entries == 2
    assert contract.guarded_entries == 2


def test_interaction_exposure_rejects_direct_execution() -> None:
    with pytest.raises(
        ValueError,
        match="direct_execution_allowed must remain false for canonical interaction exposure entries.",
    ):
        InteractionExposureEntry(
            exposure_entry_id="bad_interaction_exposure",
            interaction_source="bad_source",
            exposure_channel="bad_channel",
            policy_bound=True,
            direct_execution_allowed=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid interaction exposure entry.",
        )
