from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_read_model import (
    build_panel_registry_read_model,
)


def main() -> None:
    read_model = build_panel_registry_read_model()

    print("PANEL REGISTRY PREVIEW")
    print("=" * 100)
    for row in read_model.rows:
        print(
            f"{row.panel_id:<16} | "
            f"{row.panel_family:<12} | "
            f"{row.panel_kind:<10} | "
            f"source={str(row.source_binding_required):<5} | "
            f"visibility={str(row.visibility_policy_required):<5} | "
            f"{row.title}"
        )


if __name__ == "__main__":
    main()
