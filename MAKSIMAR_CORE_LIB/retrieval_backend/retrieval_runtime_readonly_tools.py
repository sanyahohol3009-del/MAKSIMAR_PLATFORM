from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


RETRIEVAL_VENDOR_ROOT = Path("EXTERNAL_BACKENDS/vendor_quarantine/retrieval_backends")


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class RetrievalRuntimeReadonlyBackendAvailability:
    backend_kind: str
    vendor_path: str
    source_present: bool
    usable_now: bool
    selected_tool: str
    fallback_tool: str
    unavailable_reason: str
    read_only: bool = True
    direct_execution_allowed: bool = False
    canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    network_allowed_by_default: bool = False
    docker_required_now: bool = False
    qdrant_server_start_allowed: bool = False

    def __post_init__(self) -> None:
        backend_kind = _require_text(self.backend_kind, "backend_kind")
        vendor_path = _require_text(self.vendor_path, "vendor_path")
        selected_tool = _require_text(self.selected_tool, "selected_tool")
        fallback_tool = _require_text(self.fallback_tool, "fallback_tool")
        unavailable_reason = _require_text(self.unavailable_reason, "unavailable_reason")
        if backend_kind not in {"mgrep", "sqlite_vec", "qdrant"}:
            raise ValueError(f"unsupported backend_kind: {backend_kind}")
        for field_name in (
            "source_present",
            "usable_now",
            "read_only",
            "direct_execution_allowed",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "network_allowed_by_default",
            "docker_required_now",
            "qdrant_server_start_allowed",
        ):
            _require_bool(getattr(self, field_name), field_name)
        if not self.read_only:
            raise ValueError("read_only must be True")
        for field_name in (
            "direct_execution_allowed",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "network_allowed_by_default",
            "docker_required_now",
            "qdrant_server_start_allowed",
        ):
            if getattr(self, field_name):
                raise ValueError(f"{field_name} must be False")
        object.__setattr__(self, "backend_kind", backend_kind)
        object.__setattr__(self, "vendor_path", vendor_path)
        object.__setattr__(self, "selected_tool", selected_tool)
        object.__setattr__(self, "fallback_tool", fallback_tool)
        object.__setattr__(self, "unavailable_reason", unavailable_reason)

    def to_read_model(self) -> dict[str, object]:
        return {
            "backend_kind": self.backend_kind,
            "vendor_path": self.vendor_path,
            "source_present": self.source_present,
            "usable_now": self.usable_now,
            "selected_tool": self.selected_tool,
            "fallback_tool": self.fallback_tool,
            "unavailable_reason": self.unavailable_reason,
            "read_only": self.read_only,
            "direct_execution_allowed": self.direct_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "docker_required_now": self.docker_required_now,
            "qdrant_server_start_allowed": self.qdrant_server_start_allowed,
        }


def _vendor_path(project_root: Path, backend_dir: str) -> Path:
    return project_root / RETRIEVAL_VENDOR_ROOT / backend_dir


def inspect_mgrep_readonly_availability(project_root: Path) -> RetrievalRuntimeReadonlyBackendAvailability:
    vendor_path = _vendor_path(project_root, "mgrep")
    dist_entry = vendor_path / "dist" / "index.js"
    source_present = (vendor_path / "package.json").is_file() and (vendor_path / "src" / "index.ts").is_file()
    usable_now = dist_entry.is_file()
    reason = "ready_dist_index_present" if usable_now else "mgrep source is present but dist/index.js executable package is absent"
    return RetrievalRuntimeReadonlyBackendAvailability(
        backend_kind="mgrep",
        vendor_path=str(vendor_path),
        source_present=source_present,
        usable_now=usable_now,
        selected_tool="mgrep_readonly" if usable_now else "repo_search",
        fallback_tool="repo_search",
        unavailable_reason=reason,
    )


def inspect_sqlite_vec_readonly_availability(project_root: Path) -> RetrievalRuntimeReadonlyBackendAvailability:
    vendor_path = _vendor_path(project_root, "sqlite-vec")
    loadable_extensions = tuple(vendor_path.rglob("*.so")) + tuple(vendor_path.rglob("*.dylib")) + tuple(vendor_path.rglob("*.dll"))
    source_present = (vendor_path / "sqlite-vec.c").is_file() and (vendor_path / "README.md").is_file()
    usable_now = bool(loadable_extensions)
    reason = (
        "ready_loadable_extension_present"
        if usable_now
        else "sqlite-vec source is present but no local loadable extension is available"
    )
    return RetrievalRuntimeReadonlyBackendAvailability(
        backend_kind="sqlite_vec",
        vendor_path=str(vendor_path),
        source_present=source_present,
        usable_now=usable_now,
        selected_tool="sqlite_vec_readonly" if usable_now else "repo_search",
        fallback_tool="repo_search",
        unavailable_reason=reason,
    )


def inspect_qdrant_readonly_availability(project_root: Path) -> RetrievalRuntimeReadonlyBackendAvailability:
    vendor_path = _vendor_path(project_root, "qdrant")
    source_present = (vendor_path / "Cargo.toml").is_file() and (vendor_path / "src" / "main.rs").is_file()
    return RetrievalRuntimeReadonlyBackendAvailability(
        backend_kind="qdrant",
        vendor_path=str(vendor_path),
        source_present=source_present,
        usable_now=False,
        selected_tool="qdrant_readonly_status",
        fallback_tool="retrieval_backend_status_read_model",
        unavailable_reason="qdrant source is present but server/container runtime is intentionally disabled",
    )


def build_retrieval_runtime_readonly_availability(project_root: Path) -> tuple[RetrievalRuntimeReadonlyBackendAvailability, ...]:
    return (
        inspect_mgrep_readonly_availability(project_root),
        inspect_sqlite_vec_readonly_availability(project_root),
        inspect_qdrant_readonly_availability(project_root),
    )


__all__ = [
    "RETRIEVAL_VENDOR_ROOT",
    "RetrievalRuntimeReadonlyBackendAvailability",
    "build_retrieval_runtime_readonly_availability",
    "inspect_mgrep_readonly_availability",
    "inspect_qdrant_readonly_availability",
    "inspect_sqlite_vec_readonly_availability",
]
