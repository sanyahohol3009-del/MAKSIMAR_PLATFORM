from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
)
from MAKSIMAR_SERVER.SECURITY_LAYER.adapters.security_existing_policy_adapter import (
    ExistingPolicyPermissionBinding,
    build_existing_policy_adapter_snapshot,
    build_rbac_policy_from_existing_policy_adapter,
    load_existing_policy_sources_from_binding_file,
)


def test_existing_policy_adapter_loads_binding_file_and_builds_rbac_policy(tmp_path: Path) -> None:
    binding_file = tmp_path / "security_existing_sources.yaml"
    binding_file.write_text(
        "\n".join(
            (
                "sources:",
                "  - path: MAKSIMAR_CORE/governance/config/approval_policy.yaml",
                "    relation: existing_security_related_surface",
                "    action: reference_only",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    sources = load_existing_policy_sources_from_binding_file(binding_file)
    snapshot = build_existing_policy_adapter_snapshot(
        sources=sources,
        permission_bindings=(
            ExistingPolicyPermissionBinding(
                role_id="operator",
                permission_id="perm_read_memory",
                action=SecurityActionKind.READ,
                resource_kind=SecurityResourceKind.MEMORY,
                source_path=sources[0].path,
            ),
        ),
    )
    policy = build_rbac_policy_from_existing_policy_adapter(
        snapshot,
        policy_id="adapter_policy",
    )

    assert len(sources) == 1
    assert snapshot.to_read_model().dashboard_safe is True
    assert policy.roles[0].role_id == "operator"
    assert policy.roles[0].permissions[0].permission_id == "perm_read_memory"
