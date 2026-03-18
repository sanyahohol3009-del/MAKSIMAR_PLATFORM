from __future__ import annotations

from functools import lru_cache

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_models import WorkflowDefinition
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_registry import WorkflowRegistry


@lru_cache(maxsize=1)
def _get_registry() -> WorkflowRegistry:
    """Build cached workflow registry."""
    registry = WorkflowRegistry()
    registry.load_all()
    return registry


def get_workflow_definition(workflow_id: str) -> WorkflowDefinition:
    """Get workflow definition by id."""
    definition = _get_registry().get(workflow_id)
    if definition is None:
        raise KeyError(f"Workflow definition not found: {workflow_id}")
    return definition


def list_workflow_definitions() -> list[WorkflowDefinition]:
    """List all loaded workflow definitions."""
    return _get_registry().list_all()


def find_workflows_by_trigger(trigger_phrase: str) -> list[WorkflowDefinition]:
    """Find workflow definitions by trigger phrase."""
    return _get_registry().get_by_trigger(trigger_phrase)
