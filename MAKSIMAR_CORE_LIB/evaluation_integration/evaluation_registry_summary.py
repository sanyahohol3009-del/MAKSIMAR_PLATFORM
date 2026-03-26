from __future__ import annotations

from MAKSIMAR_CORE_LIB.evaluation_integration.evaluation_models import (
    EvaluationDefinitionRecord,
    EvaluationRegistrySummary,
)
from MAKSIMAR_CORE_LIB.shared_services.atomic_io import safe_read_yaml
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


def build_evaluation_registry_summary() -> EvaluationRegistrySummary:
    """Build unified evaluation registry summary from evaluation contracts."""
    root = PATHS.contracts_root / "evaluation"
    records: list[EvaluationDefinitionRecord] = []

    if not root.exists() or not root.is_dir():
        return EvaluationRegistrySummary(total_evaluations=0, records=[])

    for file_path in sorted(root.glob("*.yaml")):
        if not file_path.is_file():
            continue

        payload = safe_read_yaml(file_path)

        contract_name = payload.get("contract_name", file_path.stem)
        schema_version = payload.get("schema_version", f"{contract_name}.v1")

        records.append(
            EvaluationDefinitionRecord(
                evaluation_id=str(contract_name),
                version=str(schema_version),
                source_definition_id=file_path.stem,
            )
        )

    return EvaluationRegistrySummary(
        total_evaluations=len(records),
        records=records,
    )
