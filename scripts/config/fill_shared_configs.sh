#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/SHARED/config"
mkdir -p "$BASE"
cd "$BASE"

cat > shared_profiles.yaml <<'YAML'
schema_version: shared_profiles.v1
description: Canonical shared profile registry for cross-platform portable-core coordination.

profiles:
  default_shared:
    enabled: true
    description: Baseline shared profile for all shells.

  engineering_shared:
    enabled: true
    description: Shared profile for engineering-oriented products and nodes.

  family_shared:
    enabled: true
    description: Shared profile for family-oriented products and assistants.

rules:
  - shared profiles must remain explicit
  - shared profiles do not override governance
  - cross-platform coordination must remain auditable
YAML

cat > product_profiles.yaml <<'YAML'
schema_version: shared_product_profiles.v1
description: Canonical shared product profile bindings for packaging and shells.

products:
  jarvis_full_platform:
    enabled: true

  jarvis_family:
    enabled: true

  jarvis_engineering:
    enabled: true

  jarvis_mobile_consumer:
    enabled: true

  jarvis_desktop_consumer:
    enabled: true

  jarvis_industrial:
    enabled: true

rules:
  - product profile identifiers must remain explicit
  - shared product profiles are references, not authority
  - shell and capability bindings must stay consistent
YAML

cat > capability_profiles.yaml <<'YAML'
schema_version: shared_capability_profiles.v1
description: Canonical shared capability profiles for portable-core deployments.

profiles:
  core_profile_full_platform:
    enabled: true

  core_profile_mobile_consumer:
    enabled: true

  core_profile_desktop_consumer:
    enabled: true

  core_profile_industrial:
    enabled: true

rules:
  - capability profiles must remain explicit and versionable
  - shared capability profiles do not bypass governance restrictions
  - disabled capabilities must not silently reactivate downstream
YAML

cat > shell_compatibility.yaml <<'YAML'
schema_version: shared_shell_compatibility.v1
description: Canonical shell compatibility policy across server, desktop, android, and ios.

shells:
  server:
    enabled: true

  desktop:
    enabled: true

  android:
    enabled: true

  ios:
    enabled: true

compatibility_rules:
  shared_contracts_required: true
  shared_action_definitions_required: true
  shared_workflow_schemas_required: true
  shared_ui_tokens_required: true

rules:
  - shells must remain compatible through shared contracts
  - shell compatibility does not imply equal capability
  - shared layer is coordination layer, not privileged execution layer
YAML

echo "shared configs filled successfully"
