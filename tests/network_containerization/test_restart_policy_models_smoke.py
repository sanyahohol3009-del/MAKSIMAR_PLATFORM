from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_containerization.restart_policy_models import (
    RestartPolicyModel,
    build_default_restart_policy_model,
)


def test_default_restart_policy_is_required_and_safe() -> None:
    policy = build_default_restart_policy_model()

    assert policy.policy_name == "unless-stopped"
    assert policy.restart_policy_required is True
    assert policy.maximum_retry_count == 3
    assert policy.dashboard_safe is True


def test_restart_policy_rejects_unsupported_policy() -> None:
    with pytest.raises(ValueError, match="unsupported restart policy"):
        RestartPolicyModel(
            policy_name="always",  # type: ignore[arg-type]
            restart_policy_required=True,
            maximum_retry_count=3,
            dashboard_safe=True,
            reason_codes=("bad",),
        )
