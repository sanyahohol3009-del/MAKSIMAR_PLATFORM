#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/SHELL_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > shell_registry.yaml <<'YAML'
schema_version: shell_registry.v1
description: Canonical registry of supported runtime shells.

shells:
  server:
    enabled: true

  desktop:
    enabled: true

  android:
    enabled: true

  ios:
    enabled: true

  cli:
    enabled: true

rules:
  - shells must be explicitly registered
  - disabled shells must not silently activate
  - shell registry defines supported runtime environments
YAML


cat > shell_capabilities.yaml <<'YAML'
schema_version: shell_capabilities.v1
description: Canonical mapping of shell capabilities.

capabilities:

  server:
    network_services: true
    long_running_tasks: true
    local_storage: true

  desktop:
    local_ui: true
    local_storage: true
    system_integration: true

  android:
    mobile_ui: true
    sensors: true
    push_notifications: true

  ios:
    mobile_ui: true
    sensors: true
    push_notifications: true

  cli:
    terminal_io: true
    automation_scripts: true

rules:
  - capability definitions must remain explicit
  - shells must not claim unsupported capabilities
  - capability mapping must remain auditable
YAML


cat > shell_security.yaml <<'YAML'
schema_version: shell_security_policy.v1
description: Canonical security policy for runtime shells.

security:
  permission_model_required: true
  sandbox_required_when_supported: true
  audit_logging_required: true

restrictions:
  hidden_privileged_shells_forbidden: true
  unauthorized_capability_escalation_forbidden: true
  policy_bypass_forbidden: true

rules:
  - shell execution must remain bounded by platform governance
  - shell privileges must remain explicit
  - shell security must remain auditable
YAML


cat > shell_ui_binding.yaml <<'YAML'
schema_version: shell_ui_binding.v1
description: Canonical binding policy between shells and UI layer.

bindings:
  ui_contract_required: true
  dashboard_router_binding_required: true
  settings_center_binding_required: true

compatibility:
  mobile_shells_require_mobile_ui: true
  desktop_shells_require_desktop_ui: true

rules:
  - shell must bind only compatible UI surfaces
  - UI binding must remain explicit
  - incompatible UI surfaces must not load
YAML


echo "shell configs filled successfully"
