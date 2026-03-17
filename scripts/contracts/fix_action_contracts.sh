#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/action"

cat > action_manifest.v1.yaml <<'YAML'
contract_name: action_manifest
schema_version: action_manifest.v1
description: Canonical declaration of approved action primitive.

required:
  - action_type
  - supported_contexts
  - risk_level

fields:
  action_type:
    type: string
    description: Unique action primitive identifier.

  supported_contexts:
    type: array
    items:
      type: string
    description: Explicit list of contexts in which the action may be used.

  required_parameters:
    type: array
    items:
      type: string
    description: Explicit list of required parameters for valid action execution.

  risk_level:
    type: string
    enum:
      - safe
      - sensitive
      - dangerous
      - blocked
    description: Governance risk level assigned to the action.

  approval_policy:
    type: string
    description: Reference or name of approval policy required for this action.

  is_repeatable:
    type: boolean
    description: Whether the action may be safely executed multiple times.

  is_reversible:
    type: boolean
    description: Whether the action has a supported reversal path.

validation_rules:
  - action_type must be unique
  - risk_level must match allowed enum
  - supported_contexts must not be empty
  - required_parameters should be explicit even when empty

security_rules:
  - blocked actions are non-executable
  - action manifests do not grant execution rights by themselves
  - action definitions must not contain hidden shell authority
YAML

cat > action_permission.v1.yaml <<'YAML'
contract_name: action_permission
schema_version: action_permission.v1
description: Permission binding for action execution.

required:
  - action_type
  - requester_role
  - allowed

fields:
  action_type:
    type: string
    description: Action primitive governed by this permission rule.

  requester_role:
    type: string
    description: Role or actor category requesting the action.

  allowed:
    type: boolean
    description: Whether the action is permitted for the requester role.

  conditions:
    type: object
    additional_properties: true
    description: Optional structured constraints required for permission to apply.

validation_rules:
  - requester_role required
  - action_type required
  - allowed must be explicit boolean

security_rules:
  - deny by default
  - permission binding cannot exceed global permission matrix
  - conditions must not silently weaken blocked classifications
YAML

cat > action_context.v1.yaml <<'YAML'
contract_name: action_context
schema_version: action_context.v1
description: Runtime execution context for actions.

required:
  - context_id
  - shell_type
  - device_id

fields:
  context_id:
    type: string
    description: Unique action execution context identifier.

  shell_type:
    type: string
    description: Shell type hosting the execution path.

  device_id:
    type: string
    description: Device or node identifier bound to this execution context.

  mode:
    type: string
    description: Active operating mode, such as engineering, family, or mobile mode.

  capability_profile_ref:
    type: string
    description: Reference to capability profile active in this context.

validation_rules:
  - shell_type and device_id required
  - context_id must be unique
  - shell_type should map to a known shell contract

security_rules:
  - context does not bypass policy
  - capability profile does not override forbidden actions
  - action context is descriptive, not authoritative
YAML

cat > action_execution.v1.yaml <<'YAML'
contract_name: action_execution
schema_version: action_execution.v1
description: Canonical record for action execution.

required:
  - execution_id
  - action_type
  - status

fields:
  execution_id:
    type: string
    description: Unique action execution identifier.

  action_type:
    type: string
    description: Action primitive that was requested or executed.

  status:
    type: string
    enum:
      - success
      - failed
      - blocked
      - cancelled
    description: Final or terminal action execution state.

  parameters:
    type: object
    additional_properties: true
    description: Structured parameters supplied for the action.

  context_ref:
    type: string
    description: Reference to the action context used for execution.

  approval_ref:
    type: string
    description: Reference to approval artifact or approval path when required.

validation_rules:
  - action_type required
  - status must match allowed enum
  - blocked status should carry linked approval or policy reason through execution metadata
  - context_ref should be present for non-simulated executions

security_rules:
  - blocked status must preserve reason
  - execution record does not imply future permission reuse
  - action execution artifacts must respect secrets and privacy policy
YAML

echo "action contracts restored successfully"
