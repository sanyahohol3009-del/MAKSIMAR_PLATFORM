from __future__ import annotations

from collections import defaultdict

from MAKSIMAR_CORE_LIB.contract_validation.models import ContractCheckResult


def apply_cross_file_rules(results: list[ContractCheckResult]) -> None:
    """Apply cross-file rules in-place to validation results.

    Rules:
    - duplicate contract_name is forbidden
    - duplicate schema_version is forbidden

    Args:
        results: Per-file validation results to enrich in-place.
    """
    by_contract_name: dict[str, list[ContractCheckResult]] = defaultdict(list)
    by_schema_version: dict[str, list[ContractCheckResult]] = defaultdict(list)

    for result in results:
        if result.contract_name:
            by_contract_name[result.contract_name].append(result)
        if result.schema_version:
            by_schema_version[result.schema_version].append(result)

    for contract_name, grouped_results in by_contract_name.items():
        if len(grouped_results) > 1:
            duplicate_paths = ", ".join(str(result.file_path) for result in grouped_results)
            for result in grouped_results:
                result.add_error(
                    "contract_name",
                    f"Duplicate contract_name '{contract_name}' found in: {duplicate_paths}",
                )

    for schema_version, grouped_results in by_schema_version.items():
        if len(grouped_results) > 1:
            duplicate_paths = ", ".join(str(result.file_path) for result in grouped_results)
            for result in grouped_results:
                result.add_error(
                    "schema_version",
                    f"Duplicate schema_version '{schema_version}' found in: {duplicate_paths}",
                )
