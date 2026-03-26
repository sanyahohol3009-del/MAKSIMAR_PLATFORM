from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.payload_policy_models import PayloadClass
from MAKSIMAR_CORE_LIB.validation_policy import (
    ValidationErrorCode,
    ValidationTaskClass,
    build_validation_error_entry,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.validation_gate.l1_header_validation import (
    L1HeaderValidationInput,
    validate_l1_header,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.validation_gate.l2_schema_validation import (
    L2SchemaValidationInput,
    validate_l2_schema,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.validation_gate.l3_deep_validation import (
    L3DeepValidationInput,
    validate_l3_deep,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.validation_gate.validation_gate_models import (
    ServerValidationGateContract,
    ServerValidationGateEntry,
)


@dataclass(frozen=True, slots=True)
class _ServerValidationInput:
    """Internal server-side validation gate input."""

    request_id: str
    task_class: ValidationTaskClass
    payload_class: PayloadClass
    payload_size_kb: int
    artifact_ref: str
    owner_task_id: str
    domain_policy_ack: bool
    safety_context_present: bool


def _assert_error_code_exists(
    *,
    error_code: ValidationErrorCode,
) -> None:
    """Ensure canonical validation error entry exists."""
    build_validation_error_entry(error_code=error_code)


def build_server_validation_gate_contract() -> ServerValidationGateContract:
    """Build server-side validation gate contract for L1/L2/L3 validation path."""
    inputs = (
        _ServerValidationInput(
            request_id="val_req_001",
            task_class="chat_request",
            payload_class="small_control",
            payload_size_kb=8,
            artifact_ref="",
            owner_task_id="",
            domain_policy_ack=False,
            safety_context_present=False,
        ),
        _ServerValidationInput(
            request_id="val_req_002",
            task_class="simulation_request",
            payload_class="heavy_artifact",
            payload_size_kb=2048,
            artifact_ref="artifact://simulation/output_001",
            owner_task_id="task_sim_001",
            domain_policy_ack=False,
            safety_context_present=False,
        ),
        _ServerValidationInput(
            request_id="val_req_003",
            task_class="robotics_action",
            payload_class="heavy_artifact",
            payload_size_kb=2048,
            artifact_ref="artifact://robotics/action_001",
            owner_task_id="task_robot_001",
            domain_policy_ack=True,
            safety_context_present=True,
        ),
        _ServerValidationInput(
            request_id="val_req_004",
            task_class="automation_job",
            payload_class="heavy_artifact",
            payload_size_kb=2048,
            artifact_ref="artifact://automation/job_001",
            owner_task_id="task_auto_001",
            domain_policy_ack=False,
            safety_context_present=False,
        ),
    )

    entries: list[ServerValidationGateEntry] = []

    for item in inputs:
        l1_result = validate_l1_header(
            request=L1HeaderValidationInput(
                request_id=item.request_id,
                task_class=item.task_class,
                payload_class=item.payload_class,
            )
        )

        if not l1_result.passed:
            _assert_error_code_exists(error_code=l1_result.error_code)  # type: ignore[arg-type]
            entries.append(
                ServerValidationGateEntry(
                    request_id=item.request_id,
                    task_class=item.task_class,
                    payload_class=item.payload_class,
                    resolved_validation_tier="L1_HEADER",
                    l1_header_passed=False,
                    l2_schema_passed=False,
                    l3_deep_passed=False,
                    final_status="rejected",
                    blocking_error_code=l1_result.error_code,
                    description="Server validation gate rejected request at L1 header validation.",
                )
            )
            continue

        l2_result = validate_l2_schema(
            request=L2SchemaValidationInput(
                task_class=item.task_class,
                payload_class=item.payload_class,
                payload_size_kb=item.payload_size_kb,
                artifact_ref=item.artifact_ref,
                owner_task_id=item.owner_task_id,
            )
        )

        if not l2_result.passed:
            _assert_error_code_exists(error_code=l2_result.error_code)  # type: ignore[arg-type]
            entries.append(
                ServerValidationGateEntry(
                    request_id=item.request_id,
                    task_class=item.task_class,
                    payload_class=item.payload_class,
                    resolved_validation_tier=(
                        l2_result.resolved_validation_tier
                        if l2_result.resolved_validation_tier != ""
                        else "L2_SCHEMA"
                    ),
                    l1_header_passed=True,
                    l2_schema_passed=False,
                    l3_deep_passed=False,
                    final_status="rejected",
                    blocking_error_code=l2_result.error_code,
                    description="Server validation gate rejected request at L2 schema validation.",
                )
            )
            continue

        l3_result = validate_l3_deep(
            request=L3DeepValidationInput(
                deep_validation_required=l2_result.deep_validation_required,
                execution_side_effects_possible=l2_result.execution_side_effects_possible,
                domain_policy_ack=item.domain_policy_ack,
                safety_context_present=item.safety_context_present,
            )
        )

        if l3_result.executed and not l3_result.passed:
            _assert_error_code_exists(error_code=l3_result.error_code)  # type: ignore[arg-type]
            entries.append(
                ServerValidationGateEntry(
                    request_id=item.request_id,
                    task_class=item.task_class,
                    payload_class=item.payload_class,
                    resolved_validation_tier=l2_result.resolved_validation_tier,  # type: ignore[arg-type]
                    l1_header_passed=True,
                    l2_schema_passed=True,
                    l3_deep_passed=False,
                    final_status="rejected",
                    blocking_error_code=l3_result.error_code,
                    description="Server validation gate rejected request at L3 deep validation.",
                )
            )
            continue

        entries.append(
            ServerValidationGateEntry(
                request_id=item.request_id,
                task_class=item.task_class,
                payload_class=item.payload_class,
                resolved_validation_tier=l2_result.resolved_validation_tier,  # type: ignore[arg-type]
                l1_header_passed=True,
                l2_schema_passed=l2_result.resolved_validation_tier in ("L2_SCHEMA", "L3_DEEP"),
                l3_deep_passed=l3_result.executed and l3_result.passed,
                final_status="passed",
                blocking_error_code="",
                description="Server validation gate passed request through required validation path.",
            )
        )

    passed_entries = sum(1 for entry in entries if entry.final_status == "passed")
    rejected_entries = sum(1 for entry in entries if entry.final_status == "rejected")

    return ServerValidationGateContract(
        total_entries=len(entries),
        passed_entries=passed_entries,
        rejected_entries=rejected_entries,
        entries=tuple(entries),
    )
