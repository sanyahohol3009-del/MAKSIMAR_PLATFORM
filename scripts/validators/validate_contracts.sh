#!/usr/bin/env bash
set -euo pipefail

ROOT="${HOME}/MAKSIMAR_PLATFORM"
CONTRACTS_DIR="${ROOT}/MAKSIMAR_CORE/contracts"

if [[ ! -d "${CONTRACTS_DIR}" ]]; then
  echo "ERROR: contracts directory not found: ${CONTRACTS_DIR}"
  exit 1
fi

required_top_keys=(
  "contract_name:"
  "schema_version:"
  "description:"
  "required:"
  "fields:"
  "validation_rules:"
  "security_rules:"
)

echo "== Contract Validator =="
echo "ROOT: ${ROOT}"
echo "CONTRACTS_DIR: ${CONTRACTS_DIR}"
echo

yaml_files=$(find "${CONTRACTS_DIR}" -type f -name "*.yaml" | sort)

if [[ -z "${yaml_files}" ]]; then
  echo "ERROR: no YAML contract files found"
  exit 1
fi

total=0
failed=0

while IFS= read -r file; do
  total=$((total + 1))
  rel_path="${file#${ROOT}/}"
  echo "-- Checking: ${rel_path}"

  if [[ ! -s "${file}" ]]; then
    echo "   ERROR: file is empty"
    failed=$((failed + 1))
    continue
  fi

  for key in "${required_top_keys[@]}"; do
    if ! grep -q "^${key}" "${file}"; then
      echo "   ERROR: missing top-level key: ${key}"
      failed=$((failed + 1))
      continue 2
    fi
  done

  contract_name="$(grep '^contract_name:' "${file}" | head -n1 | sed 's/^contract_name:[[:space:]]*//')"
  schema_version="$(grep '^schema_version:' "${file}" | head -n1 | sed 's/^schema_version:[[:space:]]*//')"
  base_name="$(basename "${file}" .yaml)"
  expected_schema="${base_name}"

  if [[ "${schema_version}" != "${expected_schema}" ]]; then
    echo "   ERROR: schema_version mismatch"
    echo "          expected: ${expected_schema}"
    echo "          actual:   ${schema_version}"
    failed=$((failed + 1))
    continue
  fi

  if [[ -z "${contract_name}" ]]; then
    echo "   ERROR: empty contract_name"
    failed=$((failed + 1))
    continue
  fi

  if [[ "${base_name}" != *.v1 ]]; then
    echo "   ERROR: file name must end with .v1.yaml"
    failed=$((failed + 1))
    continue
  fi

  echo "   OK"
done <<< "${yaml_files}"

echo
echo "== Summary =="
echo "Total checked: ${total}"
echo "Failures: ${failed}"

if [[ "${failed}" -ne 0 ]]; then
  exit 1
fi

echo "All contracts passed."
