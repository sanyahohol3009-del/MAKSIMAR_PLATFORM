#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/codegen"
cd "$BASE"

sed -i 's/^schema_version: v1$/schema_version: codegen_diff.v1/' codegen_diff.v1.yaml
sed -i 's/^schema_version: v1$/schema_version: lint_report.v1/' lint_report.v1.yaml
sed -i 's/^schema_version: v1$/schema_version: proposal_package.v1/' proposal_package.v1.yaml
sed -i 's/^schema_version: v1$/schema_version: spec_to_module.v1/' spec_to_module.v1.yaml
sed -i 's/^schema_version: v1$/schema_version: task_to_spec.v1/' task_to_spec.v1.yaml
sed -i 's/^schema_version: v1$/schema_version: test_report.v1/' test_report.v1.yaml
sed -i 's/^schema_version: v1$/schema_version: typecheck_report.v1/' typecheck_report.v1.yaml

echo "codegen schema_version values fixed successfully"
