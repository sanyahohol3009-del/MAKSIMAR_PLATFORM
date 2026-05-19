from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any

from MAKSIMAR_CORE_LIB.security_layer.security_read_model import (
    SecurityTelemetryReadModel,
)


class SecurityTracerScenarioStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class SecurityTracerGateSnapshot:
    request_id: str
    trace_id: str
    decision_status: str
    risk_level: str
    decision_allows_execution: bool
    actual_execution_performed: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name, value in (
            ("request_id", self.request_id),
            ("trace_id", self.trace_id),
            ("decision_status", self.decision_status),
            ("risk_level", self.risk_level),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")

        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")

        for reason_code in self.reason_codes:
            if not reason_code:
                raise ValueError("reason_codes must not contain empty values")

        if self.actual_execution_performed:
            raise ValueError("security tracer snapshot must not report actual execution")


@dataclass(frozen=True, slots=True)
class SecurityTracerResultReadModel:
    tracer_id: str
    scenario_id: str
    source_layer_id: str
    target_layer_id: str
    request_id: str
    trace_id: str
    decision_status: str
    risk_level: str
    action_execution_allowed: bool
    operation_blocked: bool
    actual_execution_performed: bool
    telemetry_status: str
    scenario_status: SecurityTracerScenarioStatus
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_execution_allowed: bool = False
    ui_to_execution_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("tracer_id", self.tracer_id),
            ("scenario_id", self.scenario_id),
            ("source_layer_id", self.source_layer_id),
            ("target_layer_id", self.target_layer_id),
            ("request_id", self.request_id),
            ("trace_id", self.trace_id),
            ("decision_status", self.decision_status),
            ("risk_level", self.risk_level),
            ("telemetry_status", self.telemetry_status),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if not isinstance(self.scenario_status, SecurityTracerScenarioStatus):
            raise TypeError("scenario_status must be SecurityTracerScenarioStatus")

        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")

        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")

        for reason_code in self.reason_codes:
            if not reason_code:
                raise ValueError("reason_codes must not contain empty values")

        if self.action_execution_allowed and self.operation_blocked:
            raise ValueError("allowed execution cannot be marked as blocked")

        if self.actual_execution_performed:
            raise ValueError("security tracer must not perform execution")

        if self.scenario_status is SecurityTracerScenarioStatus.PASSED:
            if not self.operation_blocked:
                raise ValueError("passed unauthorized-deny tracer requires operation_blocked=true")
            if self.action_execution_allowed:
                raise ValueError("passed unauthorized-deny tracer requires action_execution_allowed=false")

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")

        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")

        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")

        if self.ui_to_execution_allowed:
            raise ValueError("ui_to_execution_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["scenario_status"] = self.scenario_status.value
        payload["reason_codes"] = list(self.reason_codes)
        return payload


def build_security_tracer_result_read_model(
    *,
    tracer_id: str,
    scenario_id: str,
    source_layer_id: str,
    target_layer_id: str,
    gate_snapshot: SecurityTracerGateSnapshot,
    telemetry: SecurityTelemetryReadModel,
    expected_blocked: bool,
) -> SecurityTracerResultReadModel:
    if not isinstance(gate_snapshot, SecurityTracerGateSnapshot):
        raise TypeError("gate_snapshot must be SecurityTracerGateSnapshot")

    if not isinstance(telemetry, SecurityTelemetryReadModel):
        raise TypeError("telemetry must be SecurityTelemetryReadModel")

    operation_blocked = not gate_snapshot.decision_allows_execution
    scenario_passed = (
        operation_blocked is expected_blocked
        and not gate_snapshot.actual_execution_performed
    )

    return SecurityTracerResultReadModel(
        tracer_id=tracer_id,
        scenario_id=scenario_id,
        source_layer_id=source_layer_id,
        target_layer_id=target_layer_id,
        request_id=gate_snapshot.request_id,
        trace_id=gate_snapshot.trace_id,
        decision_status=gate_snapshot.decision_status,
        risk_level=gate_snapshot.risk_level,
        action_execution_allowed=gate_snapshot.decision_allows_execution,
        operation_blocked=operation_blocked,
        actual_execution_performed=gate_snapshot.actual_execution_performed,
        telemetry_status=telemetry.status.value,
        scenario_status=(
            SecurityTracerScenarioStatus.PASSED
            if scenario_passed
            else SecurityTracerScenarioStatus.FAILED
        ),
        reason_codes=(
            ("security_tracer_expected_block_confirmed",) + gate_snapshot.reason_codes
            if scenario_passed
            else ("security_tracer_expectation_failed",) + gate_snapshot.reason_codes
        ),
    )
