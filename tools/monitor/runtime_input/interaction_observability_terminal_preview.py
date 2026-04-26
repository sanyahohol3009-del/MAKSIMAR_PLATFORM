#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.interaction_exposure_contract import build_interaction_exposure_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.interaction_incident_surface_contract import build_interaction_incident_surface_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.interaction_observability_contract import build_interaction_observability_contract  # noqa: E402


def main() -> None:
    exposure_contract = build_interaction_exposure_contract()
    observability_contract = build_interaction_observability_contract()
    incident_surface_contract = build_interaction_incident_surface_contract()

    print("INTERACTION OBSERVABILITY PREVIEW")
    print("=" * 180)
    print(
        f"interaction_exposure_entries={exposure_contract.total_entries} | "
        f"interaction_observability_entries={observability_contract.total_entries} | "
        f"interaction_incident_surface_entries={incident_surface_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
