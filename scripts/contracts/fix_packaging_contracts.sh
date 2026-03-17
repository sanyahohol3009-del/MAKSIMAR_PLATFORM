#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/packaging"

cat > packaging_profile.v1.yaml <<'YAML'
contract_name: packaging_profile
schema_version: packaging_profile.v1
description: Packaging profile for assembly of deliverables.

required:
  - packaging_id
  - target_product
  - shell_targets

fields:
  packaging_id:
    type: string
    description: Unique packaging profile identifier.

  target_product:
    type: string
    description: Target product identifier assembled by this packaging profile.

  shell_targets:
    type: array
    items:
      type: string
    description: Explicit shells included in the packaging output.

  asset_groups:
    type: array
    items:
      type: string
    description: Asset groups included in the package.

  include_debug_tools:
    type: boolean
    description: Whether debug or operator tooling is included in the package.

validation_rules:
  - packaging_id required
  - target_product required
  - shell_targets must not be empty
  - asset_groups should be explicit even when empty

security_rules:
  - debug tools excluded by default in client bundles
  - packaging profile does not grant execution authority
  - packaging must respect product and governance constraints
YAML

cat > bundle_selector.v1.yaml <<'YAML'
contract_name: bundle_selector
schema_version: bundle_selector.v1
description: Selector rules for choosing bundle variants.

required:
  - selector_id
  - conditions
  - target_bundle

fields:
  selector_id:
    type: string
    description: Unique selector identifier.

  conditions:
    type: object
    additional_properties: true
    description: Structured conditions used to choose a bundle.

  target_bundle:
    type: string
    description: Bundle identifier selected when conditions match.

validation_rules:
  - selector_id required
  - target_bundle required
  - conditions must be explicit

security_rules:
  - selector cannot override policy constraints
  - selector logic must remain auditable
  - selector does not grant capability expansion
YAML

cat > capability_subset.v1.yaml <<'YAML'
contract_name: capability_subset
schema_version: capability_subset.v1
description: Explicit subset of capabilities included in one package.

required:
  - subset_id
  - included_capabilities

fields:
  subset_id:
    type: string
    description: Unique capability subset identifier.

  included_capabilities:
    type: array
    items:
      type: string
    description: Capabilities explicitly included in this package.

  excluded_capabilities:
    type: array
    items:
      type: string
    description: Capabilities explicitly excluded from this package.

validation_rules:
  - subset_id required
  - included_capabilities required
  - included_capabilities must be explicit
  - excluded_capabilities must not overlap included_capabilities

security_rules:
  - forbidden capabilities may not be reintroduced by subset
  - subset selection must respect governance and product limits
  - capability subsets do not grant authority by themselves
YAML

echo "packaging contracts restored successfully"
