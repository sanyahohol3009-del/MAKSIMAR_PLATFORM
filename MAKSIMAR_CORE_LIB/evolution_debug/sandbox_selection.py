"""Typed selection over the existing sandbox family.

This module is a read/selection boundary; it does not execute arbitrary code,
grant authority, or introduce another registry.  Each family member retains
its own executor and review contract.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ExperimentKind = Literal["code_logic", "simulation", "live_vendor", "robotics"]


@dataclass(frozen=True, slots=True)
class ExperimentRequirement:
    experiment_kind: ExperimentKind
    target_domain: str
    required_capabilities: tuple[str, ...] = ()
    mutation_scope: Literal["artifact_only", "canonical_write"] = "artifact_only"
    external_dependency_required: bool = False
    simulation_required: bool = False
    body_required: bool = False
    hardware_required: bool = False
    network_required: bool = False
    resource_profile: str = "bounded_small"
    expected_artifacts: tuple[str, ...] = ()
    validation_goal: str = ""

    def __post_init__(self) -> None:
        if self.mutation_scope != "artifact_only":
            raise ValueError("sandbox experiments cannot request canonical writes")
        if self.network_required and not self.external_dependency_required:
            raise ValueError("network requirement must be explicit")


SANDBOX_CAPABILITY_MAP = (
    {
        "authority": "READ_MODEL",
        "sandbox_id": "code_logic",
        "canonical_owner": "MAKSIMAR_CORE_LIB/evolution_debug",
        "purpose": "bounded generated-code and logic validation",
        "status": "CONTRACT_ONLY",
        "executor": None,
        "input_contract": "controlled code/evolution proposal",
        "output_contract": "artifact/test report/evidence",
        "allowed_tools": ("deterministic tests",),
        "cannot_execute": ("canonical writes", "deployment", "hardware", "unrestricted shell"),
        "resource_policy": "CODEGEN_LAYER/config/sandbox_policy.yaml",
        "network_policy": "off_by_default",
        "write_boundary": "artifact_only",
        "hardware_authority": False,
        "review_owner": "MAKSIMAR_SERVER/SANDBOX_REVIEW",
        "evidence_output": True,
    },
    {
        "authority": "READ_MODEL",
        "sandbox_id": "simulation",
        "canonical_owner": "SIMULATION_LAYER + MAKSIMAR_SERVER/WORKERS/simulation_worker",
        "purpose": "bounded numerical/system/behavioral simulation",
        "status": "ACTIVE_EXECUTOR",
        "executor": "PythonSimulationEngine",
        "input_contract": "SimulationEngineRequest",
        "output_contract": "SimulationEngineResult",
        "allowed_tools": ("python simulation backend",),
        "cannot_execute": ("canonical writes", "physical hardware", "unbounded network"),
        "resource_policy": "simulation_layer config profiles",
        "network_policy": "off_by_default",
        "write_boundary": "artifact_only",
        "hardware_authority": False,
        "review_owner": "MAKSIMAR_SERVER/SANDBOX_REVIEW",
        "evidence_output": True,
    },
    {
        "authority": "READ_MODEL",
        "sandbox_id": "live_vendor",
        "canonical_owner": "MAKSIMAR_SERVER/AI_ORCHESTRATION/live_sandbox_runtime_policy.py",
        "purpose": "provider/runtime candidate evaluation",
        "status": "CONTRACT_ONLY",
        "executor": None,
        "input_contract": "typed vendor/runtime candidate",
        "output_contract": "candidate report/evidence",
        "allowed_tools": ("bounded local provider probes",),
        "cannot_execute": ("implicit install", "credential access", "canonical writes"),
        "resource_policy": "live_sandbox_runtime_policy",
        "network_policy": "explicit_only",
        "write_boundary": "artifact_only",
        "hardware_authority": False,
        "review_owner": "MAKSIMAR_SERVER/SANDBOX_REVIEW",
        "evidence_output": True,
    },
    {
        "authority": "READ_MODEL",
        "sandbox_id": "robotics_safety",
        "canonical_owner": "ROBOTICS_LAYER + MAKSIMAR_CORE/contracts/robotics",
        "purpose": "embodied policy simulation and safety validation",
        "status": "CONTRACT_ONLY",
        "executor": None,
        "input_contract": "typed body/control policy contract",
        "output_contract": "simulation/safety report/evidence",
        "allowed_tools": ("simulation-first safety checks",),
        "cannot_execute": ("direct hardware", "canonical writes", "unapproved actuation"),
        "resource_policy": "robotics safety contracts",
        "network_policy": "off_by_default",
        "write_boundary": "artifact_only",
        "hardware_authority": False,
        "review_owner": "MAKSIMAR_SERVER/SANDBOX_REVIEW",
        "evidence_output": True,
    },
)


def sandbox_capability_map() -> tuple[dict[str, object], ...]:
    return tuple(dict(item) for item in SANDBOX_CAPABILITY_MAP)


def select_sandbox(requirement: ExperimentRequirement) -> dict[str, object]:
    by_kind = {"code_logic": "code_logic", "simulation": "simulation", "live_vendor": "live_vendor", "robotics": "robotics_safety"}
    sandbox_id = by_kind[requirement.experiment_kind]
    entry = next(item for item in SANDBOX_CAPABILITY_MAP if item["sandbox_id"] == sandbox_id)
    execution_status = "PASS" if entry["status"] == "ACTIVE_EXECUTOR" else "PRECONDITION_REQUIRED"
    if requirement.hardware_required:
        execution_status = "DENIED"
    return {
        "sandbox_id": sandbox_id,
        "selection": "SELECTED",
        "selection_basis": "typed_experiment_requirement",
        "executor_status": entry["status"],
        "execution_status": execution_status,
        "network_policy": entry["network_policy"],
        "write_boundary": entry["write_boundary"],
        "review_required": True,
        "hardware_execution_allowed": False,
        "hardware_required": requirement.hardware_required,
    }


def requirement_from_semantic_understanding(understanding: dict[str, object]) -> ExperimentRequirement | None:
    """Project an already-understood goal into sandbox selection input."""
    domain = str(understanding.get("semantic_domain", ""))
    scope = str(understanding.get("target_scope", ""))
    effect = str(understanding.get("effect_intent", understanding.get("effect_type", "")))
    if (domain == "simulation" or scope == "local_simulation_runtime") and effect in {"compute_run", "EXECUTE"}:
        return ExperimentRequirement("simulation", target_domain="system", simulation_required=True)
    if (domain == "code" or scope == "provided_task_context") and effect in {"reason_propose", "OBSERVE"}:
        return ExperimentRequirement("code_logic", target_domain="code")
    if (domain == "runtime" or scope.startswith("local_runtime")) and effect in {"compute_run", "EXECUTE"}:
        return ExperimentRequirement("live_vendor", target_domain="runtime", external_dependency_required=False)
    if domain == "robotics":
        return ExperimentRequirement(
            "robotics", target_domain="embodied_control", simulation_required=True,
            body_required=True, hardware_required=effect == "change_state",
        )
    return None
