from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_runtime_sandbox_preview_builder import (
    build_mempalace_runtime_sandbox_preview,
)


_ALLOWED_WRITE_ROOTS = (
    "EXTERNAL_BACKENDS/mempalace/sandbox_data",
)

_ALLOWED_READ_ROOTS = (
    "EXTERNAL_BACKENDS/mempalace/source",
    "EXTERNAL_BACKENDS/mempalace/manifests",
    "EXTERNAL_BACKENDS/mempalace/smoke_reports",
    "EXTERNAL_BACKENDS/mempalace/security_reports",
)

_DENIED_ROOTS = (
    "CORE_ROOT",
    "RUNTIME",
    "SUPERVISOR",
    "MAKSIMAR_CORE_LIB",
    "MAKSIMAR_SERVER/EXECUTION_CONTROL",
    "MAKSIMAR_SERVER/RUNTIME",
    "MAKSIMAR_SERVER/MEMORY_SYNC",
    "MAKSIMAR_SERVER/CONTROL_PLANE",
    ".env",
    ".pymon",
)

_DENIED_ENV_KEYS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GITHUB_TOKEN",
    "HF_TOKEN",
    "HUGGINGFACE_TOKEN",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "DATABASE_URL",
    "POSTGRES_PASSWORD",
    "REDIS_PASSWORD",
)


@dataclass(frozen=True, slots=True)
class MemPalaceFilesystemBoundary:
    boundary_id: str
    allowed_read_roots: Tuple[str, ...]
    allowed_write_roots: Tuple[str, ...]
    denied_roots: Tuple[str, ...]
    sandbox_data_only: bool
    canonical_memory_access: bool
    canonical_artifact_access: bool
    runtime_state_access: bool
    destructive_operations_allowed: bool
    filesystem_boundary_ready: bool

    def __post_init__(self) -> None:
        if not self.boundary_id:
            raise ValueError("boundary_id must be non-empty")
        if self.allowed_read_roots != _ALLOWED_READ_ROOTS:
            raise ValueError("allowed_read_roots must match approved MemPalace read roots")
        if self.allowed_write_roots != _ALLOWED_WRITE_ROOTS:
            raise ValueError("allowed_write_roots must match approved MemPalace write roots")
        if self.denied_roots != _DENIED_ROOTS:
            raise ValueError("denied_roots must match approved denied roots")
        if not self.sandbox_data_only:
            raise ValueError("sandbox_data_only must be True")
        if self.canonical_memory_access:
            raise ValueError("canonical_memory_access must be False")
        if self.canonical_artifact_access:
            raise ValueError("canonical_artifact_access must be False")
        if self.runtime_state_access:
            raise ValueError("runtime_state_access must be False")
        if self.destructive_operations_allowed:
            raise ValueError("destructive_operations_allowed must be False")
        if not self.filesystem_boundary_ready:
            raise ValueError("filesystem_boundary_ready must be True")


@dataclass(frozen=True, slots=True)
class MemPalaceNetworkBoundary:
    boundary_id: str
    network_default_policy: str
    outbound_network_allowed: bool
    external_download_allowed: bool
    remote_model_api_allowed: bool
    local_loopback_allowed: bool
    network_review_required: bool
    network_boundary_ready: bool

    def __post_init__(self) -> None:
        if not self.boundary_id:
            raise ValueError("boundary_id must be non-empty")
        if self.network_default_policy != "disabled_until_explicit_review":
            raise ValueError("network_default_policy must be disabled_until_explicit_review")
        if self.outbound_network_allowed:
            raise ValueError("outbound_network_allowed must be False")
        if self.external_download_allowed:
            raise ValueError("external_download_allowed must be False")
        if self.remote_model_api_allowed:
            raise ValueError("remote_model_api_allowed must be False")
        if self.local_loopback_allowed:
            raise ValueError("local_loopback_allowed must be False")
        if not self.network_review_required:
            raise ValueError("network_review_required must be True")
        if not self.network_boundary_ready:
            raise ValueError("network_boundary_ready must be True")


@dataclass(frozen=True, slots=True)
class MemPalaceProcessBoundary:
    boundary_id: str
    separate_venv_required: bool
    isolated_workdir_required: bool
    env_scrub_required: bool
    denied_env_keys: Tuple[str, ...]
    project_env_inheritance_allowed: bool
    secrets_access_allowed: bool
    shell_execution_allowed: bool
    subprocess_execution_allowed: bool
    process_boundary_ready: bool

    def __post_init__(self) -> None:
        if not self.boundary_id:
            raise ValueError("boundary_id must be non-empty")
        if not self.separate_venv_required:
            raise ValueError("separate_venv_required must be True")
        if not self.isolated_workdir_required:
            raise ValueError("isolated_workdir_required must be True")
        if not self.env_scrub_required:
            raise ValueError("env_scrub_required must be True")
        if self.denied_env_keys != _DENIED_ENV_KEYS:
            raise ValueError("denied_env_keys must match approved denied env keys")
        if self.project_env_inheritance_allowed:
            raise ValueError("project_env_inheritance_allowed must be False")
        if self.secrets_access_allowed:
            raise ValueError("secrets_access_allowed must be False")
        if self.shell_execution_allowed:
            raise ValueError("shell_execution_allowed must be False")
        if self.subprocess_execution_allowed:
            raise ValueError("subprocess_execution_allowed must be False")
        if not self.process_boundary_ready:
            raise ValueError("process_boundary_ready must be True")


@dataclass(frozen=True, slots=True)
class MemPalaceRealBackendSecurityBoundary:
    boundary_id: str
    filesystem: MemPalaceFilesystemBoundary
    network: MemPalaceNetworkBoundary
    process: MemPalaceProcessBoundary
    manual_security_review_required: bool
    manual_security_review_completed: bool
    real_backend_candidate_detected: bool
    real_backend_enablement_allowed: bool
    real_backend_query_allowed: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    security_boundary_ready: bool

    def __post_init__(self) -> None:
        if not self.boundary_id:
            raise ValueError("boundary_id must be non-empty")
        if not self.manual_security_review_required:
            raise ValueError("manual_security_review_required must be True")
        if self.manual_security_review_completed:
            raise ValueError("manual_security_review_completed must be False in Batch 4A")
        if not self.real_backend_candidate_detected:
            raise ValueError("real_backend_candidate_detected must be True")
        if self.real_backend_enablement_allowed:
            raise ValueError("real_backend_enablement_allowed must be False in Batch 4A")
        if self.real_backend_query_allowed:
            raise ValueError("real_backend_query_allowed must be False in Batch 4A")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.security_boundary_ready:
            raise ValueError("security_boundary_ready must be True")


def build_mempalace_filesystem_boundary() -> MemPalaceFilesystemBoundary:
    for root in _ALLOWED_WRITE_ROOTS:
        Path(root).mkdir(parents=True, exist_ok=True)

    return MemPalaceFilesystemBoundary(
        boundary_id="mempalace_filesystem_boundary_001",
        allowed_read_roots=_ALLOWED_READ_ROOTS,
        allowed_write_roots=_ALLOWED_WRITE_ROOTS,
        denied_roots=_DENIED_ROOTS,
        sandbox_data_only=True,
        canonical_memory_access=False,
        canonical_artifact_access=False,
        runtime_state_access=False,
        destructive_operations_allowed=False,
        filesystem_boundary_ready=True,
    )


def build_mempalace_network_boundary() -> MemPalaceNetworkBoundary:
    return MemPalaceNetworkBoundary(
        boundary_id="mempalace_network_boundary_001",
        network_default_policy="disabled_until_explicit_review",
        outbound_network_allowed=False,
        external_download_allowed=False,
        remote_model_api_allowed=False,
        local_loopback_allowed=False,
        network_review_required=True,
        network_boundary_ready=True,
    )


def build_mempalace_process_boundary() -> MemPalaceProcessBoundary:
    return MemPalaceProcessBoundary(
        boundary_id="mempalace_process_boundary_001",
        separate_venv_required=True,
        isolated_workdir_required=True,
        env_scrub_required=True,
        denied_env_keys=_DENIED_ENV_KEYS,
        project_env_inheritance_allowed=False,
        secrets_access_allowed=False,
        shell_execution_allowed=False,
        subprocess_execution_allowed=False,
        process_boundary_ready=True,
    )


def build_mempalace_real_backend_security_boundary() -> MemPalaceRealBackendSecurityBoundary:
    preview = build_mempalace_runtime_sandbox_preview()

    filesystem = build_mempalace_filesystem_boundary()
    network = build_mempalace_network_boundary()
    process = build_mempalace_process_boundary()

    security_boundary_ready = (
        filesystem.filesystem_boundary_ready
        and network.network_boundary_ready
        and process.process_boundary_ready
        and preview["preview_ready"] is True
        and preview["real_backend_candidate_detected"] is True
        and preview["manual_security_review_required"] is True
        and preview["real_backend_enabled"] is False
        and preview["real_backend_query_allowed"] is False
        and preview["canonical_write_allowed"] is False
        and preview["runtime_mutation_allowed"] is False
    )

    return MemPalaceRealBackendSecurityBoundary(
        boundary_id="mempalace_real_backend_security_boundary_001",
        filesystem=filesystem,
        network=network,
        process=process,
        manual_security_review_required=True,
        manual_security_review_completed=False,
        real_backend_candidate_detected=True,
        real_backend_enablement_allowed=False,
        real_backend_query_allowed=False,
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        security_boundary_ready=security_boundary_ready,
    )


def build_mempalace_real_backend_security_boundary_preview() -> dict[str, object]:
    boundary = build_mempalace_real_backend_security_boundary()

    return {
        "security_boundary_ready": boundary.security_boundary_ready,
        "filesystem_boundary_ready": boundary.filesystem.filesystem_boundary_ready,
        "network_boundary_ready": boundary.network.network_boundary_ready,
        "process_boundary_ready": boundary.process.process_boundary_ready,
        "allowed_read_roots": boundary.filesystem.allowed_read_roots,
        "allowed_write_roots": boundary.filesystem.allowed_write_roots,
        "denied_roots": boundary.filesystem.denied_roots,
        "denied_env_keys": boundary.process.denied_env_keys,
        "network_default_policy": boundary.network.network_default_policy,
        "outbound_network_allowed": boundary.network.outbound_network_allowed,
        "external_download_allowed": boundary.network.external_download_allowed,
        "remote_model_api_allowed": boundary.network.remote_model_api_allowed,
        "secrets_access_allowed": boundary.process.secrets_access_allowed,
        "shell_execution_allowed": boundary.process.shell_execution_allowed,
        "subprocess_execution_allowed": boundary.process.subprocess_execution_allowed,
        "manual_security_review_required": boundary.manual_security_review_required,
        "manual_security_review_completed": boundary.manual_security_review_completed,
        "real_backend_candidate_detected": boundary.real_backend_candidate_detected,
        "real_backend_enablement_allowed": boundary.real_backend_enablement_allowed,
        "real_backend_query_allowed": boundary.real_backend_query_allowed,
        "canonical_write_allowed": boundary.canonical_write_allowed,
        "runtime_mutation_allowed": boundary.runtime_mutation_allowed,
    }
