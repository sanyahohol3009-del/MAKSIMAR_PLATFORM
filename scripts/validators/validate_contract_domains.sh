#!/usr/bin/env bash
set -euo pipefail

ROOT="${HOME}/MAKSIMAR_PLATFORM"
BASE="${ROOT}/MAKSIMAR_CORE/contracts"

expected_domains=(
  runtime
  governance
  memory
  knowledge
  research
  workflow
  action
  module
  ui
  federation
  product
  packaging
  codegen
  evaluation
  simulation
  robotics
  cad_3d_cam
  visual_engineering
  energy
  compute_fleet
  vpn
  industrial
  content_media
  dialogue
  voice
  mobile
  shell
)

echo "== Contract Domains Validator =="
missing=0

for domain in "${expected_domains[@]}"; do
  path="${BASE}/${domain}"
  if [[ -d "${path}" ]]; then
    echo "OK  ${domain}"
  else
    echo "ERR ${domain} missing"
    missing=$((missing + 1))
  fi
done

echo
echo "Missing domains: ${missing}"

if [[ "${missing}" -ne 0 ]]; then
  exit 1
fi

echo "All contract domains exist."
