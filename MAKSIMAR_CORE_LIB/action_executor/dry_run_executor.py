from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_executor.action_accessor import get_action_definition
from MAKSIMAR_CORE_LIB.action_executor.execution_models import (
    ActionExecutionRequest,
    DryRunExecutionResult,
)


def dry_run_execute(request: ActionExecutionRequest) -> DryRunExecutionResult:
    """Resolve one action request without performing real execution.

    Args:
        request: Canonical action execution request.

    Returns:
        Dry-run execution result.
    """
    try:
        definition = get_action_definition(request.action_id)
    except KeyError:
        return DryRunExecutionResult(
            action_id=request.action_id,
            status="blocked",
            resolved=False,
            message="Action definition not found.",
        )

    return DryRunExecutionResult(
        action_id=definition.action_id,
        status="planned",
        resolved=True,
        message="Action resolved successfully in dry-run mode.",
    )
