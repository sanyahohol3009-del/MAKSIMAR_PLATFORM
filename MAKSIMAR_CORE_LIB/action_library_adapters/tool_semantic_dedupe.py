from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.universal_tool_manifest import UniversalToolManifest


def normalize_tool_name(name: str) -> str:
    return "".join(ch for ch in str(name).casefold() if ch.isalnum())


def manifests_are_semantic_duplicates(left: UniversalToolManifest, right: UniversalToolManifest) -> bool:
    if left.semantic_fingerprint == right.semantic_fingerprint:
        return True
    if normalize_tool_name(left.tool_id) == normalize_tool_name(right.tool_id):
        return True
    if left.capability_id == right.capability_id:
        left_aliases = set(left.normalized_aliases()) | {normalize_tool_name(left.tool_id)}
        right_aliases = set(right.normalized_aliases()) | {normalize_tool_name(right.tool_id)}
        if left_aliases & right_aliases:
            return True
    return False


def dedupe_tool_manifests(
    manifests: tuple[UniversalToolManifest, ...],
) -> tuple[tuple[UniversalToolManifest, ...], tuple[str, ...]]:
    unique: list[UniversalToolManifest] = []
    duplicates: list[str] = []
    for manifest in manifests:
        if any(manifests_are_semantic_duplicates(existing, manifest) for existing in unique):
            duplicates.append(manifest.tool_id)
            continue
        unique.append(manifest)
    return tuple(unique), tuple(duplicates)
