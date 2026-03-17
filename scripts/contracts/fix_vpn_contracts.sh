#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/vpn"

cat > vpn_profile.v1.yaml <<'YAML'
contract_name: vpn_profile
schema_version: vpn_profile.v1
description: Canonical VPN profile declaration.

required:
  - profile_id
  - profile_name
  - mode

fields:
  profile_id:
    type: string
    description: Unique VPN profile identifier.

  profile_name:
    type: string
    description: Human-readable VPN profile name.

  mode:
    type: string
    enum:
      - off
      - on_demand
      - always_on
      - node_link
    description: VPN operating mode for this profile.

  allowed_nodes:
    type: array
    items:
      type: string
    description: Explicit node references allowed by this VPN profile.

  routing_policy_ref:
    type: string
    description: Reference to routing policy bound to this profile.

validation_rules:
  - profile_id required
  - profile_name required
  - mode must match allowed enum
  - allowed_nodes should be explicit even when empty

security_rules:
  - VPN remains optional
  - profile declaration does not imply automatic trust escalation
  - routing behavior remains bounded by node trust and governance policy
YAML

cat > vpn_state.v1.yaml <<'YAML'
contract_name: vpn_state
schema_version: vpn_state.v1
description: Current state of VPN layer or module.

required:
  - state_id
  - profile_ref
  - status

fields:
  state_id:
    type: string
    description: Unique VPN state record identifier.

  profile_ref:
    type: string
    description: Reference to active or selected VPN profile.

  status:
    type: string
    enum:
      - disabled
      - connecting
      - connected
      - failed
    description: Current runtime state of VPN connectivity.

  connected_peers:
    type: array
    items:
      type: string
    description: Explicit list of connected peer nodes or endpoints.

validation_rules:
  - state_id required
  - profile_ref required
  - status must match allowed enum
  - connected_peers should be explicit even when empty

security_rules:
  - no implied trust escalation
  - vpn state records do not authorize route or profile mutation
  - peer visibility follows trust and access policy
YAML

cat > vpn_policy.v1.yaml <<'YAML'
contract_name: vpn_policy
schema_version: vpn_policy.v1
description: Policy controlling VPN usage in different contexts.

required:
  - policy_id
  - applies_to

fields:
  policy_id:
    type: string
    description: Unique VPN policy identifier.

  applies_to:
    type: string
    description: Context, profile, product, or shell scope this policy applies to.

  auto_enable_allowed:
    type: boolean
    description: Whether VPN may auto-enable in this scope.

  auto_disable_allowed:
    type: boolean
    description: Whether VPN may auto-disable in this scope.

  user_confirmation_required:
    type: boolean
    description: Whether explicit user confirmation is required for policy-driven changes.

validation_rules:
  - policy_id required
  - applies_to required
  - policy booleans should be explicit

security_rules:
  - VPN policy cannot override node trust policy
  - policy does not bypass approval requirements for sensitive route changes
  - auto behavior remains bounded by governance
YAML

cat > vpn_route.v1.yaml <<'YAML'
contract_name: vpn_route
schema_version: vpn_route.v1
description: Route declaration for VPN node traffic.

required:
  - route_id
  - source_scope
  - target_scope

fields:
  route_id:
    type: string
    description: Unique VPN route identifier.

  source_scope:
    type: string
    description: Source node, group, or federation scope.

  target_scope:
    type: string
    description: Target node, group, or federation scope.

  enabled:
    type: boolean
    description: Whether this route is currently enabled.

validation_rules:
  - route_id required
  - source_scope required
  - target_scope required
  - enabled must be explicit

security_rules:
  - route changes may require approval
  - routing does not imply trust escalation
  - route definitions remain bounded by policy and federation trust
YAML

echo "vpn contracts restored successfully"
