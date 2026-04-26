#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.preview_consumer_integration_contract import (  # noqa: E402
    build_preview_consumer_integration_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.runtime_data_handoff_integration_contract import (  # noqa: E402
    build_runtime_data_handoff_integration_contract,
)


def main() -> None:
    runtime_contract = build_runtime_data_handoff_integration_contract()
    preview_contract = build_preview_consumer_integration_contract()

    print("RUNTIME / DATA HANDOFF INTEGRATION PREVIEW")
    print("=" * 180)
    print(
        f"runtime_handoff_entries={runtime_contract.total_entries} | "
        f"payload_consistent_entries={runtime_contract.payload_consistent_entries} | "
        f"preview_consumer_entries={preview_contract.total_entries} | "
        f"preview_ready_entries={preview_contract.preview_ready_entries}"
    )


if __name__ == "__main__":
    main()
