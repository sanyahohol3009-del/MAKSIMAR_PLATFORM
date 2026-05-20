from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_containerization.container_healthcheck_models import (
    ContainerHealthcheckModel,
    build_default_container_healthcheck_model,
)


def test_default_container_healthcheck_is_enabled_and_safe() -> None:
    healthcheck = build_default_container_healthcheck_model()

    assert healthcheck.enabled is True
    assert healthcheck.command
    assert healthcheck.interval_seconds == 30
    assert healthcheck.timeout_seconds == 5
    assert healthcheck.retries == 3
    assert healthcheck.dashboard_safe is True


def test_container_healthcheck_rejects_disabled_state() -> None:
    with pytest.raises(ValueError, match="enabled"):
        ContainerHealthcheckModel(
            enabled=False,
            command=("CMD", "true"),
            interval_seconds=30,
            timeout_seconds=5,
            retries=3,
            start_period_seconds=10,
            dashboard_safe=True,
            reason_codes=("bad",),
        )
