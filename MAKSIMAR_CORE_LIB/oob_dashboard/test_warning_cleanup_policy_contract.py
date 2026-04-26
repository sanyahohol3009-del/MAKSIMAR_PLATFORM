from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class WarningCleanupPolicyEntry:
    policy_entry_id: str
    warning_scope: str
    warning_class: str
    cleanup_required: bool
    xdist_sensitive: bool
    owner_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.policy_entry_id, "policy_entry_id")
        _require_non_empty(self.warning_scope, "warning_scope")
        _require_non_empty(self.warning_class, "warning_class")
        _require_non_empty(self.description, "description")

        if not self.cleanup_required:
            raise ValueError(
                "cleanup_required must remain true for canonical warning cleanup policy entries."
            )
        if not self.owner_visible:
            raise ValueError(
                "owner_visible must remain true for canonical warning cleanup policy entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical warning cleanup policy entries."
            )


@dataclass(frozen=True, slots=True)
class WarningCleanupPolicyContract:
    contract_id: str
    total_entries: int
    cleanup_required_entries: int
    xdist_sensitive_entries: int
    owner_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[WarningCleanupPolicyEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.cleanup_required_entries != sum(
            1 for entry in self.entries if entry.cleanup_required
        ):
            raise ValueError(
                "cleanup_required_entries must match cleanup_required count."
            )
        if self.xdist_sensitive_entries != sum(
            1 for entry in self.entries if entry.xdist_sensitive
        ):
            raise ValueError(
                "xdist_sensitive_entries must match xdist_sensitive count."
            )
        if self.owner_visible_entries != sum(
            1 for entry in self.entries if entry.owner_visible
        ):
            raise ValueError(
                "owner_visible_entries must match owner_visible count."
            )
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_test_warning_cleanup_policy_contract() -> WarningCleanupPolicyContract:
    entries = (
        WarningCleanupPolicyEntry(
            policy_entry_id="test_warning_cleanup_policy_001",
            warning_scope="benchmark_xdist_parallel_warning",
            warning_class="PytestBenchmarkWarning",
            cleanup_required=True,
            xdist_sensitive=True,
            owner_visible=True,
            truth_bound=True,
            description="Canonical cleanup policy for benchmark warnings under xdist.",
        ),
        WarningCleanupPolicyEntry(
            policy_entry_id="test_warning_cleanup_policy_002",
            warning_scope="multiprocessing_fork_deprecation_warning",
            warning_class="DeprecationWarning",
            cleanup_required=True,
            xdist_sensitive=True,
            owner_visible=True,
            truth_bound=True,
            description="Canonical cleanup policy for multiprocessing fork deprecation warnings.",
        ),
        WarningCleanupPolicyEntry(
            policy_entry_id="test_warning_cleanup_policy_003",
            warning_scope="suite_warning_cluster_cleanup",
            warning_class="WarningClusterSummary",
            cleanup_required=True,
            xdist_sensitive=False,
            owner_visible=True,
            truth_bound=True,
            description="Canonical cleanup policy for repeated suite warning clusters.",
        ),
    )

    return WarningCleanupPolicyContract(
        contract_id="test_warning_cleanup_policy_contract_001",
        total_entries=len(entries),
        cleanup_required_entries=sum(1 for entry in entries if entry.cleanup_required),
        xdist_sensitive_entries=sum(1 for entry in entries if entry.xdist_sensitive),
        owner_visible_entries=sum(1 for entry in entries if entry.owner_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
