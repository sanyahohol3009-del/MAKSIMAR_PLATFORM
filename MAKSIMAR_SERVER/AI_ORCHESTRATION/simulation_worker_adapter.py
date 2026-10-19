from __future__ import annotations

"""Canonical evidence bridge for the existing runnable simulation worker owner."""

from dataclasses import asdict
import hashlib
import json
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle,
    EvidenceItem,
    ExecutionPlan,
    ExecutionReceipt,
    RequestDeadline,
    RequestUnderstanding,
    utc_observed_at,
)
from MAKSIMAR_CORE_LIB.workers_registry.simulation_io_contracts import (
    SimulationEngineRequest,
    SimulationEngineResult,
)
from MAKSIMAR_CORE_LIB.workers_registry.simulation_worker_provider_registry import (
    get_simulation_worker_factory,
)


PROVIDER_ID = "existing_simulation_worker_runtime"
SIMULATION_SCENARIOS = (
    "control_validation",
    "safety_regression",
    "runtime_pressure_probe",
)


DEFAULT_ITERATION_BUDGET = 8


def _coerce_positive_int(value: Any) -> int | None:
    """Return the single unambiguous integer token in a parameter string, else None.

    Never concatenates separate digit groups: zero numeric tokens or multiple distinct
    numeric groups both resolve to None so the caller can apply a runtime default rather
    than fabricate a value (e.g. '8 to 10' is ambiguous, 'user_defined' is unresolved)."""
    text = str(value or "")
    tokens: list[str] = []
    current: list[str] = []
    for ch in text:
        if ch.isdigit():
            current.append(ch)
        else:
            if current:
                tokens.append("".join(current))
                current = []
    if current:
        tokens.append("".join(current))
    if len(tokens) != 1:
        return None
    return int(tokens[0])


def _contract(
    operation_id: str, description: str, *, semantic_owner_id: str = "simulation.run",
) -> tuple[dict[str, Any], ...]:
    return ({
        "operation_id": operation_id,
        "description": description,
        "required_parameters": ("scenario_type", "iteration_budget"),
        "evidence_kinds": ("simulation_result",),
        "effect_type": "EXECUTE",
        "target_scope": "local_simulation_runtime",
        "semantic_owner_id": semantic_owner_id,
        "reversibility": "REVERSIBLE",
        "external_side_effect": False,
        "risk_class": "MUTATION",
    },)


SIMULATION_CAPABILITY_OPERATION_CONTRACTS: dict[str, tuple[dict[str, Any], ...]] = {
    "skill_simulation_simulation_analysis": _contract(
        "analyze_simulation",
        "Run the existing local sandboxed simulation-analysis skill. scenario_type must be exactly one of "
        "control_validation, safety_regression, or runtime_pressure_probe; a control simulation uses "
        "control_validation. iteration_budget is an integer from 1 through 10000.",
        semantic_owner_id="simulation.analyze",
    ),
    "worker_sim_001": _contract(
        "run_simulation_task",
        "Run the existing local Python simulation worker. scenario_type must be exactly one of "
        "control_validation, safety_regression, or runtime_pressure_probe; a control simulation uses "
        "control_validation. iteration_budget is an integer from 1 through 10000.",
        semantic_owner_id="simulation.run",
    ),
}


class ExistingSimulationWorkerAdapter:
    """One provider boundary over the existing SimulationWorkerRuntime."""

    provider_id = PROVIDER_ID

    def __init__(self) -> None:
        self.__runtime = None

    @property
    def _runtime(self):
        if self.__runtime is None:
            self.__runtime = get_simulation_worker_factory()()
        return self.__runtime

    def health(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "status": "AVAILABLE",
            "worker_id": self._runtime.worker_id,
            "sandboxed": True,
            "network_required": False,
            "external_side_effect": False,
        }

    def collect_evidence(
        self,
        understanding: RequestUnderstanding,
        plan: ExecutionPlan,
        trace_id: str,
        deadline: RequestDeadline | None = None,
    ) -> EvidenceBundle:
        items: list[EvidenceItem] = []
        receipts: list[ExecutionReceipt] = []
        errors: list[str] = []
        allowed_operations = {
            contract["operation_id"]
            for contracts in SIMULATION_CAPABILITY_OPERATION_CONTRACTS.values()
            for contract in contracts
        }
        for step in plan.steps:
            if deadline is not None and deadline.cancelled:
                errors.append(f"{step.operation}:total_deadline")
                break
            if step.operation not in allowed_operations:
                errors.append(f"{step.operation}:unsupported_operation")
                continue
            parameters = dict(step.parameters)
            scenario = str(parameters.get("scenario_type", ""))
            iteration_budget = _coerce_positive_int(parameters.get("iteration_budget", ""))
            if iteration_budget is None:
                # iteration_budget is runtime-defaultable; a missing/ambiguous model value
                # must never be fabricated, so the provider owns the canonical safe default.
                iteration_budget = DEFAULT_ITERATION_BUDGET
            if scenario not in SIMULATION_SCENARIOS:
                errors.append(f"{step.operation}:invalid_scenario_type")
                continue
            if not 1 <= iteration_budget <= 10_000:
                errors.append(f"{step.operation}:iteration_budget_out_of_range")
                continue
            request = SimulationEngineRequest(
                task_id=f"{understanding.request_id}:{step.step_id}",
                scenario_type=scenario,
                iteration_budget=iteration_budget,
                input_payload_ref=f"request://{understanding.request_id}",
                requires_gpu=False,
                degraded_allowed=True,
                trace_id=trace_id,
            )
            try:
                result = self._runtime.execute_task(request)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{step.operation}:{type(exc).__name__}")
                continue
            payload = asdict(result)
            observation = json.dumps(payload, ensure_ascii=False, sort_keys=True)
            digest = hashlib.sha256(observation.encode("utf-8")).hexdigest()
            items.append(EvidenceItem(
                kind="simulation_result",
                source=f"{self.provider_id}:{step.operation}",
                observation=observation,
                scope="local_simulation_runtime",
                confidence=1.0,
                trace_id=trace_id,
                observed_at=utc_observed_at(),
                content_hash=f"sha256:{digest}",
                source_reference=result.output_payload_ref,
                truncated=False,
                omitted_count=0,
                request_id=understanding.request_id,
                step_id=step.step_id,
                capability_id=step.capability_id,
                operation_id=step.operation,
                provider_id=self.provider_id,
            ))
            receipts.append(ExecutionReceipt(
                receipt_id=f"{trace_id}:{step.step_id}",
                request_id=understanding.request_id,
                trace_id=trace_id,
                step_id=step.step_id,
                capability_id=step.capability_id,
                operation_id=step.operation,
                provider_id=self.provider_id,
                status="COMPLETE",
                result="existing local simulation worker completed the typed task",
            ))
        status = "COMPLETE" if items and not errors else "PARTIAL" if items else "UNAVAILABLE"
        capability_ids = tuple(dict.fromkeys(step.capability_id for step in plan.steps))
        return EvidenceBundle(
            request_id=understanding.request_id,
            capability_id=(capability_ids[0] if capability_ids else "worker_sim_001"),
            trace_id=trace_id,
            status=status,
            items=tuple(items),
            limitations=(() if status == "COMPLETE" else ("simulation execution incomplete",)),
            receipts=tuple(receipts),
            errors=tuple(errors),
            capability_ids=capability_ids,
        )


__all__ = [
    "ExistingSimulationWorkerAdapter",
    "PROVIDER_ID",
    "SIMULATION_CAPABILITY_OPERATION_CONTRACTS",
    "SIMULATION_SCENARIOS",
]
