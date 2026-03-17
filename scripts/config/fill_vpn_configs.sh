#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/VPN_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > vpn_profiles.yaml <<'YAML'
schema_version: vpn_profiles_config.v1
description: Canonical VPN profile configuration for optional secure routing modes.

profiles:
  off:
    enabled: true
    mode: off

  on_demand:
    enabled: true
    mode: on_demand

  always_on:
    enabled: true
    mode: always_on

  node_link:
    enabled: true
    mode: node_link

rules:
  - VPN remains optional by design
  - profile selection must remain explicit
  - profile config does not imply trust escalation
YAML

cat > vpn_policy.yaml <<'YAML'
schema_version: vpn_policy_config.v1
description: Canonical policy for VPN enablement, disablement, and guarded usage.

policy:
  auto_enable_allowed: true
  auto_disable_allowed: true
  user_confirmation_required_for_sensitive_contexts: true
  trust_policy_binding_required: true

restrictions:
  no_trust_override: true
  no_hidden_activation: true
  no_policy_bypass: true

rules:
  - VPN policy cannot override node trust policy
  - sensitive context changes must remain reviewable
  - activation path must remain auditable
YAML

cat > vpn_routing.yaml <<'YAML'
schema_version: vpn_routing_config.v1
description: Canonical routing configuration for VPN-mediated node traffic.

routing:
  node_to_node_routes_enabled: true
  split_tunnel_allowed: true
  full_tunnel_allowed: true
  routing_scope_must_be_explicit: true

validation:
  source_scope_required: true
  target_scope_required: true
  route_enablement_explicit: true

rules:
  - route declarations must remain explicit
  - routing config does not imply automatic activation
  - routing must remain bounded by trust and policy
YAML

cat > vpn_autostart.yaml <<'YAML'
schema_version: vpn_autostart_config.v1
description: Canonical autostart policy for VPN behavior across products, shells, and contexts.

autostart:
  desktop_allowed: true
  android_allowed: true
  ios_allowed: true
  server_allowed: true
  family_mode_default: false
  engineering_mode_default: false

requirements:
  explicit_profile_required: true
  policy_check_required: true
  user_override_allowed: true

rules:
  - autostart must remain optional
  - autostart must not silently force always-on mode
  - product defaults must remain overridable where policy allows
YAML

echo "vpn configs filled successfully"
