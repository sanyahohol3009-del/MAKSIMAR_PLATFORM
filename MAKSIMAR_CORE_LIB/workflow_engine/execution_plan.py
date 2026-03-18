from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_models import WorkflowDefinition


@dataclass(frozen=True, slots=True)
class PlannedWorkflowStep:
    """Canonical planned workflow step."""

    step_id: str
    action_ref: str


@dataclass(frozen=True, slots=True)
class WorkflowExecutionPlan:
    """Canonical execution plan for one workflow."""

    workflow_id: str
    total_steps: int
    steps: list[PlannedWorkflowStep]


def build_execution_plan(definition: WorkflowDefinition) -> WorkflowExecutionPlan:
    """Build execution plan from loaded workflow definition.

    Args:
        definition: Workflow definition.

    Returns:
        Canonical execution plan.
    """
    steps = [
        PlannedWorkflowStep(
            step_id=step.step_id,
            action_ref=step.action_ref,
        )
        for step in definition.steps
    ]

    return WorkflowExecutionPlan(
        workflow_id=definition.workflow_id,
        total_steps=len(steps),
        steps=steps,
    )
