from __future__ import annotations

from dataclasses import dataclass, field

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_models import WorkflowDefinition


@dataclass(slots=True)
class WorkflowSummary:
    """Aggregated summary across workflow definitions."""

    total_workflows: int = 0
    total_steps: int = 0
    by_trigger: dict[str, int] = field(default_factory=dict)

    def register_definition(self, definition: WorkflowDefinition) -> None:
        """Accumulate one workflow definition."""
        self.total_workflows += 1
        self.total_steps += len(definition.steps)

        for trigger in definition.trigger_phrases:
            self.by_trigger[trigger] = self.by_trigger.get(trigger, 0) + 1


def build_workflow_summary(
    definitions: list[WorkflowDefinition],
) -> WorkflowSummary:
    """Build aggregated workflow summary.

    Args:
        definitions: Workflow definitions.

    Returns:
        Aggregated summary.
    """
    summary = WorkflowSummary()
    for definition in definitions:
        summary.register_definition(definition)
    return summary
