#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_bundle_contract import build_base_family_bundle_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_manifest_contract import build_base_family_manifest_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_mount_plan_contract import build_base_family_mount_plan_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_readiness_contract import build_base_family_readiness_contract  # noqa: E402


def main() -> None:
    manifest = build_base_family_manifest_contract()
    bundle = build_base_family_bundle_contract()
    mount = build_base_family_mount_plan_contract()
    readiness = build_base_family_readiness_contract()

    print("BASE FAMILY COMPOSITION PREVIEW")
    print("=" * 180)
    print(
        f"manifest_total={manifest.total_entries} | "
        f"bundle_total={bundle.total_entries} | "
        f"mount_plan_total={mount.total_entries} | "
        f"readiness_total={readiness.total_entries}"
    )


if __name__ == "__main__":
    main()
