from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability.config_boundary_models import (
    TypedConfigBoundaryContract,
    TypedConfigEntry,
)


def build_typed_config_boundary_contract() -> TypedConfigBoundaryContract:
    """Build unified typed config boundary contract."""

    entries = (
        TypedConfigEntry(
            key="runtime.mode",
            value_type="string",
            scope="runtime",
            required=True,
        ),
        TypedConfigEntry(
            key="runtime.max_workers",
            value_type="integer",
            scope="runtime",
            required=True,
        ),
        TypedConfigEntry(
            key="feature.enable_gesture_control",
            value_type="boolean",
            scope="feature_flag",
            required=True,
        ),
        TypedConfigEntry(
            key="feature.enable_voice_input",
            value_type="boolean",
            scope="feature_flag",
            required=True,
        ),
        TypedConfigEntry(
            key="environment.name",
            value_type="string",
            scope="environment",
            required=True,
        ),
    )

    return TypedConfigBoundaryContract(
        total_entries=len(entries),
        entries=entries,
    )
