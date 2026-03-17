#!/usr/bin/env bash

set -e

ROOT="$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts"

find "$ROOT" -type f -name "*.yaml" | while read file
do
  if [ ! -s "$file" ]; then

    name=$(basename "$file" .yaml)

cat <<EOF > "$file"
contract_name: ${name%%.v1}
schema_version: ${name##*.}
description: Canonical contract for ${name%%.v1}.

required:
  - id

fields:
  id:
    type: string

metadata:
  created_by: MAKSIMAR_PLATFORM
  layer: portable_core
  status: draft

validation_rules:
  - id required

security_rules:
  - no implicit authority
  - execution requires approval policy
EOF

  fi
done

echo "Contract schema skeletons filled."
