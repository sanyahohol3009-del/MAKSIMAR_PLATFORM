#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_adapter_canonical_identity_compliance_contract import (  # noqa: E402
    build_visual_adapter_canonical_identity_compliance_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_adapter_vendor_leakage_compliance_contract import (  # noqa: E402
    build_visual_adapter_vendor_leakage_compliance_contract,
)


def main() -> None:
    vendor_contract = build_visual_adapter_vendor_leakage_compliance_contract()
    identity_contract = build_visual_adapter_canonical_identity_compliance_contract()

    print("VISUAL ADAPTER COMPLIANCE PREVIEW")
    print("=" * 180)
    print(
        f"vendor_leakage_entries={vendor_contract.total_entries} | "
        f"vendor_compliance_passed_entries={vendor_contract.compliance_passed_entries} | "
        f"identity_entries={identity_contract.total_entries} | "
        f"identity_compliance_passed_entries={identity_contract.compliance_passed_entries}"
    )


if __name__ == "__main__":
    main()
