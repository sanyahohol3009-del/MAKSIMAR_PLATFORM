from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.offline_import_gate_contract import (
    OfflineImportCandidate,
    OfflineImportGateDecisionReadModel,
    evaluate_offline_import_gate,
)


OFFLINE_IMPORT_GATE_RUNTIME_ID = "offline_import_gate_runtime_v1"


@dataclass(frozen=True, slots=True)
class OfflineImportGateRuntimeResult:
    runtime_id: str
    import_id: str
    package_id: str
    decision: OfflineImportGateDecisionReadModel
    wrapper_only: bool
    runtime_apply_allowed: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.runtime_id != OFFLINE_IMPORT_GATE_RUNTIME_ID:
            raise ValueError("runtime_id must be offline_import_gate_runtime_v1")
        _validate_non_empty("import_id", self.import_id)
        _validate_non_empty("package_id", self.package_id)
        if not isinstance(self.decision, OfflineImportGateDecisionReadModel):
            raise TypeError("decision must be OfflineImportGateDecisionReadModel")
        if not self.wrapper_only:
            raise ValueError("wrapper_only must remain true")
        _validate_runtime_safety_flags(
            runtime_apply_allowed=self.runtime_apply_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_execution_allowed=self.dashboard_execution_allowed,
        )
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_id": self.runtime_id,
            "import_id": self.import_id,
            "package_id": self.package_id,
            "decision": self.decision.to_dict(),
            "wrapper_only": self.wrapper_only,
            "runtime_apply_allowed": self.runtime_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "reason_codes": self.reason_codes,
        }


def run_offline_import_gate(
    candidate: OfflineImportCandidate,
) -> OfflineImportGateRuntimeResult:
    if not isinstance(candidate, OfflineImportCandidate):
        raise TypeError("candidate must be OfflineImportCandidate")

    decision = evaluate_offline_import_gate(candidate)
    return OfflineImportGateRuntimeResult(
        runtime_id=OFFLINE_IMPORT_GATE_RUNTIME_ID,
        import_id=candidate.import_id,
        package_id=candidate.package_id,
        decision=decision,
        wrapper_only=True,
        runtime_apply_allowed=False,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        reason_codes=("offline_import_gate_runtime_wrapped_contract",),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        _validate_non_empty("reason_code", reason_code)


def _validate_runtime_safety_flags(
    *,
    runtime_apply_allowed: bool,
    canonical_write_allowed: bool,
    dashboard_execution_allowed: bool,
) -> None:
    if runtime_apply_allowed:
        raise ValueError("runtime_apply_allowed must remain false")
    if canonical_write_allowed:
        raise ValueError("canonical_write_allowed must remain false")
    if dashboard_execution_allowed:
        raise ValueError("dashboard_execution_allowed must remain false")
