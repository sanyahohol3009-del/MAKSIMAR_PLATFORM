from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.contract_validation.validator import validate_contract_root
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


def main() -> int:
    """Run contract validation engine against canonical contracts root."""
    contracts_root: Path = PATHS.contracts_root
    results, summary = validate_contract_root(contracts_root)

    print("== CONTRACT VALIDATION ENGINE ==")
    print(f"contracts_root: {contracts_root}")
    print(f"total_files: {summary.total_files}")
    print(f"valid_files: {summary.valid_files}")
    print(f"invalid_files: {summary.invalid_files}")
    print(f"warning_count: {summary.warning_count}")
    print(f"error_count: {summary.error_count}")

    for result in results:
        status = "OK" if result.is_valid else "INVALID"
        print(f"[{status}] {result.file_path}")
        for issue in result.issues:
            print(f"  - {issue.level}: {issue.path}: {issue.message}")

    return 1 if summary.invalid_files > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
