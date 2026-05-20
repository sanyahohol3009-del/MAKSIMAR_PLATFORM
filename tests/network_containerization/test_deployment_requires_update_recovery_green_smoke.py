from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_containerization.network_containerization_acceptance_read_model import (
    build_network_containerization_acceptance_read_model,
)


def test_deployment_requires_update_recovery_green() -> None:
    with pytest.raises(ValueError, match="update_recovery_green_required"):
        build_network_containerization_acceptance_read_model(
            update_recovery_green_required=False,
        )
