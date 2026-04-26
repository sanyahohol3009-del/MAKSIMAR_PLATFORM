#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.export_status_panel_contract import (  # noqa: E402
    build_export_status_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.project_assets_panel_contract import (  # noqa: E402
    build_project_assets_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.validation_assets_panel_contract import (  # noqa: E402
    build_validation_assets_panel_contract,
)


def main() -> None:
    export_status_contract = build_export_status_panel_contract()
    validation_assets_contract = build_validation_assets_panel_contract()
    project_assets_contract = build_project_assets_panel_contract()

    print("EXPORT / VALIDATION / ASSETS FAMILY PREVIEW")
    print("=" * 180)
    print(
        f"export_status_entries={export_status_contract.total_entries} | "
        f"validation_assets_entries={validation_assets_contract.total_entries} | "
        f"project_assets_entries={project_assets_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
