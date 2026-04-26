#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_adapter_contract import build_gesture_adapter_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_input_contract import build_gesture_input_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_policy_handoff_contract import build_gesture_policy_handoff_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_preprocessing_contract import build_gesture_preprocessing_contract  # noqa: E402


def main() -> None:
    input_contract = build_gesture_input_contract()
    preprocessing_contract = build_gesture_preprocessing_contract()
    adapter_contract = build_gesture_adapter_contract()
    handoff_contract = build_gesture_policy_handoff_contract()

    print("GESTURE FLOW PREVIEW")
    print("=" * 180)
    print(
        f"gesture_input_entries={input_contract.total_entries} | "
        f"gesture_preprocessing_entries={preprocessing_contract.total_entries} | "
        f"gesture_adapter_entries={adapter_contract.total_entries} | "
        f"gesture_policy_handoff_entries={handoff_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
