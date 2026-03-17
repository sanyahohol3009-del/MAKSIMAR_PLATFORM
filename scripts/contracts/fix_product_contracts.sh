#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/product"

cat > product_manifest.v1.yaml <<'YAML'
contract_name: product_manifest
schema_version: product_manifest.v1
description: Canonical definition of a deployable JARVIS product configuration.

required:
  - product_id
  - name
  - supported_nodes
  - modules

fields:
  product_id:
    type: string
    description: Unique product identifier.

  name:
    type: string
    description: Human-readable product name.

  description:
    type: string
    description: Short description of the product configuration.

  supported_nodes:
    type: array
    items:
      type: string
    description: Node types capable of running this product.

  modules:
    type: array
    items:
      type: string
    description: Module identifiers bundled in the product.

  workflows:
    type: array
    items:
      type: string
    description: Workflow identifiers included in the product.

  capability_profile_ref:
    type: string
    description: Capability profile applied to this product.

validation_rules:
  - product_id must be unique
  - modules must not be empty
  - supported_nodes must be explicit
  - workflows should be explicit even when empty

security_rules:
  - product manifest does not grant permissions by itself
  - modules must still obey module permission matrices
  - workflows must obey approval policies
YAML

cat > product_profile.v1.yaml <<'YAML'
contract_name: product_profile
schema_version: product_profile.v1
description: Canonical product capability profile.

required:
  - profile_id
  - allowed_modules

fields:
  profile_id:
    type: string
    description: Unique capability profile identifier.

  allowed_modules:
    type: array
    items:
      type: string
    description: Modules allowed in this product profile.

  forbidden_modules:
    type: array
    items:
      type: string
    description: Explicitly forbidden modules.

  allowed_actions:
    type: array
    items:
      type: string
    description: Actions permitted under this profile.

validation_rules:
  - profile_id required
  - allowed_modules must be explicit
  - forbidden_modules must not overlap allowed_modules

security_rules:
  - forbidden modules must never activate
  - capability profiles must not bypass governance
  - profiles must remain auditable
YAML

cat > product_bundle.v1.yaml <<'YAML'
contract_name: product_bundle
schema_version: product_bundle.v1
description: Bundle definition grouping products for distribution.

required:
  - bundle_id
  - products

fields:
  bundle_id:
    type: string
    description: Unique bundle identifier.

  products:
    type: array
    items:
      type: string
    description: Product identifiers included in the bundle.

  distribution_targets:
    type: array
    items:
      type: string
    description: Target platforms or markets.

validation_rules:
  - bundle_id required
  - products must not be empty
  - products should reference known product identifiers

security_rules:
  - bundle does not grant module execution authority
  - distribution targets must respect regional policy constraints
  - bundle composition must remain auditable
YAML

cat > product_deployment.v1.yaml <<'YAML'
contract_name: product_deployment
schema_version: product_deployment.v1
description: Deployment record of a product instance.

required:
  - deployment_id
  - product_id
  - node_id

fields:
  deployment_id:
    type: string
    description: Unique deployment identifier.

  product_id:
    type: string
    description: Product deployed on the node.

  node_id:
    type: string
    description: Node running the product instance.

  deployed_at:
    type: string
    format: date-time
    description: UTC timestamp of deployment.

  deployment_mode:
    type: string
    description: Deployment mode applied.

validation_rules:
  - product_id required
  - node_id required
  - deployment_id must be unique

security_rules:
  - deployment does not bypass node trust policy
  - deployment must respect module lifecycle state
  - deployment records must remain auditable
YAML

cat > product_lifecycle.v1.yaml <<'YAML'
contract_name: product_lifecycle
schema_version: product_lifecycle.v1
description: Lifecycle state of product configuration.

required:
  - product_id
  - lifecycle_state

fields:
  product_id:
    type: string
    description: Product being tracked.

  lifecycle_state:
    type: string
    enum:
      - registered
      - deployed
      - deprecated
      - removed
    description: Current lifecycle state.

  last_changed_at:
    type: string
    format: date-time
    description: Timestamp of latest lifecycle transition.

validation_rules:
  - lifecycle_state must match allowed enum
  - product_id required

security_rules:
  - deprecated products must not deploy new instances
  - removed products must not remain active
  - lifecycle changes require governance approval
YAML

echo "product contracts restored successfully"
