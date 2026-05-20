from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_containerization.container_exposure_policy import (
    ContainerExposurePolicy,
    build_no_public_exposure_policy,
)


def test_no_public_exposure_policy_defaults_safe() -> None:
    policy = build_no_public_exposure_policy()

    assert policy.public_exposure_allowed is False
    assert policy.bind_localhost_only is True
    assert policy.exposed_ports == ()
    assert policy.published_ports == ()
    assert policy.internal_network_only is True
    assert policy.dashboard_safe is True


def test_container_exposure_policy_rejects_published_ports() -> None:
    with pytest.raises(ValueError, match="published_ports"):
        ContainerExposurePolicy(
            public_exposure_allowed=False,
            bind_localhost_only=True,
            exposed_ports=(),
            published_ports=(8080,),
            internal_network_only=True,
            dashboard_safe=True,
            reason_codes=("bad",),
        )
