#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/ACTION_LIBRARY/config"
mkdir -p "$BASE"
cd "$BASE"

cat > action_library.yaml <<'YAML'
schema_version: action_library_config.v1
description: Canonical configuration for the portable action library.

registry:
  manifest_registry_enabled: true
  handler_registry_enabled: true
  permission_registry_enabled: true

execution_policy:
  shell_execution_forbidden: true
  direct_core_write_forbidden: true
  hidden_actions_forbidden: true
  approval_bridge_required: true

resolution:
  strict_manifest_lookup: true
  handler_binding_required: true
  explicit_parameter_schema_required: true

rules:
  - every action must have manifest
  - every action must resolve to handler
  - action library must remain explicit and auditable
  - no action may bypass governance approval
YAML

cat > action_risk_mapping.yaml <<'YAML'
schema_version: action_risk_mapping.v1
description: Mapping between action categories and governance risk levels.

categories:
  informational:
    risk_level: safe

  device_control:
    risk_level: sensitive

  system_operation:
    risk_level: sensitive

  hardware_operation:
    risk_level: dangerous

  industrial_operation:
    risk_level: dangerous

  forbidden_operation:
    risk_level: blocked

rules:
  - action category must map to governance risk level
  - blocked actions must never resolve
YAML

cat > action_contexts.yaml <<'YAML'
schema_version: action_contexts.v1
description: Allowed execution contexts for portable actions.

contexts:
  desktop:
    allowed: true

  android:
    allowed: true

  ios:
    allowed: true

  server:
    allowed: true

  family_mode:
    restricted_actions: true

  engineering_mode:
    extended_actions: true

rules:
  - context restrictions must remain explicit
  - actions must declare supported contexts
YAML

cat > action_permissions.yaml <<'YAML'
schema_version: action_permissions.v1
description: Permission mapping for action execution.

permission_levels:
  public:
    description: available without special permissions

  user:
    description: requires authenticated user context

  privileged:
    description: requires elevated permission and approval

  restricted:
    description: requires explicit policy approval

rules:
  - permission level must be declared in action manifest
  - privileged and restricted actions require approval policy
YAML

cat > action_validation.yaml <<'YAML'
schema_version: action_validation_policy.v1
description: Validation rules for action manifests and handlers.

manifest_rules:
  require_action_id: true
  require_parameter_schema: true
  require_handler_reference: true
  require_permission_level: true

handler_rules:
  handler_must_exist: true
  handler_must_declare_supported_contexts: true
  handler_must_not_execute_unbounded_shell: true

rules:
  - invalid manifest must block action registration
  - handler validation must occur before activation
YAML

echo "action configs filled successfully"
