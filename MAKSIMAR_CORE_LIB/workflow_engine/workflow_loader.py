from __future__ import annotations

from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.shared_services.atomic_io import AtomicIOError, safe_read_yaml
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_models import (
    WorkflowDefinition,
    WorkflowLoadResult,
    WorkflowStep,
)


def _extract_string_list(value: Any) -> list[str]:
    """Extract list of strings from arbitrary value."""
    if not isinstance(value, list):
        return []

    items: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            items.append(item.strip())
    return items


def _extract_steps(payload: dict[str, Any]) -> tuple[list[WorkflowStep], str | None]:
    """Extract canonical workflow steps from payload."""
    raw_steps = payload.get("steps")
    if not isinstance(raw_steps, list):
        return [], "Workflow definition must contain 'steps' list."

    steps: list[WorkflowStep] = []

    for index, raw_step in enumerate(raw_steps):
        if not isinstance(raw_step, dict):
            return [], f"Step at index {index} must be a mapping."

        step_id = raw_step.get("step_id")
        action_ref = raw_step.get("action_ref")

        if not isinstance(step_id, str) or not step_id.strip():
            return [], f"Step at index {index} must contain non-empty 'step_id'."

        if not isinstance(action_ref, str) or not action_ref.strip():
            return [], f"Step at index {index} must contain non-empty 'action_ref'."

        step_payload = {
            key: value
            for key, value in raw_step.items()
            if key not in {"step_id", "action_ref"}
        }

        steps.append(
            WorkflowStep(
                step_id=step_id.strip(),
                action_ref=action_ref.strip(),
                payload=step_payload,
            )
        )

    return steps, None


def collect_workflow_files() -> list[Path]:
    """Collect workflow definition contract files."""
    root = PATHS.workflow_contracts
    if not root.exists() or not root.is_dir():
        return []

    return sorted(
        [
            path
            for path in root.glob("*.yaml")
            if path.is_file()
            and path.name not in {"workflow_execution.v1.yaml", "action_result.v1.yaml"}
        ]
    )


def load_workflow_definition(file_path: Path) -> WorkflowLoadResult:
    """Load one workflow definition from contract YAML."""
    try:
        payload = safe_read_yaml(file_path)
    except AtomicIOError as exc:
        return WorkflowLoadResult(
            definition=None,
            is_valid=False,
            error=f"Failed to read workflow file: {exc}",
        )

    workflow_id = payload.get("workflow_id")
    if not isinstance(workflow_id, str) or not workflow_id.strip():
        return WorkflowLoadResult(
            definition=None,
            is_valid=False,
            error="Workflow definition must contain non-empty 'workflow_id'.",
        )

    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, str) or not schema_version.strip():
        return WorkflowLoadResult(
            definition=None,
            is_valid=False,
            error="Workflow definition must contain non-empty 'schema_version'.",
        )

    trigger_phrases = _extract_string_list(payload.get("trigger_phrases"))

    steps, step_error = _extract_steps(payload)
    if step_error is not None:
        return WorkflowLoadResult(
            definition=None,
            is_valid=False,
            error=step_error,
        )

    definition = WorkflowDefinition(
        workflow_id=workflow_id.strip(),
        version=schema_version.strip(),
        file_path=file_path,
        trigger_phrases=trigger_phrases,
        steps=steps,
        payload=payload,
    )

    return WorkflowLoadResult(
        definition=definition,
        is_valid=True,
    )


def load_all_workflow_definitions() -> list[WorkflowLoadResult]:
    """Load all workflow definitions from workflow contracts root."""
    return [load_workflow_definition(file_path) for file_path in collect_workflow_files()]
