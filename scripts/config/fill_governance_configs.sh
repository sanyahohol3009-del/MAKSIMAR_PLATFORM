#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/governance/config"
mkdir -p "$BASE"
cd "$BASE"

cat > risk_matrix.yaml <<'YAML'
schema_version: governance_risk_matrix.v1
description: Canonical risk classification matrix for actions, workflows, proposals, and domain operations.

levels:
  safe:
    description: Low-risk operations that do not affect privileged state or safety boundaries.
    approval_required: false
    voice_confirmation_required: false
    hardware_key_required: false
    execution_forbidden: false

  sensitive:
    description: Operations affecting user state, device state, network behavior, or business-significant flows.
    approval_required: true
    voice_confirmation_required: true
    hardware_key_required: false
    execution_forbidden: false

  dangerous:
    description: Operations affecting critical services, hardware actions, industrial flows, or destructive state transitions.
    approval_required: true
    voice_confirmation_required: true
    hardware_key_required: true
    execution_forbidden: false

  blocked:
    description: Explicitly forbidden operations that must never be executed by platform orchestration.
    approval_required: false
    voice_confirmation_required: false
    hardware_key_required: false
    execution_forbidden: true

rules:
  - blocked overrides all lower-level decisions
  - action-level block cannot be weakened by workflow-level safe classification
  - dangerous operations must remain human-gated
  - no domain may redefine blocked as executable
YAML

cat > approval_policy.yaml <<'YAML'
schema_version: governance_approval_policy.v1
description: Canonical approval requirements for actions, workflows, proposals, and deployment paths.

policies:
  safe_default:
    applies_to:
      - action
      - workflow
    risk_level: safe
    approval_required: false
    approval_type: none
    voice_confirmation_required: false
    hardware_key_required: false
    delay_buffer_sec: 0

  sensitive_default:
    applies_to:
      - action
      - workflow
      - product_change
      - packaging_change
    risk_level: sensitive
    approval_required: true
    approval_type: confirm_once
    voice_confirmation_required: true
    hardware_key_required: false
    delay_buffer_sec: 5

  dangerous_default:
    applies_to:
      - action
      - workflow
      - hardware_bridge
      - industrial_control
      - deployment
    risk_level: dangerous
    approval_required: true
    approval_type: hardware_key
    voice_confirmation_required: true
    hardware_key_required: true
    delay_buffer_sec: 15

  blocked_default:
    applies_to:
      - forbidden_action
      - forbidden_workflow
      - forbidden_deploy
    risk_level: blocked
    approval_required: false
    approval_type: none
    voice_confirmation_required: false
    hardware_key_required: false
    delay_buffer_sec: 0
    execution_forbidden: true

rules:
  - blocked policies must not authorize execution
  - stricter approval requirements must not be weakened downstream
  - deployment into privileged or hardware-adjacent layers must remain gated
  - approval evidence must be auditable
YAML

cat > permission_matrix.yaml <<'YAML'
schema_version: governance_permission_matrix.v1
description: Canonical deny-by-default permission matrix for core roles, domains, and execution scopes.

roles:
  - operator
  - owner
  - platform_service
  - shell_adapter
  - module_runtime
  - ai_service
  - monitoring
  - sandbox_runtime

resources:
  - contracts
  - configs
  - workflows
  - actions
  - memory
  - knowledge
  - research
  - products
  - packaging
  - simulation
  - robotics
  - visual_engineering
  - energy
  - compute_fleet
  - vpn
  - industrial
  - voice
  - dialogue
  - shell
  - core_root
  - safety_foundation

permissions:
  operator:
    contracts: read
    configs: read
    workflows: read_write
    actions: read
    memory: read_write
    knowledge: read_write
    research: read_write
    products: read_write
    packaging: read_write
    simulation: read_write
    robotics: read_write
    visual_engineering: read_write
    energy: read_write
    compute_fleet: read_write
    vpn: read_write
    industrial: read_write
    voice: read_write
    dialogue: read_write
    shell: read_write
    core_root: none
    safety_foundation: read

  owner:
    contracts: read_write
    configs: read_write
    workflows: read_write
    actions: read_write
    memory: read_write
    knowledge: read_write
    research: read_write
    products: read_write
    packaging: read_write
    simulation: read_write
    robotics: read_write
    visual_engineering: read_write
    energy: read_write
    compute_fleet: read_write
    vpn: read_write
    industrial: read_write
    voice: read_write
    dialogue: read_write
    shell: read_write
    core_root: none
    safety_foundation: read

  platform_service:
    contracts: read
    configs: read
    workflows: read_write
    actions: read
    memory: read_write
    knowledge: read_write
    research: read_write
    products: read
    packaging: read
    simulation: read_write
    robotics: read
    visual_engineering: read_write
    energy: read_write
    compute_fleet: read_write
    vpn: read_write
    industrial: read
    voice: read_write
    dialogue: read_write
    shell: read
    core_root: none
    safety_foundation: none

  shell_adapter:
    contracts: read
    configs: read
    workflows: read
    actions: read
    memory: read_write
    knowledge: read
    research: read
    products: read
    packaging: read
    simulation: none
    robotics: none
    visual_engineering: read
    energy: read
    compute_fleet: read
    vpn: read_write
    industrial: none
    voice: read_write
    dialogue: read_write
    shell: read_write
    core_root: none
    safety_foundation: none

  module_runtime:
    contracts: read
    configs: read
    workflows: read_write
    actions: read
    memory: read_write
    knowledge: read
    research: read
    products: read
    packaging: read
    simulation: read
    robotics: read
    visual_engineering: read
    energy: read
    compute_fleet: read
    vpn: read
    industrial: read
    voice: none
    dialogue: none
    shell: none
    core_root: none
    safety_foundation: none

  ai_service:
    contracts: read
    configs: read
    workflows: read
    actions: read
    memory: read_write
    knowledge: read_write
    research: read_write
    products: read
    packaging: read
    simulation: read
    robotics: read
    visual_engineering: read
    energy: read
    compute_fleet: read
    vpn: read
    industrial: read
    voice: read
    dialogue: read_write
    shell: none
    core_root: none
    safety_foundation: none

  monitoring:
    contracts: read
    configs: read
    workflows: read
    actions: read
    memory: read
    knowledge: read
    research: read
    products: read
    packaging: read
    simulation: read
    robotics: read
    visual_engineering: read
    energy: read
    compute_fleet: read
    vpn: read
    industrial: read
    voice: read
    dialogue: read
    shell: read
    core_root: none
    safety_foundation: read

  sandbox_runtime:
    contracts: read
    configs: read
    workflows: read
    actions: read
    memory: read_write
    knowledge: read
    research: read
    products: none
    packaging: none
    simulation: read_write
    robotics: read
    visual_engineering: read_write
    energy: read
    compute_fleet: read
    vpn: none
    industrial: none
    voice: none
    dialogue: none
    shell: none
    core_root: none
    safety_foundation: none

rules:
  - deny by default
  - no wildcard write permissions
  - core_root write is forbidden across all standard roles
  - safety_foundation mutation requires separate immutable path outside this matrix
YAML

cat > capability_profiles.yaml <<'YAML'
schema_version: governance_capability_profiles.v1
description: Canonical capability profile definitions for portable-core deployments and products.

profiles:
  core_profile_full_platform:
    enabled_capabilities:
      - memory_full
      - knowledge_full
      - research
      - workflow
      - actions
      - packaging
      - federation
      - codegen
      - evaluation
      - simulation
      - robotics
      - visual_engineering
      - energy
      - compute_fleet
      - vpn
      - industrial
      - dialogue
      - voice
    disabled_capabilities: []
    target_products:
      - jarvis_full_platform

  core_profile_mobile_consumer:
    enabled_capabilities:
      - memory_light
      - knowledge_basic
      - workflow
      - actions_mobile
      - vpn
      - dialogue
      - voice
    disabled_capabilities:
      - codegen
      - simulation
      - robotics
      - industrial
      - compute_fleet
    target_products:
      - jarvis_mobile_consumer

  core_profile_desktop_consumer:
    enabled_capabilities:
      - memory_light
      - knowledge_basic
      - workflow
      - actions_desktop
      - vpn
      - dialogue
      - voice
    disabled_capabilities:
      - codegen
      - robotics
      - industrial
    target_products:
      - jarvis_desktop_consumer

  core_profile_engineering:
    enabled_capabilities:
      - memory_full
      - knowledge_full
      - research
      - workflow
      - actions
      - codegen
      - evaluation
      - simulation
      - visual_engineering
      - dialogue
      - voice
    disabled_capabilities:
      - industrial_hardware_control
    target_products:
      - jarvis_engineering

rules:
  - enabled and disabled capability sets must not overlap
  - capability profiles cannot override blocked governance rules
  - productization must happen by profile selection, not by core fork
YAML

cat > deployment_modes.yaml <<'YAML'
schema_version: governance_deployment_modes.v1
description: Canonical deployment mode definitions for platform and product assembly.

modes:
  full_platform:
    shell_targets:
      - server
      - desktop
      - android
      - ios
    capability_profile_ref: core_profile_full_platform
    standalone: false
    backend_required: true

  personal_mobile_node:
    shell_targets:
      - android
      - ios
    capability_profile_ref: core_profile_mobile_consumer
    standalone: true
    backend_required: false

  standalone_desktop:
    shell_targets:
      - desktop
    capability_profile_ref: core_profile_desktop_consumer
    standalone: true
    backend_required: false

  engineering_station:
    shell_targets:
      - desktop
      - server
    capability_profile_ref: core_profile_engineering
    standalone: false
    backend_required: true

rules:
  - shell targets must be explicit
  - deployment mode cannot grant forbidden rights
  - backend-required modes must not degrade silently into standalone privileged behavior
YAML

cat > node_roles.yaml <<'YAML'
schema_version: governance_node_roles.v1
description: Canonical role definitions for JARVIS federation nodes.

roles:
  primary_personal_core:
    execution_scope: platform_root
    may_host_voice_layer: true
    may_host_full_memory: true
    may_host_codegen: true
    may_host_simulation: true

  desktop_companion:
    execution_scope: desktop_assist
    may_host_voice_layer: true
    may_host_full_memory: false
    may_host_codegen: true
    may_host_simulation: false

  android_personal_node:
    execution_scope: mobile_assist
    may_host_voice_layer: true
    may_host_full_memory: false
    may_host_codegen: false
    may_host_simulation: false

  ios_personal_node:
    execution_scope: mobile_assist
    may_host_voice_layer: true
    may_host_full_memory: false
    may_host_codegen: false
    may_host_simulation: false

  client_standalone_mobile:
    execution_scope: detached_mobile_product
    may_host_voice_layer: true
    may_host_full_memory: false
    may_host_codegen: false
    may_host_simulation: false

  server_control_node:
    execution_scope: backend_services
    may_host_voice_layer: false
    may_host_full_memory: true
    may_host_codegen: true
    may_host_simulation: true

rules:
  - node role does not imply automatic trust
  - simulation and codegen hosting remain separately governed
  - mobile roles must remain capability-bounded
YAML

cat > trust_policies.yaml <<'YAML'
schema_version: governance_trust_policies.v1
description: Canonical trust policy definitions for federation links and node scopes.

policies:
  personal_trusted:
    sync_allowed: true
    secrets_access_allowed: false
    restricted_memory_access_allowed: false

  personal_limited:
    sync_allowed: true
    secrets_access_allowed: false
    restricted_memory_access_allowed: false

  client_detached:
    sync_allowed: false
    secrets_access_allowed: false
    restricted_memory_access_allowed: false

  unknown:
    sync_allowed: false
    secrets_access_allowed: false
    restricted_memory_access_allowed: false

  denied:
    sync_allowed: false
    secrets_access_allowed: false
    restricted_memory_access_allowed: false

rules:
  - denied trust level must disable all sensitive access
  - trust never bypasses approval rules
  - runtime state sync remains forbidden even between trusted nodes
  - secrets access is separately governed and disabled by default
YAML

echo "governance configs filled successfully"
