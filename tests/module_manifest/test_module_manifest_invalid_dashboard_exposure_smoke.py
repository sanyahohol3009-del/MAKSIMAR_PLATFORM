from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.module_manifest import (
    ModuleManifestEntry,
)


def test_module_manifest_invalid_dashboard_exposure_smoke() -> None:
    with pytest.raises(ValueError, match="dashboard_view_ids require dashboard_exposure_allowed"):
        ModuleManifestEntry(
            module_kind="extension_cube",
            module_slug="bad_dashboard_exposure",
            display_name="Bad Dashboard Exposure",
            domain_class="observability",
            input_contract_ids=(),
            output_contract_ids=(),
            policy_profile="read_only",
            observability_profile="basic",
            dashboard_view_ids=("view_bad_dashboard_exposure",),
            supported_display_roles=("primary_dashboard_display",),
            explanation_available=False,
            multi_display_allowed=False,
            engine_adapter_required=False,
            supported_languages=("en",),
            supported_scripts=("Latin",),
            active=True,
            dashboard_exposure_allowed=False,
        )
