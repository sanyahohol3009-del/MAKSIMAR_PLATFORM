from __future__ import annotations

import argparse
import ast
import difflib
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


GROUP_ORDER: tuple[str, ...] = (
    "foundation",
    "operator",
    "display",
    "visual",
    "other",
)

GROUP_TO_FILENAME: dict[str, str] = {
    "foundation": "exports_foundation.py",
    "operator": "exports_operator.py",
    "display": "exports_display.py",
    "visual": "exports_visual.py",
    "other": "exports_other.py",
}

GROUP_HEADERS: dict[str, str] = {
    "foundation": "Foundation and OOB monitoring exports.",
    "operator": "Operator interaction and operator-visible exports.",
    "display": "Display, monitor, routing, restore, and projection exports.",
    "visual": "Visual shell, HUD, rendering, preview, and presentation exports.",
    "other": "Exports that are intentionally preserved but not yet classified into a canonical group.",
}

INIT_IMPORT_ORDER: tuple[str, ...] = (
    "foundation",
    "operator",
    "display",
    "visual",
    "other",
)

TARGET_PACKAGE = "MAKSIMAR_CORE_LIB.oob_dashboard"
TARGET_INIT_RELATIVE_PATH = Path("MAKSIMAR_CORE_LIB/oob_dashboard/__init__.py")


@dataclass(frozen=True, slots=True)
class ImportBlock:
    """A single top-level import block from the target __init__.py."""

    module_path: str
    raw_text: str
    imported_names: tuple[str, ...]
    group_name: str

    def __post_init__(self) -> None:
        _require_non_empty(self.module_path, "module_path")
        _require_non_empty(self.raw_text, "raw_text")
        _require_non_empty(self.group_name, "group_name")

        if not self.imported_names:
            raise ValueError("imported_names must not be empty.")

        if self.group_name not in GROUP_ORDER:
            raise ValueError(
                f"group_name must be one of {GROUP_ORDER}, got {self.group_name!r}."
            )


@dataclass(frozen=True, slots=True)
class RefactorPlan:
    """Refactor plan for export-surface normalization."""

    target_init_path: Path
    backup_init_path: Path
    parsed_blocks: tuple[ImportBlock, ...]
    all_export_names: tuple[str, ...]
    grouped_export_names: dict[str, tuple[str, ...]]
    grouped_blocks: dict[str, tuple[ImportBlock, ...]]
    generated_files: dict[str, Path]
    new_init_content: str

    def __post_init__(self) -> None:
        if not self.target_init_path.exists():
            raise ValueError("target_init_path must exist.")

        if not self.parsed_blocks:
            raise ValueError("parsed_blocks must not be empty.")

        if not self.all_export_names:
            raise ValueError("all_export_names must not be empty.")

        for group_name in GROUP_ORDER:
            if group_name not in self.grouped_export_names:
                raise ValueError(f"Missing grouped_export_names entry for {group_name}.")
            if group_name not in self.grouped_blocks:
                raise ValueError(f"Missing grouped_blocks entry for {group_name}.")


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def _normalize_newlines(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n")


def _extract_all_list_literal(source_text: str) -> tuple[list[str], str]:
    marker = "__all__ = ["
    start = source_text.find(marker)
    if start == -1:
        raise ValueError("Could not locate __all__ = [ in target __init__.py.")

    bracket_start = source_text.find("[", start)
    if bracket_start == -1:
        raise ValueError("Could not locate opening [ for __all__ list.")

    index = bracket_start
    depth = 0
    end = -1
    while index < len(source_text):
        char = source_text[index]
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                end = index
                break
        index += 1

    if end == -1:
        raise ValueError("Could not locate closing ] for __all__ list.")

    raw_list_block = source_text[start : end + 1]
    raw_list_literal = source_text[bracket_start : end + 1]

    try:
        parsed = ast.literal_eval(raw_list_literal)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"Could not parse __all__ list literal safely: {exc}") from exc

    if not isinstance(parsed, list):
        raise ValueError("__all__ must parse to a list.")

    export_names = []
    for item in parsed:
        if not isinstance(item, str):
            raise ValueError("__all__ must contain only strings.")
        export_names.append(item)

    if not export_names:
        raise ValueError("Extracted __all__ is empty.")

    return export_names, raw_list_block


def _extract_import_section(source_text: str, all_block_text: str) -> str:
    marker = "from MAKSIMAR_CORE_LIB.oob_dashboard"
    first_import_index = source_text.find(marker)
    if first_import_index == -1:
        raise ValueError("Could not locate target oob_dashboard import section.")

    all_index = source_text.find(all_block_text)
    if all_index == -1:
        raise ValueError("Could not align import section with __all__ block.")

    import_section = source_text[first_import_index:all_index].rstrip()
    if not import_section:
        raise ValueError("Import section is empty.")

    return import_section


def _split_import_blocks(import_section: str) -> list[str]:
    blocks: list[str] = []
    current_lines: list[str] = []

    for line in import_section.splitlines():
        if line.startswith("from MAKSIMAR_CORE_LIB.oob_dashboard.") and current_lines:
            blocks.append("\n".join(current_lines).rstrip())
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        blocks.append("\n".join(current_lines).rstrip())

    return [block for block in blocks if block.strip()]


def _parse_imported_names(block_text: str) -> tuple[str, tuple[str, ...]]:
    lines = block_text.splitlines()
    first_line = lines[0].strip()

    prefix = "from "
    middle = " import ("
    if not first_line.startswith(prefix) or middle not in first_line:
        raise ValueError(f"Unexpected import block start: {first_line!r}")

    module_path = first_line[len(prefix) : first_line.index(middle)].strip()
    imported_names: list[str] = []

    for raw_line in lines[1:]:
        stripped = raw_line.strip()
        if stripped == ")":
            continue
        if stripped.endswith(","):
            stripped = stripped[:-1].strip()
        if stripped:
            imported_names.append(stripped)

    if not imported_names:
        raise ValueError(f"No imported names parsed for module {module_path!r}.")

    return module_path, tuple(imported_names)


def _classify_group(module_path: str, imported_names: tuple[str, ...]) -> str:
    lower_module = module_path.lower()
    lowered_names = " ".join(imported_names).lower()

    foundation_markers = (
        "foundation_",
        "consistency_panel",
        "incident_view",
        "diagnostics_",
        "snapshot_aggregator",
        "dashboard_models",
        "chat_contract",
        "chat_models",
        "chat_input_",
        "input_contract",
        "input_models",
        "input_router_contract",
        "feedback_",
        "dashboard_shell_",
        "workspace_contract",
        "workspace_models",
        "navigation_",
        "panel_registry_",
        "view_composition_",
        "settings_panel_",
        "gesture_panel_",
        "queue_load_panel_",
        "node_topology_panel_",
        "degraded_mode_panel_",
        "project_map_panel_",
        "data_flow_panel_",
        "dependency_map_panel_",
        "version_control_panel_",
        "dashboard_execution_shell_",
        "panel_identity_",
        "panel_metadata_",
        "panel_taxonomy_",
        "panel_source_binding_",
        "panel_exposure_policy_",
        "panel_content_",
        "panel_binding_",
        "view_targeting_",
        "panel_view_display_chain_",
        "workspace_registry_",
        "layout_composition_",
        "workspace_read_model_",
        "panel_zone_slot_vocabulary_",
        "main_operator_dashboard_contract",
        "main_operator_dashboard_read_model_contract",
        "operator_workspace_binding_contract",
        "operator_interaction_guard_contract",
        "control_plane_handoff_contract",
        "policy_aware_action_exposure_contract",
        "system_status_panel_content_contract",
        "guard_chain_panel_content_contract",
        "incidents_panel_content_contract",
        "logs_panel_content_contract",
        "topology_panel_content_contract",
        "panel_orchestration_contract",
        "panel_orchestration_models",
        "panel_orchestration_contract",
        "panel_orchestration_models",
    )

    operator_markers = (
        "operator_intent_",
        "panel_operator_intent_binding_",
        "operator_approval_decision_",
        "operator_control_plane_handoff_",
        "operator_audit_visibility_",
        "operator_interaction_read_model_",
        "main_operator_interaction_surface_",
        "operator_action_queue_panel_",
        "operator_approval_queue_panel_",
        "operator_audit_timeline_panel_",
        "operator_visible_presentation_",
        "operator_presentation_bundle_",
        "operator_dashboard_visible_state_",
        "operator_dashboard_screen_state_",
        "operator_dashboard_render_handoff_",
        "operator_dashboard_visible_snapshot_",
        "operator_dashboard_first_honest_view_",
        "operator_dashboard_visible_output_",
        "operator_dashboard_first_real_picture_",
        "operator_dashboard_final_assembled_state_",
        "operator_dashboard_first_system_view_artifact_",
        "operator_dashboard_operator_surface_export_",
        "operator_dashboard_visual_shell_ready_",
    )

    display_markers = (
        "display_target_vocabulary_",
        "display_runtime_resolver_integration_",
        "display_assignment_registry_",
        "display_assignment_restore_",
        "display_conflict_resolution_",
        "display_continuity_snapshot_",
        "display_occupancy_",
        "display_placement_routing_",
        "display_replacement_policy_",
        "display_resolver_decision_",
        "display_restore_continuity_",
        "display_visual_projection_",
        "free_display_selection_",
        "monitor_inventory_",
    )

    visual_markers = (
        "visual_",
        "panel_to_visual_mapping_",
    )

    if any(marker in lower_module for marker in visual_markers):
        return "visual"
    if any(marker in lower_module for marker in display_markers):
        return "display"
    if any(marker in lower_module for marker in operator_markers):
        return "operator"
    if any(marker in lower_module for marker in foundation_markers):
        return "foundation"

    if "visual" in lowered_names:
        return "visual"
    if "display" in lowered_names or "monitor" in lowered_names:
        return "display"
    if "operator" in lowered_names:
        return "operator"

    return "other"


def _build_import_blocks(import_section: str) -> tuple[ImportBlock, ...]:
    parsed_blocks: list[ImportBlock] = []

    for raw_block in _split_import_blocks(import_section):
        module_path, imported_names = _parse_imported_names(raw_block)
        group_name = _classify_group(module_path, imported_names)
        parsed_blocks.append(
            ImportBlock(
                module_path=module_path,
                raw_text=raw_block,
                imported_names=imported_names,
                group_name=group_name,
            )
        )

    if not parsed_blocks:
        raise ValueError("No import blocks parsed from target __init__.py.")

    return tuple(parsed_blocks)


def _group_blocks(blocks: Iterable[ImportBlock]) -> dict[str, tuple[ImportBlock, ...]]:
    grouped: dict[str, list[ImportBlock]] = {group: [] for group in GROUP_ORDER}
    for block in blocks:
        grouped.setdefault(block.group_name, []).append(block)

    return {group: tuple(grouped.get(group, [])) for group in GROUP_ORDER}


def _group_export_names(
    grouped_blocks: dict[str, tuple[ImportBlock, ...]]
) -> dict[str, tuple[str, ...]]:
    result: dict[str, tuple[str, ...]] = {}

    for group_name, blocks in grouped_blocks.items():
        seen: set[str] = set()
        ordered_names: list[str] = []
        for block in blocks:
            for imported_name in block.imported_names:
                if imported_name not in seen:
                    seen.add(imported_name)
                    ordered_names.append(imported_name)
        result[group_name] = tuple(ordered_names)

    return result


def _render_aggregator_module(group_name: str, blocks: tuple[ImportBlock, ...]) -> str:
    if group_name not in GROUP_TO_FILENAME:
        raise ValueError(f"Unsupported group for aggregator rendering: {group_name}")

    header = GROUP_HEADERS[group_name]
    export_names: list[str] = []
    for block in blocks:
        export_names.extend(block.imported_names)

    unique_export_names: list[str] = []
    seen: set[str] = set()
    for name in export_names:
        if name not in seen:
            seen.add(name)
            unique_export_names.append(name)

    lines: list[str] = [
        "from __future__ import annotations",
        "",
        f'"""',
        header,
        '"""',
        "",
    ]

    for index, block in enumerate(blocks):
        lines.append(block.raw_text)
        if index != len(blocks) - 1:
            lines.append("")

    lines.append("")
    lines.append("__all__ = [")
    for name in unique_export_names:
        lines.append(f'    "{name}",')
    lines.append("]")
    lines.append("")

    return "\n".join(lines)


def _render_new_init(
    grouped_export_names: dict[str, tuple[str, ...]],
    original_export_names: tuple[str, ...],
) -> str:
    lines: list[str] = [
        "from __future__ import annotations",
        "",
        '"""',
        "Canonical top-level export surface for oob_dashboard.",
        "",
        "This file intentionally re-exports grouped canonical export modules only.",
        "Do not add new dashboard exports here blindly.",
        "Add them to the appropriate grouped export module first.",
        '"""',
        "",
    ]

    for group_name in INIT_IMPORT_ORDER:
        if grouped_export_names[group_name]:
            module_name = GROUP_TO_FILENAME[group_name].replace(".py", "")
            lines.append(f"from {TARGET_PACKAGE}.{module_name} import *")

    lines.append("")
    lines.append("__all__ = [")
    for name in original_export_names:
        lines.append(f'    "{name}",')
    lines.append("]")
    lines.append("")

    return "\n".join(lines)


def _make_backup_path(path: Path) -> Path:
    return path.with_name(path.name + ".bak")


def _build_plan(project_root: Path) -> RefactorPlan:
    target_init_path = project_root / TARGET_INIT_RELATIVE_PATH
    if not target_init_path.exists():
        raise FileNotFoundError(f"Target file does not exist: {target_init_path}")

    source_text = _normalize_newlines(_read_text(target_init_path))
    all_export_names, raw_all_block = _extract_all_list_literal(source_text)
    import_section = _extract_import_section(source_text, raw_all_block)
    parsed_blocks = _build_import_blocks(import_section)
    grouped_blocks = _group_blocks(parsed_blocks)
    grouped_export_names = _group_export_names(grouped_blocks)

    generated_files = {
        group_name: target_init_path.with_name(filename)
        for group_name, filename in GROUP_TO_FILENAME.items()
    }

    new_init_content = _render_new_init(
    grouped_export_names,
    tuple(all_export_names),
)

    return RefactorPlan(
        target_init_path=target_init_path,
        backup_init_path=_make_backup_path(target_init_path),
        parsed_blocks=parsed_blocks,
        all_export_names=tuple(all_export_names),
        grouped_export_names=grouped_export_names,
        grouped_blocks=grouped_blocks,
        generated_files=generated_files,
        new_init_content=new_init_content,
    )


def _print_plan(plan: RefactorPlan) -> None:
    print(f"Target init: {plan.target_init_path}")
    print(f"Backup init: {plan.backup_init_path}")
    print(f"Parsed import blocks: {len(plan.parsed_blocks)}")
    print(f"Existing __all__ size: {len(plan.all_export_names)}")
    print("")

    for group_name in GROUP_ORDER:
        blocks = plan.grouped_blocks[group_name]
        names = plan.grouped_export_names[group_name]
        out_path = plan.generated_files[group_name]
        print(
            f"[{group_name}] blocks={len(blocks)} names={len(names)} "
            f"file={out_path.name}"
        )

    print("")
    if plan.grouped_export_names["other"]:
        print("WARNING: Unclassified exports remain in group 'other':")
        for name in plan.grouped_export_names["other"]:
            print(f"  - {name}")
        print("")


def _print_diff(old_text: str, new_text: str, from_name: str, to_name: str) -> None:
    diff = difflib.unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        fromfile=from_name,
        tofile=to_name,
        lineterm="",
    )
    for line in diff:
        print(line)


def _render_all_group_files(plan: RefactorPlan) -> dict[str, str]:
    rendered: dict[str, str] = {}
    for group_name, output_path in plan.generated_files.items():
        blocks = plan.grouped_blocks[group_name]
        rendered[group_name] = _render_aggregator_module(group_name, blocks)
        if not blocks:
            # Keep empty aggregator modules valid and explicit.
            rendered[group_name] = (
                "from __future__ import annotations\n\n"
                f'"""{GROUP_HEADERS[group_name]}"""\n\n'
                "__all__ = []\n"
            )
    return rendered


def _validate_export_equivalence(plan: RefactorPlan) -> None:
    old_exports = tuple(plan.all_export_names)
    new_exports: list[str] = []

    for group_name in INIT_IMPORT_ORDER:
        new_exports.extend(plan.grouped_export_names[group_name])

    old_counter = Counter(old_exports)
    new_counter = Counter(new_exports)

    if old_counter != new_counter:
        missing: list[str] = []
        extra: list[str] = []

        for name, count in old_counter.items():
            diff = count - new_counter.get(name, 0)
            if diff > 0:
                missing.extend([name] * diff)

        for name, count in new_counter.items():
            diff = count - old_counter.get(name, 0)
            if diff > 0:
                extra.extend([name] * diff)

        details: list[str] = []
        if missing:
            details.append(f"missing={missing!r}")
        if extra:
            details.append(f"extra={extra!r}")

        raise ValueError(
            "Export surface mismatch after regrouping. "
            "The new grouped exports do not preserve original export membership. "
            + " ".join(details)
        )


def _backup_file(path: Path) -> Path:
    backup_path = _make_backup_path(path)
    shutil.copy2(path, backup_path)
    return backup_path


def _apply(plan: RefactorPlan, create_backups: bool) -> None:
    _validate_export_equivalence(plan)

    rendered_group_files = _render_all_group_files(plan)

    if create_backups:
        _backup_file(plan.target_init_path)

    old_init_text = _normalize_newlines(_read_text(plan.target_init_path))
    for group_name, output_path in plan.generated_files.items():
        if output_path.exists() and create_backups:
            _backup_file(output_path)

        _write_text(output_path, rendered_group_files[group_name])

    _write_text(plan.target_init_path, plan.new_init_content)

    print("Applied export-surface refactor.")
    print("")
    print("Diff for __init__.py:")
    print("")
    _print_diff(
        old_init_text,
        plan.new_init_content,
        str(plan.target_init_path),
        str(plan.target_init_path),
    )


def _validate_files(plan: RefactorPlan) -> None:
    if not plan.target_init_path.exists():
        raise ValueError("Target __init__.py is missing after refactor.")

    for output_path in plan.generated_files.values():
        if not output_path.exists():
            raise ValueError(f"Generated export file missing: {output_path}")

    init_text = _normalize_newlines(_read_text(plan.target_init_path))
    if "from MAKSIMAR_CORE_LIB.oob_dashboard.exports_foundation import *" not in init_text:
        raise ValueError("New __init__.py is missing exports_foundation import.")
    if "from MAKSIMAR_CORE_LIB.oob_dashboard.exports_operator import *" not in init_text:
        raise ValueError("New __init__.py is missing exports_operator import.")
    if "from MAKSIMAR_CORE_LIB.oob_dashboard.exports_display import *" not in init_text:
        raise ValueError("New __init__.py is missing exports_display import.")
    if "from MAKSIMAR_CORE_LIB.oob_dashboard.exports_visual import *" not in init_text:
        raise ValueError("New __init__.py is missing exports_visual import.")

    print("Validation passed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Safe export-surface refactor for "
            "MAKSIMAR_CORE_LIB/oob_dashboard/__init__.py"
        )
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Path to project root. Default: current directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze and print the refactor plan without changing files.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the export-surface refactor.",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create .bak backups before overwriting files.",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate generated files after apply or against current state.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()

    if not args.dry_run and not args.apply and not args.validate:
        print("Nothing to do. Use --dry-run, --apply, and/or --validate.")
        return 1

    try:
        plan = _build_plan(project_root)

        if args.dry_run:
            print("=== DRY RUN ===")
            _print_plan(plan)
            print("Preview of new __init__.py:")
            print("")
            print(plan.new_init_content)

        if args.apply:
            print("=== APPLY ===")
            _apply(plan, create_backups=args.backup)

        if args.validate:
            print("=== VALIDATE ===")
            refreshed_plan = _build_plan(project_root)
            _validate_export_equivalence(refreshed_plan)
            _validate_files(refreshed_plan)

    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
