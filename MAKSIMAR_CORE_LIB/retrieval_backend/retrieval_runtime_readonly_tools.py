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


@dataclass(frozen=True, slots=True)
class RetrievalReadonlyToolRoute:
    route_key: str
    requested_tools: tuple[str, ...]
    selected_tool_chain: tuple[str, ...]
    primary_tool: str
    effective_tool: str
    fallback_tool: str
    fallback_reason: str
    read_only: bool = True
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    direct_execution_allowed: bool = False
    canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    network_allowed_by_default: bool = False

    def __post_init__(self) -> None:
        route_key = _require_text(self.route_key, "route_key")
        if not isinstance(self.requested_tools, tuple) or not self.requested_tools:
            raise ValueError("requested_tools must be a non-empty tuple")
        if not isinstance(self.selected_tool_chain, tuple) or not self.selected_tool_chain:
            raise ValueError("selected_tool_chain must be a non-empty tuple")
        normalized_requested = tuple(_require_text(tool, "requested_tools") for tool in self.requested_tools)
        normalized_chain = tuple(_require_text(tool, "selected_tool_chain") for tool in self.selected_tool_chain)
        primary_tool = _require_text(self.primary_tool, "primary_tool")
        effective_tool = _require_text(self.effective_tool, "effective_tool")
        fallback_tool = _require_text(self.fallback_tool, "fallback_tool")
        fallback_reason = _require_text(self.fallback_reason, "fallback_reason")
        if primary_tool not in normalized_chain:
            raise ValueError("primary_tool must be present in selected_tool_chain")
        if effective_tool not in normalized_chain:
            raise ValueError("effective_tool must be present in selected_tool_chain")
        if fallback_tool not in normalized_chain:
            raise ValueError("fallback_tool must be present in selected_tool_chain")
        for field_name in (
            "read_only",
            "source_ref_required",
            "evidence_binding_required",
            "direct_execution_allowed",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "network_allowed_by_default",
        ):
            _require_bool(getattr(self, field_name), field_name)
        for field_name in ("read_only", "source_ref_required", "evidence_binding_required"):
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} must be True")
        for field_name in (
            "direct_execution_allowed",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "network_allowed_by_default",
        ):
            if getattr(self, field_name):
                raise ValueError(f"{field_name} must be False")
        object.__setattr__(self, "route_key", route_key)
        object.__setattr__(self, "requested_tools", normalized_requested)
        object.__setattr__(self, "selected_tool_chain", normalized_chain)
        object.__setattr__(self, "primary_tool", primary_tool)
        object.__setattr__(self, "effective_tool", effective_tool)
        object.__setattr__(self, "fallback_tool", fallback_tool)
        object.__setattr__(self, "fallback_reason", fallback_reason)

    def to_read_model(self) -> dict[str, object]:
        return {
            "route_key": self.route_key,
            "requested_tools": self.requested_tools,
            "selected_tool_chain": self.selected_tool_chain,
            "primary_tool": self.primary_tool,
            "effective_tool": self.effective_tool,
            "fallback_tool": self.fallback_tool,
            "fallback_reason": self.fallback_reason,
            "read_only": self.read_only,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "direct_execution_allowed": self.direct_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
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


def build_retrieval_readonly_tool_route(
    route_key: str,
    requested_tools: tuple[str, ...],
    project_root: Path,
) -> RetrievalReadonlyToolRoute:
    route_key = _require_text(route_key, "route_key")
    if not isinstance(requested_tools, tuple) or not requested_tools:
        raise ValueError("requested_tools must be a non-empty tuple")
    normalized_requested = tuple(_require_text(tool, "requested_tools") for tool in requested_tools)

    if route_key == "PROJECT_SEARCH" or "mgrep_readonly" in normalized_requested:
        mgrep = inspect_mgrep_readonly_availability(project_root)
        chain = tuple(dict.fromkeys(("mgrep_readonly", mgrep.fallback_tool, *normalized_requested)))
        effective_tool = "mgrep_readonly" if mgrep.usable_now else mgrep.fallback_tool
        return RetrievalReadonlyToolRoute(
            route_key=route_key,
            requested_tools=normalized_requested,
            selected_tool_chain=chain,
            primary_tool="mgrep_readonly",
            effective_tool=effective_tool,
            fallback_tool=mgrep.fallback_tool,
            fallback_reason=mgrep.unavailable_reason,
        )

    if route_key == "SEMANTIC_SIMILARITY" or "sqlite_vec_readonly" in normalized_requested:
        sqlite_vec = inspect_sqlite_vec_readonly_availability(project_root)
        chain = tuple(dict.fromkeys(("sqlite_vec_readonly", sqlite_vec.fallback_tool, *normalized_requested)))
        effective_tool = "sqlite_vec_readonly" if sqlite_vec.usable_now else sqlite_vec.fallback_tool
        return RetrievalReadonlyToolRoute(
            route_key=route_key,
            requested_tools=normalized_requested,
            selected_tool_chain=chain,
            primary_tool="sqlite_vec_readonly",
            effective_tool=effective_tool,
            fallback_tool=sqlite_vec.fallback_tool,
            fallback_reason=sqlite_vec.unavailable_reason,
        )

    if route_key == "RETRIEVAL_BACKEND_STATUS" or "qdrant_readonly_status" in normalized_requested:
        qdrant = inspect_qdrant_readonly_availability(project_root)
        chain = tuple(dict.fromkeys(("qdrant_readonly_status", qdrant.fallback_tool, *normalized_requested)))
        return RetrievalReadonlyToolRoute(
            route_key=route_key,
            requested_tools=normalized_requested,
            selected_tool_chain=chain,
            primary_tool="qdrant_readonly_status",
            effective_tool="qdrant_readonly_status",
            fallback_tool=qdrant.fallback_tool,
            fallback_reason=qdrant.unavailable_reason,
        )

    return RetrievalReadonlyToolRoute(
        route_key=route_key,
        requested_tools=normalized_requested,
        selected_tool_chain=normalized_requested,
        primary_tool=normalized_requested[0],
        effective_tool=normalized_requested[0],
        fallback_tool=normalized_requested[-1],
        fallback_reason="primary read-only tool is available through existing local router",
    )


__all__ = [
    "RETRIEVAL_VENDOR_ROOT",
    "RetrievalRuntimeReadonlyBackendAvailability",
    "RetrievalReadonlyToolRoute",
    "build_retrieval_readonly_tool_route",
    "build_retrieval_runtime_readonly_availability",
    "inspect_mgrep_readonly_availability",
    "inspect_qdrant_readonly_availability",
    "inspect_sqlite_vec_readonly_availability",
]
