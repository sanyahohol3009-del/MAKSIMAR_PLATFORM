#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.voice_display_handoff_contract import build_voice_display_handoff_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.voice_normalization_contract import build_voice_normalization_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.voice_routing_contract import build_voice_routing_contract  # noqa: E402


def main() -> None:
    normalization_contract = build_voice_normalization_contract()
    routing_contract = build_voice_routing_contract()
    handoff_contract = build_voice_display_handoff_contract()

    print("VOICE ROUTING PREVIEW")
    print("=" * 180)
    print(
        f"voice_normalization_entries={normalization_contract.total_entries} | "
        f"voice_routing_entries={routing_contract.total_entries} | "
        f"voice_display_handoff_entries={handoff_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
