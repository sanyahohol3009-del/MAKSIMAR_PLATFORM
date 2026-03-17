#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/UI_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > ui_system.yaml <<'YAML'
schema_version: ui_system_config.v1
description: Canonical top-level configuration for unified system UI.

ui_system:
  unified_style_required: true
  dashboard_router_enabled: true
  settings_center_enabled: true
  shared_components_required: true

safety:
  ui_permission_escalation_forbidden: true
  hidden_admin_surfaces_forbidden: true
  ui_action_binding_must_follow_policy: true

rules:
  - UI is presentation and interaction layer, not authority layer
  - UI must not bypass governance, approval, or action policy
  - all surfaces must remain auditable and explicit
YAML

cat > main_dashboard.yaml <<'YAML'
schema_version: ui_main_dashboard.v1
description: Canonical policy for main system dashboard.

dashboard:
  system_state_visible: true
  assistant_state_visible: true
  connected_nodes_visible: true
  active_modules_visible: true
  alerts_visible: true

requirements:
  widget_contract_required: true
  access_policy_filtering_required: true
  shell_compatibility_required: true

rules:
  - main dashboard must remain bounded by access policy
  - critical alerts must stay visible
  - dashboard does not imply execution authority
YAML

cat > module_dashboard_router.yaml <<'YAML'
schema_version: ui_module_dashboard_router.v1
description: Canonical routing policy for module dashboards.

router:
  module_dashboard_registration_required: true
  supported_shells_required: true
  settings_schema_required: true
  status_widget_binding_required: true

navigation:
  unified_navigation_required: true
  hidden_module_panels_forbidden: true
  access_filtered_listing_required: true

rules:
  - every visible module dashboard must be explicitly registered
  - router must respect module compatibility and access policy
  - dashboard routing must remain deterministic and auditable
YAML

cat > settings_center.yaml <<'YAML'
schema_version: ui_settings_center.v1
description: Canonical settings center policy for system and module configuration.

settings:
  owner_reference_required: true
  settings_schema_required: true
  sensitive_settings_policy_gated: true
  shell_specific_rendering_allowed: true

validation:
  explicit_field_definitions_required: true
  audit_required_for_sensitive_changes: true
  forbidden_hidden_settings: true

rules:
  - settings center must not expose hidden privileged controls
  - sensitive settings require policy-gated visibility and changes
  - settings changes must remain auditable
YAML

cat > theme_contracts.yaml <<'YAML'
schema_version: ui_theme_contracts.v1
description: Canonical theme and token policy for unified UI rendering.

theme:
  design_tokens_required: true
  module_ui_token_binding_required: true
  shell_theming_allowed: true
  branding_profile_binding_allowed: true

validation:
  token_reference_required: true
  unsupported_theme_fallback_required: true

rules:
  - theming must remain compatible with shared UI tokens
  - visual customization must not affect authority or access rules
  - theme selection must remain explicit and reviewable
YAML

echo "ui configs filled successfully"
