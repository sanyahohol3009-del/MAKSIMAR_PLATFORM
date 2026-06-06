from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.workers_registry.worker_alias_binding_contract import (
    build_worker_alias_binding_contract,
)
from MAKSIMAR_CORE_LIB.workers_registry.worker_role_binding_contract import (
    build_worker_role_binding_contract,
)


def build_model_worker_binding_read_model() -> dict[str, Any]:
    role_contract = build_worker_role_binding_contract()
    alias_contract = build_worker_alias_binding_contract()
    role_read_model = role_contract.to_read_model()
    alias_read_model = alias_contract.to_read_model()

    return {
        "summary_id": "model_worker_binding_read_model_v0_1",
        "roles": role_read_model["bindings"],
        "aliases": alias_read_model["alias_bindings"],
        "role_count": role_read_model["role_count"],
        "alias_count": alias_read_model["alias_count"],
        "canonical_worker_ids": alias_read_model["canonical_worker_ids"],
        "referenced_surfaces": role_read_model["referenced_surfaces"],
        "reused_existing_worker_registry": True,
        "new_worker_registry_created": False,
        "runtime_start_allowed": False,
        "direct_execution_allowed": False,
        "shell_allowed": False,
        "model_download_allowed": False,
        "dashboard_execution_allowed": False,
        "read_only": True,
        "dashboard_safe": True,
    }

