#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/mobile"

cat > mobile_capability.v1.yaml <<'YAML'
contract_name: mobile_capability
schema_version: mobile_capability.v1
description: Mobile capability declaration for Android and iOS products.

required:
  - capability_id
  - platform
  - supported_actions

fields:
  capability_id:
    type: string
    description: Unique mobile capability identifier.

  platform:
    type: string
    enum:
      - android
      - ios
    description: Mobile platform for which this capability is defined.

  supported_actions:
    type: array
    items:
      type: string
    description: Explicit list of portable actions supported on this mobile platform.

  local_only:
    type: boolean
    description: Whether the capability is restricted to fully local execution.

validation_rules:
  - capability_id required
  - platform must match allowed enum
  - supported_actions required
  - supported_actions must not be empty
  - local_only should be explicit

security_rules:
  - mobile capability set must respect shell boundary
  - declared capability does not grant authority by itself
  - local_only capabilities must not be silently rerouted to privileged backends
YAML

cat > app_action.v1.yaml <<'YAML'
contract_name: app_action
schema_version: app_action.v1
description: Android-oriented App Actions bridge contract.

required:
  - action_id
  - intent_name
  - target_handler

fields:
  action_id:
    type: string
    description: Unique Android app action identifier.

  intent_name:
    type: string
    description: Android intent or App Action name exposed by the shell bridge.

  target_handler:
    type: string
    description: Portable-core or shell handler bound to this action.

  parameter_schema:
    type: object
    additional_properties: true
    description: Structured parameter schema for the action bridge.

validation_rules:
  - action_id required
  - intent_name required
  - target_handler required
  - parameter_schema should be explicit when parameters are supported

security_rules:
  - app actions remain within approved mobile action library
  - action bridge does not bypass workflow, approval, or shell policy
  - Android integration must stay bounded by portable-core governance
YAML

cat > app_intent.v1.yaml <<'YAML'
contract_name: app_intent
schema_version: app_intent.v1
description: iOS-oriented App Intents bridge contract.

required:
  - intent_id
  - intent_name
  - target_handler

fields:
  intent_id:
    type: string
    description: Unique iOS App Intent identifier.

  intent_name:
    type: string
    description: App Intent name exposed by the iOS shell bridge.

  target_handler:
    type: string
    description: Portable-core or shell handler bound to this intent.

  parameter_schema:
    type: object
    additional_properties: true
    description: Structured parameter schema for the iOS intent bridge.

validation_rules:
  - intent_id required
  - intent_name required
  - target_handler required
  - parameter_schema should be explicit when parameters are supported

security_rules:
  - app intents remain within approved mobile action library
  - intent bridge does not bypass workflow, approval, or shell policy
  - iOS integration must stay bounded by portable-core governance
YAML

cat > mobile_permission_bridge.v1.yaml <<'YAML'
contract_name: mobile_permission_bridge
schema_version: mobile_permission_bridge.v1
description: Bridge between portable-core permissions and mobile OS permissions.

required:
  - bridge_id
  - platform
  - core_permission
  - os_permission

fields:
  bridge_id:
    type: string
    description: Unique permission bridge identifier.

  platform:
    type: string
    enum:
      - android
      - ios
    description: Mobile platform governed by this permission bridge.

  core_permission:
    type: string
    description: Portable-core permission identifier.

  os_permission:
    type: string
    description: Operating-system permission identifier.

  granted:
    type: boolean
    description: Current bridge state between OS permission and core permission usability.

validation_rules:
  - bridge_id required
  - platform must match allowed enum
  - core_permission required
  - os_permission required
  - granted should be explicit

security_rules:
  - OS permission is not equal to core authority automatically
  - bridge records do not bypass governance or approval policy
  - permission mapping must remain explicit and auditable
YAML

echo "mobile contracts restored successfully"
