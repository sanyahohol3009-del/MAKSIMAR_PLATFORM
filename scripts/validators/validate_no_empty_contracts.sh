#!/usr/bin/env bash
set -euo pipefail

ROOT="${HOME}/MAKSIMAR_PLATFORM"
BASE="${ROOT}/MAKSIMAR_CORE/contracts"

echo "== Empty Contract Files Validator =="

empty_count=$(find "${BASE}" -type f -name "*.yaml" -empty | wc -l)

if [[ "${empty_count}" -ne 0 ]]; then
  echo "ERROR: found empty YAML contract files"
  find "${BASE}" -type f -name "*.yaml" -empty | sort
  exit 1
fi

echo "No empty YAML contract files found."
