from __future__ import annotations

from collections import defaultdict

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_loader import load_all_workflow_definitions
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_models import WorkflowDefinition


class WorkflowRegistry:
    """In-memory registry of workflow definitions."""

    def __init__(self) -> None:
        self._definitions: dict[str, WorkflowDefinition] = {}
        self._by_trigger: dict[str, list[WorkflowDefinition]] = defaultdict(list)

    def load_all(self) -> None:
        """Load all workflow definitions."""
        for result in load_all_workflow_definitions():
            if not result.is_valid or result.definition is None:
                continue

            definition = result.definition
            self._definitions[definition.workflow_id] = definition

            for trigger in definition.trigger_phrases:
                self._by_trigger[trigger].append(definition)

    def get(self, workflow_id: str) -> WorkflowDefinition | None:
        """Get workflow by workflow_id."""
        return self._definitions.get(workflow_id)

    def get_by_trigger(self, trigger_phrase: str) -> list[WorkflowDefinition]:
        """Get workflows by trigger phrase."""
        return self._by_trigger.get(trigger_phrase, [])

    def list_all(self) -> list[WorkflowDefinition]:
        """List all loaded workflow definitions."""
        return list(self._definitions.values())
