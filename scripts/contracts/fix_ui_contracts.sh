#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/ui"

cat > dashboard_manifest.v1.yaml <<'YAML'
contract_name: dashboard_manifest
schema_version: dashboard_manifest.v1
description: Canonical dashboard declaration for a module or platform layer.

required:
  - dashboard_id
  - owner_ref
  - dashboard_type
  - sections

fields:
  dashboard_id:
    type: string
    description: Unique dashboard identifier.

  owner_ref:
    type: string
    description: Reference to owning module, layer, or product surface.

  dashboard_type:
    type: string
    description: Canonical dashboard category or surface type.

  sections:
    type: array
    items:
      type: string
    description: Ordered list of dashboard sections.

  widgets:
    type: array
    items:
      type: string
    description: Widget identifiers rendered within this dashboard.

  supported_shells:
    type: array
    items:
      type: string
    description: Explicit list of shells allowed to render this dashboard.

validation_rules:
  - dashboard_id must be unique
  - sections must not be empty
  - supported_shells should be explicit even when limited
  - owner_ref must reference a known module, layer, or product surface

security_rules:
  - UI does not imply permission escalation
  - dashboard visibility must follow access policy
  - dashboard manifest must not embed hidden action authority
YAML

cat > settings_schema.v1.yaml <<'YAML'
contract_name: settings_schema
schema_version: settings_schema.v1
description: Canonical settings schema for dashboards, layers, and modules.

required:
  - settings_id
  - owner_ref
  - fields

fields:
  settings_id:
    type: string
    description: Unique settings schema identifier.

  owner_ref:
    type: string
    description: Reference to the owner of this settings surface.

  fields:
    type: array
    items:
      type: object
    description: Structured list of settings field definitions.

validation_rules:
  - owner_ref required
  - fields must not be empty
  - settings field definitions should be explicit and typed

security_rules:
  - sensitive settings require policy-gated exposure
  - settings schema does not imply mutation rights by itself
  - hidden privileged settings are forbidden
YAML

cat > widget_schema.v1.yaml <<'YAML'
contract_name: widget_schema
schema_version: widget_schema.v1
description: Canonical widget contract for dashboard composition.

required:
  - widget_id
  - widget_type
  - data_binding

fields:
  widget_id:
    type: string
    description: Unique widget identifier.

  widget_type:
    type: string
    description: Canonical widget category.

  data_binding:
    type: string
    description: Bound data source, metric source, or contract reference.

  display_policy:
    type: object
    additional_properties: true
    description: Structured widget display rules, visibility, and layout hints.

validation_rules:
  - widget_id must be unique
  - data_binding required
  - widget_type required
  - display_policy should remain structured when present

security_rules:
  - widget visibility follows access policy
  - widgets do not grant execution rights
  - widget bindings must not expose restricted data outside policy
YAML

cat > notification_schema.v1.yaml <<'YAML'
contract_name: notification_schema
schema_version: notification_schema.v1
description: Canonical notification payload for system and module surfaces.

required:
  - notification_id
  - severity
  - message

fields:
  notification_id:
    type: string
    description: Unique notification identifier.

  severity:
    type: string
    enum:
      - info
      - warning
      - critical
    description: Notification severity level.

  message:
    type: string
    description: Human-readable notification message.

  source_ref:
    type: string
    description: Source component, module, or subsystem producing the notification.

  action_refs:
    type: array
    items:
      type: string
    description: Optional references to allowed follow-up actions.

validation_rules:
  - notification_id must be unique
  - message required
  - severity must match allowed enum
  - action_refs should reference approved actions only when present

security_rules:
  - notifications cannot trigger execution without policy
  - critical notifications must remain visible to authorized surfaces
  - notifications must not embed hidden command payloads
YAML

cat > shell_surface_schema.v1.yaml <<'YAML'
contract_name: shell_surface_schema
schema_version: shell_surface_schema.v1
description: Canonical UI surface contract per shell.

required:
  - surface_id
  - shell_type
  - supported_dashboards

fields:
  surface_id:
    type: string
    description: Unique shell surface identifier.

  shell_type:
    type: string
    description: Shell type associated with this UI surface.

  supported_dashboards:
    type: array
    items:
      type: string
    description: Dashboard identifiers supported by this shell surface.

  capabilities:
    type: array
    items:
      type: string
    description: UI capabilities supported on this shell surface.

validation_rules:
  - surface_id must be unique
  - shell_type required
  - supported_dashboards must be explicit
  - capabilities should remain bounded to shell contract

security_rules:
  - shell surface follows shell permissions
  - shell surface does not grant action authority by itself
  - restricted dashboards must remain filtered by access policy
YAML

echo "ui contracts restored successfully"
