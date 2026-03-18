from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


@dataclass(frozen=True, slots=True)
class ConfigRootEntry:
    """Canonical registry entry for one config root."""

    name: str
    path: Path


def get_config_roots() -> list[ConfigRootEntry]:
    """Return canonical ordered registry of all known config roots.

    Returns:
        Ordered config root registry.
    """
    project_root = PATHS.project_root

    return [
        ConfigRootEntry(name="memory_system", path=PATHS.memory_system / "config"),
        ConfigRootEntry(name="knowledge_system", path=PATHS.knowledge_system / "config"),
        ConfigRootEntry(name="research_layer", path=PATHS.research_layer / "config"),
        ConfigRootEntry(name="workflow_engine", path=PATHS.workflow_engine / "config"),
        ConfigRootEntry(name="action_library", path=PATHS.action_library / "config"),
        ConfigRootEntry(name="module_system", path=PATHS.module_system / "config"),
        ConfigRootEntry(name="codegen_layer", path=PATHS.codegen_layer / "config"),
        ConfigRootEntry(name="evaluation_layer", path=PATHS.evaluation_layer / "config"),
        ConfigRootEntry(name="simulation_layer", path=PATHS.simulation_layer / "config"),
        ConfigRootEntry(name="robotics_layer", path=PATHS.robotics_layer / "config"),
        ConfigRootEntry(name="cad_3d_cam_layer", path=PATHS.cad_3d_cam_layer / "config"),
        ConfigRootEntry(
            name="visual_engineering_layer",
            path=PATHS.visual_engineering_layer / "config",
        ),
        ConfigRootEntry(
            name="energy_operations_layer",
            path=PATHS.energy_operations_layer / "config",
        ),
        ConfigRootEntry(
            name="compute_fleet_layer",
            path=PATHS.compute_fleet_layer / "config",
        ),
        ConfigRootEntry(name="vpn_layer", path=PATHS.vpn_layer / "config"),
        ConfigRootEntry(name="industrial_layer", path=PATHS.industrial_layer / "config"),
        ConfigRootEntry(
            name="content_media_layer",
            path=PATHS.content_media_layer / "config",
        ),
        ConfigRootEntry(name="dialogue_layer", path=PATHS.dialogue_layer / "config"),
        ConfigRootEntry(name="voice_layer", path=PATHS.voice_layer / "config"),
        ConfigRootEntry(name="ui_layer", path=PATHS.ui_layer / "config"),
        ConfigRootEntry(name="shared", path=PATHS.shared / "config"),
        ConfigRootEntry(
            name="governance_config",
            path=project_root / "MAKSIMAR_CORE" / "governance" / "config",
        ),
        ConfigRootEntry(name="shell_layer", path=project_root / "SHELL_LAYER" / "config"),
    ]
