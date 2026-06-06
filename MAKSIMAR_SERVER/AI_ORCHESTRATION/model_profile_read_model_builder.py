from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    build_model_profile_registry,
)


def build_model_profile_read_model() -> dict[str, Any]:
    registry = build_model_profile_registry()
    read_model = registry.to_read_model()
    profiles = tuple(read_model["profiles"])

    return {
        "summary_id": "jarvis_live_model_profile_read_model_v1",
        "registry_id": read_model["registry_id"],
        "profile_count": len(profiles),
        "roles": tuple(profile["role"] for profile in profiles),
        "profiles": profiles,
        "referenced_architecture_surfaces": read_model["referenced_architecture_surfaces"],
        "duplicated_registry_surfaces": read_model["duplicated_registry_surfaces"],
        "model_download_allowed_now": False,
        "runtime_start_allowed_now": False,
        "read_only": True,
        "dashboard_safe": True,
    }
