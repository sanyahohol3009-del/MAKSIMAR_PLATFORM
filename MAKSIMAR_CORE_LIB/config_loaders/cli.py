from __future__ import annotations

from MAKSIMAR_CORE_LIB.config_loaders.loader import load_config_root
from MAKSIMAR_CORE_LIB.config_loaders.root_registry import get_config_roots


def main() -> int:
    """Run config loader over all canonical config roots."""
    total_files = 0
    valid_files = 0
    invalid_files = 0
    warning_count = 0
    error_count = 0

    print("== CORE CONFIG LOADERS ==")

    for entry in get_config_roots():
        results, summary = load_config_root(entry.path)
        print(f"[ROOT] {entry.name}: {entry.path}")
        print(
            f"  total={summary.total_files} "
            f"valid={summary.valid_files} "
            f"invalid={summary.invalid_files} "
            f"warnings={summary.warning_count} "
            f"errors={summary.error_count}"
        )

        for result in results:
            status = "OK" if result.is_valid else "INVALID"
            print(f"  [{status}] {result.file_path}")
            for issue in result.issues:
                print(f"    - {issue.level}: {issue.path}: {issue.message}")

        total_files += summary.total_files
        valid_files += summary.valid_files
        invalid_files += summary.invalid_files
        warning_count += summary.warning_count
        error_count += summary.error_count

    print("== SUMMARY ==")
    print(f"total_files: {total_files}")
    print(f"valid_files: {valid_files}")
    print(f"invalid_files: {invalid_files}")
    print(f"warning_count: {warning_count}")
    print(f"error_count: {error_count}")

    return 1 if invalid_files > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
