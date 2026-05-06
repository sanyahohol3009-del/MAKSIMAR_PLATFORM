from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.canonical_mapping import (
    build_history_track_freeze_manifest,
)


def build_canonical_freeze_summary() -> Dict[str, object]:
    manifest = build_history_track_freeze_manifest()
    canonical_mapping = manifest["canonical_mapping"]

    canonical_phase_keys = tuple(
        key for key in canonical_mapping.keys() if key != "support_only_noncanonical_helpers"
    )

    return {
        "track_name": manifest["track_name"],
        "freeze_ready": manifest["freeze_ready"],
        "canonical_phase_count": manifest["canonical_phase_count"],
        "support_phase_count": manifest["support_phase_count"],
        "first_canonical_phase": canonical_phase_keys[0],
        "last_canonical_phase": canonical_phase_keys[-1],
        "support_bucket": "support_only_noncanonical_helpers",
    }
