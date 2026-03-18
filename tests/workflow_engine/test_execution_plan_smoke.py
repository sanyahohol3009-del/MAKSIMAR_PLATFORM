from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.workflow_engine.execution_plan import build_execution_plan
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_models import (
    WorkflowDefinition,
    WorkflowStep,
)


def test_build_execution_plan_from_definition() -> None:
    """Execution plan should preserve workflow id and step count."""
    definition = WorkflowDefinition(
        workflow_id="wf.sample",
        version="workflow_definition.v1",
        file_path=Path("workflow_definition.v1.yaml"),
        trigger_phrases=["run sample"],
        steps=[
            WorkflowStep(
                step_id="s1",
                action_ref="action.one",
                payload={},
            ),
            WorkflowStep(
                step_id="s2",
                action_ref="action.two",
                payload={},
            ),
        ],
        payload={},
    )

    plan = build_execution_plan(definition)

    assert plan.workflow_id == "wf.sample"
    assert plan.total_steps == 2
    assert plan.steps[0].step_id == "s1"
    assert plan.steps[1].action_ref == "action.two"
