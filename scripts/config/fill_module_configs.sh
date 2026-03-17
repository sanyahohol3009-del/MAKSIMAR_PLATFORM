#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/MODULE_SYSTEM/config"
mkdir -p "$BASE"
cd "$BASE"

cat > module_registry.yaml <<'YAML'
schema_version: module_registry_config.v1
description: Canonical registry configuration for platform modules and cubes.

registry:
  manifest_registry_enabled: true
  permission_registry_enabled: true
  compatibility_registry_enabled: true
  dashboard_registry_enabled: true
  workflow_binding_registry_enabled: true

defaults:
  modules_disabled_by_default: true
  manual_registration_required: true
  registry_audit_enabled: true

rules:
  - every module must be manifest-declared
  - hidden modules are forbidden
  - registry mutations must remain auditable
YAML

cat > lifecycle_policy.yaml <<'YAML'
schema_version: module_lifecycle_policy.v1
description: Canonical lifecycle policy for installation, enablement, disablement, and removal of modules.

states:
  - registered
  - installed
  - enabled
  - disabled
  - removed

transitions:
  registered:
    allowed_to:
      - installed
      - removed

  installed:
    allowed_to:
      - enabled
      - disabled
      - removed

  enabled:
    allowed_to:
      - disabled
      - removed

  disabled:
    allowed_to:
      - enabled
      - removed

  removed:
    allowed_to: []

requirements:
  permission_check_required: true
  compatibility_check_required: true
  dashboard_manifest_check_required: true

rules:
  - lifecycle transitions must be explicit
  - incompatible modules must not be enabled
  - removal must not leave orphaned privileged bindings
YAML

cat > compatibility_policy.yaml <<'YAML'
schema_version: module_compatibility_policy.v1
description: Canonical compatibility policy across shells, products, and deployment modes.

checks:
  shell_compatibility_required: true
  product_compatibility_required: true
  capability_profile_compatibility_required: true
  backend_requirement_check_required: true

defaults:
  incompatible_modules_block_activation: true
  standalone_incompatible_modules_block_packaging: true

rules:
  - module compatibility must be explicit
  - backend-required modules must not be activated in unsupported standalone contexts
  - compatibility does not imply automatic enablement
YAML

cat > dashboard_policy.yaml <<'YAML'
schema_version: module_dashboard_policy.v1
description: Canonical dashboard policy for modules and cube UI surfaces.

dashboard_rules:
  module_dashboard_required: true
  settings_schema_required: true
  status_widgets_required: true
  supported_shells_required: true

ui_rules:
  unified_style_required: true
  dashboard_router_integration_required: true
  hidden_admin_panels_forbidden: true

rules:
  - every user-facing module must declare dashboard surface
  - dashboard visibility must follow access policy
  - module dashboards must remain within unified UI contract
YAML

cat > module_templates.yaml <<'YAML'
schema_version: module_templates_policy.v1
description: Canonical template policy for scaffolded module families and cube generation.

templates:
  family_assistant:
    enabled: true

  engineering_assistant:
    enabled: true

  knowledge_assistant:
    enabled: true

  automation_cube:
    enabled: true

  vpn_cube:
    enabled: true

  energy_cube:
    enabled: true

  compute_fleet_cube:
    enabled: true

  visual_engineering_cube:
    enabled: true

  robotics_cube:
    enabled: true

rules:
  - templates are scaffolding aids, not active modules
  - generated modules must still pass manifest and compatibility checks
  - template use must not bypass governance or module lifecycle policy
YAML

echo "module configs filled successfully"
