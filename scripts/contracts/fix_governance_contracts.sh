#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/governance"

cat > risk_matrix.v1.yaml <<'YAML'
contract_name: risk_matrix
schema_version: risk_matrix.v1
description: Canonical risk classification matrix.

required:
  - levels

fields:
  levels:
    type: object
    properties:
      safe:
        type: object
        description: Low-risk operations that may execute without additional approval under allowed policy.
      sensitive:
        type: object
        description: Medium-risk operations requiring explicit confirmation or context-dependent approval.
      dangerous:
        type: object
        description: High-risk operations requiring strict approval controls.
      blocked:
        type: object
        description: Operations that are non-executable under current governance rules.

validation_rules:
  - all four levels must exist
  - levels must be explicitly named safe, sensitive, dangerous, and blocked
  - blocked level must remain non-executable by downstream policy

security_rules:
  - blocked level is non-executable
  - risk matrix is policy-defining metadata
  - no execution authority is embedded in the matrix itself
YAML

cat > approval_policy.v1.yaml <<'YAML'
contract_name: approval_policy
schema_version: approval_policy.v1
description: Canonical approval rules for actions, workflows, proposals, and deploys.

required:
  - policy_id
  - applies_to
  - approval_required

fields:
  policy_id:
    type: string
    description: Unique approval policy identifier.

  applies_to:
    type: string
    description: Exact target scope this policy applies to, such as action, workflow, proposal, or deploy path.

  approval_required:
    type: boolean
    description: Whether explicit approval is required before execution or promotion.

  approval_type:
    type: string
    enum:
      - none
      - confirm_once
      - strict
      - hardware_key
      - operator_pair
    description: Type of approval mechanism required.

  voice_confirmation_required:
    type: boolean
    description: Whether voice confirmation is mandatory.

  hardware_key_required:
    type: boolean
    description: Whether hardware key confirmation is mandatory.

  delay_buffer_sec:
    type: integer
    description: Delay buffer in seconds before execution may proceed.

  allowed_contexts:
    type: array
    items:
      type: string
    description: Explicit contexts in which this approval policy may apply.

validation_rules:
  - blocked policies must not authorize execution
  - approval_type must match allowed enum when present
  - delay_buffer_sec must be non-negative when present
  - allowed_contexts should be explicit for non-global policies

security_rules:
  - approval policy is authoritative
  - approval rules do not grant execution by themselves
  - stricter approval requirements must not be silently weakened downstream
YAML

cat > permission_matrix.v1.yaml <<'YAML'
contract_name: permission_matrix
schema_version: permission_matrix.v1
description: Canonical permission matrix for roles, modules, and actions.

required:
  - roles
  - resources
  - permissions

fields:
  roles:
    type: array
    items:
      type: string
    description: Explicit list of roles recognized by the permission system.

  resources:
    type: array
    items:
      type: string
    description: Explicit list of protected resources, domains, or action groups.

  permissions:
    type: object
    additional_properties: true
    description: Structured permission bindings between roles and resources.

validation_rules:
  - roles and resources must be explicit
  - no wildcard global write by default
  - every permission entry should map to declared roles and resources
  - deny-by-default assumption must hold for unspecified combinations

security_rules:
  - deny by default
  - permissions do not override immutable restrictions
  - no implicit privileged escalation allowed
YAML

cat > capability_profile.v1.yaml <<'YAML'
contract_name: capability_profile
schema_version: capability_profile.v1
description: Capability subset contract for portable core deployments.

required:
  - profile_id
  - profile_name
  - enabled_capabilities

fields:
  profile_id:
    type: string
    description: Unique capability profile identifier.

  profile_name:
    type: string
    description: Human-readable profile name.

  enabled_capabilities:
    type: array
    items:
      type: string
    description: Explicit set of capabilities enabled in this profile.

  disabled_capabilities:
    type: array
    items:
      type: string
    description: Explicit set of capabilities disabled in this profile.

  target_products:
    type: array
    items:
      type: string
    description: Product families or bundles intended to use this profile.

validation_rules:
  - enabled and disabled sets must not conflict
  - enabled_capabilities must not be empty
  - target_products should be explicit when profile is product-bound

security_rules:
  - capability profile cannot override immutable governance
  - forbidden capabilities must remain forbidden even if listed accidentally
  - profile selection does not bypass approval policy
YAML

cat > deployment_mode.v1.yaml <<'YAML'
contract_name: deployment_mode
schema_version: deployment_mode.v1
description: Canonical deployment mode definition.

required:
  - mode_id
  - mode_name
  - shell_targets
  - capability_profile_ref

fields:
  mode_id:
    type: string
    description: Unique deployment mode identifier.

  mode_name:
    type: string
    description: Human-readable deployment mode name.

  shell_targets:
    type: array
    items:
      type: string
    description: Explicit shells targeted by this deployment mode.

  capability_profile_ref:
    type: string
    description: Reference to the capability profile used by this mode.

  standalone:
    type: boolean
    description: Whether the deployment may operate standalone.

  backend_required:
    type: boolean
    description: Whether backend support is mandatory for this mode.

validation_rules:
  - shell_targets must be explicit
  - capability_profile_ref required
  - shell_targets should not contain duplicates

security_rules:
  - mode cannot grant forbidden core rights
  - deployment mode does not bypass shell boundaries
  - standalone mode does not imply unrestricted local authority
YAML

cat > trust_policy.v1.yaml <<'YAML'
contract_name: trust_policy
schema_version: trust_policy.v1
description: Canonical trust policy for nodes and sync relationships.

required:
  - trust_policy_id
  - trust_level
  - applies_to

fields:
  trust_policy_id:
    type: string
    description: Unique trust policy identifier.

  trust_level:
    type: string
    enum:
      - personal_trusted
      - personal_limited
      - client_detached
      - unknown
      - denied
    description: Trust tier assigned to a node, link, or sync relationship.

  applies_to:
    type: string
    description: Exact target scope this trust policy applies to.

  sync_allowed:
    type: boolean
    description: Whether synchronization is allowed.

  secrets_access_allowed:
    type: boolean
    description: Whether secrets access is allowed.

  restricted_memory_access_allowed:
    type: boolean
    description: Whether restricted memory access is allowed.

validation_rules:
  - denied trust level must disable all sensitive access
  - trust_level must match allowed enum
  - applies_to must be explicit

security_rules:
  - trust does not bypass approval rules
  - denied remains strongest effective state
  - secrets and restricted memory require explicit separate allowance
YAML

cat > node_role.v1.yaml <<'YAML'
contract_name: node_role
schema_version: node_role.v1
description: Canonical role definition for JARVIS nodes.

required:
  - role_id
  - role_name
  - execution_scope

fields:
  role_id:
    type: string
    description: Unique node role identifier.

  role_name:
    type: string
    description: Human-readable node role name.

  execution_scope:
    type: string
    description: Declared scope of execution authority or operational responsibility.

  may_host_voice_layer:
    type: boolean
    description: Whether this role may host a voice layer.

  may_host_full_memory:
    type: boolean
    description: Whether this role may host full memory system features.

  may_host_codegen:
    type: boolean
    description: Whether this role may host code generation features.

  may_host_simulation:
    type: boolean
    description: Whether this role may host simulation features.

validation_rules:
  - role_name must be unique
  - execution_scope must be explicit
  - hosting flags must be explicit booleans when present

security_rules:
  - node role does not imply automatic trust
  - node role does not override approval or permission policy
  - privileged hosting flags remain bounded by governance
YAML

echo "governance contracts restored successfully"
