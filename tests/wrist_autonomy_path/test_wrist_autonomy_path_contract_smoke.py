from __future__ import annotations

from MAKSIMAR_CORE_LIB.wrist_autonomy_path import (
    build_wrist_autonomy_path_contract,
)


def test_wrist_autonomy_path_contract_builds() -> None:
    """Wrist autonomy path contract should build successfully."""
    contract = build_wrist_autonomy_path_contract()

    assert contract.total_entries == 3
    assert contract.local_inference_entries == 2
    assert contract.remote_heavy_compute_entries == 2
    assert contract.autonomous_stage_entries == 1
    assert contract.defined_entries == 3


def test_wrist_autonomy_path_contract_contains_expected_stage_1() -> None:
    """Wrist autonomy path should expose expected stage 1 entry."""
    contract = build_wrist_autonomy_path_contract()
    entry = contract.entries[0]

    assert entry.autonomy_stage == "stage_1_thin_client"
    assert entry.compute_placement == "remote_heavy_compute"
    assert entry.inference_mode == "remote_only"
    assert entry.execution_authority == "remote_authority"
    assert entry.local_inference_required is False
    assert entry.remote_heavy_compute_allowed is True


def test_wrist_autonomy_path_contract_contains_expected_stage_2() -> None:
    """Wrist autonomy path should expose expected stage 2 entry."""
    contract = build_wrist_autonomy_path_contract()
    entry = contract.entries[1]

    assert entry.autonomy_stage == "stage_2_hybrid_inference"
    assert entry.compute_placement == "hybrid_local_and_remote"
    assert entry.inference_mode == "hybrid_inference"
    assert entry.execution_authority == "shared_authority"
    assert entry.local_inference_required is True
    assert entry.remote_heavy_compute_allowed is True


def test_wrist_autonomy_path_contract_contains_expected_stage_3() -> None:
    """Wrist autonomy path should expose expected stage 3 entry."""
    contract = build_wrist_autonomy_path_contract()
    entry = contract.entries[2]

    assert entry.autonomy_stage == "stage_3_autonomous_node"
    assert entry.compute_placement == "local_primary_compute"
    assert entry.inference_mode == "local_inference"
    assert entry.execution_authority == "local_authority_with_policy"
    assert entry.local_inference_required is True
    assert entry.remote_heavy_compute_allowed is False
