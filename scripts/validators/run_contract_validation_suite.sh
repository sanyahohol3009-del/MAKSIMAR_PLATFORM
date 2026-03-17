#!/usr/bin/env bash
set -euo pipefail

ROOT="${HOME}/MAKSIMAR_PLATFORM"
cd "${ROOT}"

echo "== Running Contract Validation Suite =="

bash scripts/validators/validate_contract_domains.sh
echo

bash scripts/validators/validate_no_empty_contracts.sh
echo

bash scripts/validators/validate_contracts.sh
echo

echo "Contract validation suite finished successfully."
