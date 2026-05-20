from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_containerization.network_containerization_acceptance_read_model import (
    build_network_containerization_acceptance_read_model,
)


def test_deployment_requires_security_layer_green() -> None:
    with pytest.raises(ValueError, match="security_layer_green_required"):
        build_network_containerization_acceptance_read_model(
            security_layer_green_required=False,
        )
