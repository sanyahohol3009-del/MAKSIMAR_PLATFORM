from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_executor.dry_run_executor import dry_run_execute
from MAKSIMAR_CORE_LIB.action_executor.execution_models import ActionExecutionRequest


def test_dry_run_executor_blocks_unknown_action() -> None:
    """Dry-run executor should block unknown action."""
    request = ActionExecutionRequest(
        action_id="unknown.action",
        parameters={},
        context={},
    )

    result = dry_run_execute(request)

    assert result.status == "blocked"
    assert result.resolved is False


def test_dry_run_executor_plans_known_action() -> None:
    """Dry-run executor should plan known action."""
    request = ActionExecutionRequest(
        action_id="action_manifest",
        parameters={},
        context={},
    )

    result = dry_run_execute(request)

    assert result.status == "planned"
    assert result.resolved is True
