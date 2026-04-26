from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.test_warning_cleanup_policy_contract import (
    WarningCleanupPolicyEntry,
    build_test_warning_cleanup_policy_contract,
)


def test_test_warning_cleanup_policy_contract_builds() -> None:
    contract = build_test_warning_cleanup_policy_contract()

    assert contract.contract_id == "test_warning_cleanup_policy_contract_001"
    assert contract.total_entries == 3
    assert contract.cleanup_required_entries == 3
    assert contract.xdist_sensitive_entries == 2
    assert contract.owner_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_test_warning_cleanup_policy_contract_contains_expected_scopes() -> None:
    contract = build_test_warning_cleanup_policy_contract()

    values = tuple(
        (entry.policy_entry_id, entry.warning_scope, entry.warning_class)
        for entry in contract.entries
    )

    assert values == (
        (
            "test_warning_cleanup_policy_001",
            "benchmark_xdist_parallel_warning",
            "PytestBenchmarkWarning",
        ),
        (
            "test_warning_cleanup_policy_002",
            "multiprocessing_fork_deprecation_warning",
            "DeprecationWarning",
        ),
        (
            "test_warning_cleanup_policy_003",
            "suite_warning_cluster_cleanup",
            "WarningClusterSummary",
        ),
    )


def test_test_warning_cleanup_policy_entry_rejects_non_cleanup_mode() -> None:
    with pytest.raises(
        ValueError,
        match="cleanup_required must remain true for canonical warning cleanup policy entries.",
    ):
        WarningCleanupPolicyEntry(
            policy_entry_id="bad_warning_policy",
            warning_scope="bad_scope",
            warning_class="BadWarning",
            cleanup_required=False,
            xdist_sensitive=False,
            owner_visible=True,
            truth_bound=True,
            description="Invalid warning cleanup entry.",
        )
