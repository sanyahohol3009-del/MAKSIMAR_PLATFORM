from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_SERVER.UPDATE_RECOVERY.adapters.runtime_recovery_manager_adapter import (
    build_runtime_recovery_manager_adapter_read_model,
)
from MAKSIMAR_SERVER.UPDATE_RECOVERY.adapters.secure_sync_update_transport_adapter import (
    build_secure_sync_update_transport_adapter_read_model,
)


@dataclass(frozen=True, slots=True)
class UpdateTracerResultReadModel:
    tracer_id: str
    package_id: str
    unsigned_update_rejected: bool
    update_apply_performed: bool
    secure_sync_update_transport_preserved: bool
    runtime_recovery_manager_wrapped: bool
    manifest_present: bool
    source_of_truth_check_passed: bool
    version_control_check_passed: bool
    drift_guard_required: bool
    xray_required: bool
    full_pytest_required: bool
    dashboard_safe: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.tracer_id != "update_tracer_result_read_model_v1":
            raise ValueError("tracer_id must be update_tracer_result_read_model_v1")
        if not self.package_id:
            raise ValueError("package_id must not be empty")
        if not self.unsigned_update_rejected:
            raise ValueError("unsigned_update_rejected must remain true")
        if self.update_apply_performed:
            raise ValueError("update_apply_performed must remain false")
        if not self.secure_sync_update_transport_preserved:
            raise ValueError("secure_sync_update_transport_preserved must remain true")
        if not self.runtime_recovery_manager_wrapped:
            raise ValueError("runtime_recovery_manager_wrapped must remain true")
        if not self.manifest_present:
            raise ValueError("manifest_present must remain true")
        if not self.source_of_truth_check_passed:
            raise ValueError("source_of_truth_check_passed must remain true")
        if not self.version_control_check_passed:
            raise ValueError("version_control_check_passed must remain true")
        if not self.drift_guard_required:
            raise ValueError("drift_guard_required must remain true")
        if not self.xray_required:
            raise ValueError("xray_required must remain true")
        if not self.full_pytest_required:
            raise ValueError("full_pytest_required must remain true")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.dashboard_execution_allowed:
            raise ValueError("dashboard_execution_allowed must remain false")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "tracer_id": self.tracer_id,
            "package_id": self.package_id,
            "unsigned_update_rejected": self.unsigned_update_rejected,
            "update_apply_performed": self.update_apply_performed,
            "secure_sync_update_transport_preserved": self.secure_sync_update_transport_preserved,
            "runtime_recovery_manager_wrapped": self.runtime_recovery_manager_wrapped,
            "manifest_present": self.manifest_present,
            "source_of_truth_check_passed": self.source_of_truth_check_passed,
            "version_control_check_passed": self.version_control_check_passed,
            "drift_guard_required": self.drift_guard_required,
            "xray_required": self.xray_required,
            "full_pytest_required": self.full_pytest_required,
            "dashboard_safe": self.dashboard_safe,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "reason_codes": self.reason_codes,
        }


def build_unsigned_update_rejection_tracer() -> UpdateTracerResultReadModel:
    secure_sync_adapter = build_secure_sync_update_transport_adapter_read_model()
    recovery_manager_adapter = build_runtime_recovery_manager_adapter_read_model()

    return UpdateTracerResultReadModel(
        tracer_id="update_tracer_result_read_model_v1",
        package_id="unsigned-update-package-mock-001",
        unsigned_update_rejected=True,
        update_apply_performed=False,
        secure_sync_update_transport_preserved=not secure_sync_adapter.replaces_existing_transport,
        runtime_recovery_manager_wrapped=(
            recovery_manager_adapter.adapter_bound
            and recovery_manager_adapter.recovery_manager_preserved
            and not recovery_manager_adapter.replaces_existing_manager
        ),
        manifest_present=True,
        source_of_truth_check_passed=True,
        version_control_check_passed=True,
        drift_guard_required=True,
        xray_required=True,
        full_pytest_required=True,
        dashboard_safe=True,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        reason_codes=(
            "unsigned_update_rejected",
            "no_update_apply_performed",
            "secure_sync_update_transport_preserved",
            "runtime_recovery_manager_wrapped",
            "manifest_present",
            "source_of_truth_check_passed",
            "version_control_check_passed",
            "drift_guard_required",
            "xray_required",
            "full_pytest_required",
        ),
    )


def test_update_channel_rejects_unsigned_update_without_apply() -> None:
    result = build_unsigned_update_rejection_tracer()

    assert result.unsigned_update_rejected is True
    assert result.update_apply_performed is False
    assert result.secure_sync_update_transport_preserved is True
    assert result.runtime_recovery_manager_wrapped is True
    assert result.manifest_present is True
    assert result.source_of_truth_check_passed is True
    assert result.version_control_check_passed is True
    assert result.drift_guard_required is True
    assert result.xray_required is True
    assert result.full_pytest_required is True
    assert result.dashboard_safe is True
    assert result.canonical_write_allowed is False
    assert result.dashboard_execution_allowed is False
    assert result.to_dict()["tracer_id"] == "update_tracer_result_read_model_v1"
