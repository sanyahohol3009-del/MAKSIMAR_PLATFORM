from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final


class PathResolverError(RuntimeError):
    """Raised when project path resolution fails."""


@dataclass(frozen=True, slots=True)
class ProjectPaths:
    """Canonical project path map for MAKSIMAR_PLATFORM."""

    project_root: Path

    maksimar_core_lib: Path
    maksimar_server: Path
    jarvis_mobile_android: Path
    jarvis_mobile_ios: Path

    safety_foundation: Path
    oob_monitoring: Path
    observability_layer: Path
    ai_services: Path
    sandbox_execution: Path
    knowledge_system: Path
    research_layer: Path
    memory_system: Path
    workflow_engine: Path
    action_library: Path
    module_system: Path
    codegen_layer: Path
    evaluation_layer: Path
    simulation_layer: Path
    robotics_layer: Path
    cad_3d_cam_layer: Path
    visual_engineering_layer: Path
    energy_operations_layer: Path
    compute_fleet_layer: Path
    vpn_layer: Path
    industrial_layer: Path
    content_media_layer: Path
    dialogue_layer: Path
    voice_layer: Path
    ui_layer: Path
    shared: Path
    server_shell: Path
    desktop_shell: Path
    android_shell: Path
    ios_shell: Path
    packaging: Path
    products: Path
    domain_cubes: Path
    tests: Path
    scripts: Path
    docs: Path
    assets: Path
    requirements: Path

    contracts_root: Path
    governance_contracts: Path
    runtime_contracts: Path
    memory_contracts: Path
    knowledge_contracts: Path
    research_contracts: Path
    workflow_contracts: Path
    action_contracts: Path
    module_contracts: Path
    ui_contracts: Path
    federation_contracts: Path
    product_contracts: Path
    packaging_contracts: Path
    codegen_contracts: Path
    evaluation_contracts: Path
    simulation_contracts: Path
    robotics_contracts: Path
    cad_3d_cam_contracts: Path
    visual_engineering_contracts: Path
    energy_contracts: Path
    compute_fleet_contracts: Path
    vpn_contracts: Path
    industrial_contracts: Path
    content_media_contracts: Path
    dialogue_contracts: Path
    voice_contracts: Path
    mobile_contracts: Path
    shell_contracts: Path

    shared_services: Path


_ROOT_MARKER: Final[str] = ".maksimar_root"


def _find_project_root(start_path: Path) -> Path:
    """Find MAKSIMAR_PLATFORM root by walking upwards.

    Root is identified by explicit root marker file.

    Args:
        start_path: Starting path for upward search.

    Returns:
        Resolved project root path.

    Raises:
        PathResolverError: If the project root cannot be identified.
    """
    current = start_path.resolve()

    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if (candidate / _ROOT_MARKER).is_file():
            return candidate

    raise PathResolverError(
        "Unable to resolve MAKSIMAR_PLATFORM root. "
        f"Expected root marker '{_ROOT_MARKER}' was not found."
    )


def build_project_paths(start_path: Path | None = None) -> ProjectPaths:
    """Build canonical project paths.

    Args:
        start_path: Optional path inside project. If omitted, current file location is used.

    Returns:
        Immutable ProjectPaths mapping.
    """
    anchor = start_path if start_path is not None else Path(__file__)
    root = _find_project_root(anchor)

    contracts_root = root / "MAKSIMAR_CORE" / "contracts"
    core_lib = root / "MAKSIMAR_CORE_LIB"

    return ProjectPaths(
        project_root=root,
        maksimar_core_lib=core_lib,
        maksimar_server=root / "MAKSIMAR_SERVER",
        jarvis_mobile_android=root / "JARVIS_MOBILE_ANDROID",
        jarvis_mobile_ios=root / "JARVIS_MOBILE_IOS",
        safety_foundation=root / "SAFETY_FOUNDATION",
        oob_monitoring=root / "OOB_MONITORING",
        observability_layer=root / "OBSERVABILITY_LAYER",
        ai_services=root / "AI_SERVICES",
        sandbox_execution=root / "SANDBOX_EXECUTION",
        knowledge_system=root / "KNOWLEDGE_SYSTEM",
        research_layer=root / "RESEARCH_LAYER",
        memory_system=root / "MEMORY_SYSTEM",
        workflow_engine=root / "WORKFLOW_ENGINE",
        action_library=root / "ACTION_LIBRARY",
        module_system=root / "MODULE_SYSTEM",
        codegen_layer=root / "CODEGEN_LAYER",
        evaluation_layer=root / "EVALUATION_LAYER",
        simulation_layer=root / "SIMULATION_LAYER",
        robotics_layer=root / "ROBOTICS_LAYER",
        cad_3d_cam_layer=root / "CAD_3D_CAM_LAYER",
        visual_engineering_layer=root / "VISUAL_ENGINEERING_LAYER",
        energy_operations_layer=root / "ENERGY_OPERATIONS_LAYER",
        compute_fleet_layer=root / "COMPUTE_FLEET_LAYER",
        vpn_layer=root / "VPN_LAYER",
        industrial_layer=root / "INDUSTRIAL_LAYER",
        content_media_layer=root / "CONTENT_MEDIA_LAYER",
        dialogue_layer=root / "DIALOGUE_LAYER",
        voice_layer=root / "VOICE_LAYER",
        ui_layer=root / "UI_LAYER",
        shared=root / "SHARED",
        server_shell=root / "SERVER_SHELL",
        desktop_shell=root / "DESKTOP_SHELL",
        android_shell=root / "ANDROID_SHELL",
        ios_shell=root / "IOS_SHELL",
        packaging=root / "PACKAGING",
        products=root / "PRODUCTS",
        domain_cubes=root / "DOMAIN_CUBES",
        tests=root / "tests",
        scripts=root / "scripts",
        docs=root / "docs",
        assets=root / "assets",
        requirements=root / "requirements",
        contracts_root=contracts_root,
        governance_contracts=contracts_root / "governance",
        runtime_contracts=contracts_root / "runtime",
        memory_contracts=contracts_root / "memory",
        knowledge_contracts=contracts_root / "knowledge",
        research_contracts=contracts_root / "research",
        workflow_contracts=contracts_root / "workflow",
        action_contracts=contracts_root / "action",
        module_contracts=contracts_root / "module",
        ui_contracts=contracts_root / "ui",
        federation_contracts=contracts_root / "federation",
        product_contracts=contracts_root / "product",
        packaging_contracts=contracts_root / "packaging",
        codegen_contracts=contracts_root / "codegen",
        evaluation_contracts=contracts_root / "evaluation",
        simulation_contracts=contracts_root / "simulation",
        robotics_contracts=contracts_root / "robotics",
        cad_3d_cam_contracts=contracts_root / "cad_3d_cam",
        visual_engineering_contracts=contracts_root / "visual_engineering",
        energy_contracts=contracts_root / "energy",
        compute_fleet_contracts=contracts_root / "compute_fleet",
        vpn_contracts=contracts_root / "vpn",
        industrial_contracts=contracts_root / "industrial",
        content_media_contracts=contracts_root / "content_media",
        dialogue_contracts=contracts_root / "dialogue",
        voice_contracts=contracts_root / "voice",
        mobile_contracts=contracts_root / "mobile",
        shell_contracts=contracts_root / "shell",
        shared_services=core_lib / "shared_services",
    )


PATHS: Final[ProjectPaths] = build_project_paths()


def ensure_directory(path: Path) -> Path:
    """Ensure directory exists.

    Args:
        path: Directory path to create.

    Returns:
        Same path after creation.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
