#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/shell"

cat > shell_contract.v1.yaml <<'YAML'
contract_name: shell_contract
schema_version: shell_contract.v1
description: Generic shell boundary contract.

required:
  - shell_id
  - shell_type
  - supported_capabilities

fields:
  shell_id:
    type: string
    description: Unique shell identifier.

  shell_type:
    type: string
    enum:
      - server
      - desktop
      - android
      - ios
    description: Canonical shell type.

  supported_capabilities:
    type: array
    items:
      type: string
    description: Explicit list of capabilities exposed by this shell.

  shell_policy_ref:
    type: string
    description: Reference to governing shell policy.

validation_rules:
  - shell_id required
  - shell_type must match allowed enum
  - supported_capabilities required
  - supported_capabilities must not be empty

security_rules:
  - shell must not exceed portable core governance
  - shell declaration does not grant authority by itself
  - shell boundaries must remain explicit and auditable
YAML

cat > shell_surface.v1.yaml <<'YAML'
contract_name: shell_surface
schema_version: shell_surface.v1
description: User-visible surfaces exposed by a shell.

required:
  - surface_id
  - shell_ref
  - surfaces

fields:
  surface_id:
    type: string
    description: Unique shell surface identifier.

  shell_ref:
    type: string
    description: Reference to owning shell contract.

  surfaces:
    type: array
    items:
      type: string
    description: Explicit list of user-visible surfaces exposed by the shell.

validation_rules:
  - surface_id required
  - shell_ref required
  - surfaces required
  - surfaces must not be empty

security_rules:
  - surfaces obey access policies
  - visible surfaces do not imply hidden capabilities
  - shell UI exposure must remain bounded by governance
YAML

cat > shell_action_bridge.v1.yaml <<'YAML'
contract_name: shell_action_bridge
schema_version: shell_action_bridge.v1
description: Mapping between portable action primitives and shell implementations.

required:
  - bridge_id
  - action_type
  - shell_type
  - handler_ref

fields:
  bridge_id:
    type: string
    description: Unique shell action bridge identifier.

  action_type:
    type: string
    description: Portable action primitive being bridged.

  shell_type:
    type: string
    enum:
      - server
      - desktop
      - android
      - ios
    description: Shell type implementing the action.

  handler_ref:
    type: string
    description: Reference to shell-side handler implementation.

  supported_parameters:
    type: array
    items:
      type: string
    description: Explicit parameter set supported by this shell handler.

validation_rules:
  - bridge_id required
  - action_type required
  - shell_type must match allowed enum
  - handler_ref required
  - supported_parameters should be explicit even when empty

security_rules:
  - bridge does not bypass action permission policy
  - shell implementation remains bounded by governance and approval
  - handler bindings must not embed hidden privileged paths
YAML

echo "shell contracts restored successfully"
