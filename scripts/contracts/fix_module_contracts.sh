#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/module"

cat > module_manifest.v1.yaml <<'YAML'
contract_name: module_manifest
schema_version: module_manifest.v1
description: Canonical module declaration for cubes and domain modules.

required:
  - module_id
  - module_name
  - version
  - supported_platforms

fields:
  module_id:
    type: string
    description: Unique module identifier.

  module_name:
    type: string
    description: Human-readable module name.

  version:
    type: string
    description: Version string of the module manifest.

  description:
    type: string
    description: Short semantic description of module purpose.

  supported_platforms:
    type: array
    items:
      type: string
    description: Explicit list of supported shells or platforms.

  requires_backend:
    type: boolean
    description: Whether this module requires external backend or server support.

  can_run_standalone:
    type: boolean
    description: Whether this module can run without backend federation support.

  actions:
    type: array
    items:
      type: string
    description: Action primitives exposed or required by this module.

  workflows:
    type: array
    items:
      type: string
    description: Workflow identifiers bundled with or referenced by this module.

  dashboard_ref:
    type: string
    description: Reference to dashboard manifest bound to this module.

validation_rules:
  - module_id must be unique
  - version required
  - supported_platforms must not be empty
  - actions and workflows should be explicit even when empty

security_rules:
  - module capabilities must be bounded by permission matrix
  - module manifest does not grant execution authority by itself
  - module metadata must not contain hidden privileged commands
YAML

cat > module_permission_matrix.v1.yaml <<'YAML'
contract_name: module_permission_matrix
schema_version: module_permission_matrix.v1
description: Permission matrix scoped to one module.

required:
  - module_id
  - permissions

fields:
  module_id:
    type: string
    description: Module governed by this permission matrix.

  permissions:
    type: object
    additional_properties: true
    description: Structured permission mapping for module resources, actions, and contexts.

validation_rules:
  - module_id required
  - permissions must be explicit object
  - permission keys should map only to declared module surfaces or actions

security_rules:
  - module permissions cannot exceed global permission matrix
  - deny by default for undeclared resources
  - permission scope must remain bounded to module contract
YAML

cat > module_dependency.v1.yaml <<'YAML'
contract_name: module_dependency
schema_version: module_dependency.v1
description: Canonical module dependency declaration.

required:
  - module_id
  - depends_on

fields:
  module_id:
    type: string
    description: Module declaring dependencies.

  depends_on:
    type: array
    items:
      type: string
    description: Required module dependencies.

  optional_dependencies:
    type: array
    items:
      type: string
    description: Optional dependencies that enhance behavior but are not required.

validation_rules:
  - circular dependencies not allowed
  - module_id required
  - depends_on should be explicit even when empty
  - dependency references should target known module identifiers

security_rules:
  - dependencies do not imply trust
  - optional dependencies must not silently elevate module permissions
  - dependency loading must remain policy-governed
YAML

cat > module_lifecycle.v1.yaml <<'YAML'
contract_name: module_lifecycle
schema_version: module_lifecycle.v1
description: Module lifecycle state contract.

required:
  - module_id
  - lifecycle_state

fields:
  module_id:
    type: string
    description: Module whose lifecycle is being tracked.

  lifecycle_state:
    type: string
    enum:
      - registered
      - installed
      - enabled
      - disabled
      - removed
    description: Current lifecycle state of the module.

  installed_at:
    type: string
    format: date-time
    description: UTC timestamp of install registration.

  last_changed_at:
    type: string
    format: date-time
    description: UTC timestamp of latest lifecycle transition.

validation_rules:
  - lifecycle_state required
  - lifecycle_state must match allowed enum
  - last_changed_at should not be earlier than installed_at when both exist

security_rules:
  - lifecycle transitions require policy
  - enabled state does not bypass approval or action governance
  - removed modules must not remain executable
YAML

cat > module_compatibility.v1.yaml <<'YAML'
contract_name: module_compatibility
schema_version: module_compatibility.v1
description: Compatibility matrix for module across shells and products.

required:
  - module_id
  - supports_server
  - supports_desktop
  - supports_android
  - supports_ios

fields:
  module_id:
    type: string
    description: Module being described.

  supports_server:
    type: boolean
    description: Whether module supports server shell.

  supports_desktop:
    type: boolean
    description: Whether module supports desktop shell.

  supports_android:
    type: boolean
    description: Whether module supports Android shell.

  supports_ios:
    type: boolean
    description: Whether module supports iOS shell.

  requires_backend:
    type: boolean
    description: Whether module requires backend service even when shell is supported.

  supported_products:
    type: array
    items:
      type: string
    description: Product identifiers in which this module may be bundled.

validation_rules:
  - module_id required
  - compatibility booleans must be explicit
  - supported_products should be explicit for distributable modules

security_rules:
  - compatibility does not imply automatic activation
  - backend-required modules must not be promoted to standalone mode silently
  - shell support must still obey capability profiles and governance
YAML

echo "module contracts restored successfully"
