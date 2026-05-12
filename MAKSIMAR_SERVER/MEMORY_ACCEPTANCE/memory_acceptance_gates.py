from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_acceptance_models import (
    build_memory_acceptance_contract,
)
from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_write_safety_models import (
    build_memory_write_safety_policy,
)


@dataclass(frozen=True, slots=True)
class MemoryAcceptanceGateResult:
    gate_id: str
    gate_name: str
    passed: bool
    evidence_ref: str
    blocking: bool

    def __post_init__(self) -> None:
        if not self.gate_id:
            raise ValueError("gate_id must be non-empty")
        if not self.gate_name:
            raise ValueError("gate_name must be non-empty")
        if not self.evidence_ref:
            raise ValueError("evidence_ref must be non-empty")
        if self.blocking and not self.passed:
            raise ValueError(f"blocking gate failed: {self.gate_id}")


@dataclass(frozen=True, slots=True)
class MemoryAcceptanceGateReport:
    report_id: str
    gates: Tuple[MemoryAcceptanceGateResult, ...]
    total_gates: int
    passed_gates: int
    failed_gates: int
    dashboard_read_only: bool
    duplicate_write_allowed: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    acceptance_gates_ready: bool

    def __post_init__(self) -> None:
        if not self.report_id:
            raise ValueError("report_id must be non-empty")
        if not self.gates:
            raise ValueError("gates must be non-empty")
        if self.total_gates != len(self.gates):
            raise ValueError("total_gates must match gates length")
        if self.passed_gates != sum(1 for gate in self.gates if gate.passed):
            raise ValueError("passed_gates mismatch")
        if self.failed_gates != sum(1 for gate in self.gates if not gate.passed):
            raise ValueError("failed_gates mismatch")
        if self.dashboard_read_only is not True:
            raise ValueError("dashboard_read_only must be True")
        if self.duplicate_write_allowed:
            raise ValueError("duplicate_write_allowed must be False")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.acceptance_gates_ready is not True:
            raise ValueError("acceptance_gates_ready must be True")


def build_memory_acceptance_gate_report() -> MemoryAcceptanceGateReport:
    contract = build_memory_acceptance_contract()
    write_policy = build_memory_write_safety_policy()

    gates = (
        MemoryAcceptanceGateResult(
            gate_id="gate_memory_acceptance_contract",
            gate_name="Memory acceptance contract ready",
            passed=contract.acceptance_ready,
            evidence_ref="MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_acceptance_models.py",
            blocking=True,
        ),
        MemoryAcceptanceGateResult(
            gate_id="gate_write_safety_policy",
            gate_name="Write safety policy ready",
            passed=write_policy.policy_ready,
            evidence_ref="MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_write_safety_models.py",
            blocking=True,
        ),
        MemoryAcceptanceGateResult(
            gate_id="gate_no_duplicate_write",
            gate_name="Duplicate write is forbidden",
            passed=write_policy.duplicate_write_allowed is False,
            evidence_ref="memory_write_safety_policy_phase_6_0_001",
            blocking=True,
        ),
        MemoryAcceptanceGateResult(
            gate_id="gate_no_direct_canonical_write",
            gate_name="Direct runtime-to-canonical write is forbidden",
            passed=write_policy.direct_runtime_to_canonical_write_allowed is False,
            evidence_ref="memory_write_safety_policy_phase_6_0_001",
            blocking=True,
        ),
        MemoryAcceptanceGateResult(
            gate_id="gate_operator_review_required",
            gate_name="Operator review is required",
            passed=contract.operator_review_required is True,
            evidence_ref="MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_operator_review_builder.py",
            blocking=True,
        ),
        MemoryAcceptanceGateResult(
            gate_id="gate_release_preview_required",
            gate_name="Release preview is required",
            passed=contract.release_preview_required is True,
            evidence_ref="MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_release_preview_builder.py",
            blocking=True,
        ),
    )

    return MemoryAcceptanceGateReport(
        report_id="memory_acceptance_gate_report_phase_6_0_001",
        gates=gates,
        total_gates=len(gates),
        passed_gates=sum(1 for gate in gates if gate.passed),
        failed_gates=sum(1 for gate in gates if not gate.passed),
        dashboard_read_only=contract.dashboard_read_only,
        duplicate_write_allowed=contract.duplicate_write_allowed,
        canonical_write_allowed=contract.canonical_write_allowed,
        runtime_mutation_allowed=contract.runtime_mutation_allowed,
        acceptance_gates_ready=all(gate.passed for gate in gates),
    )
