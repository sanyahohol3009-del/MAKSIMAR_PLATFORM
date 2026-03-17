#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/CODEGEN_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > codegen_policy.yaml <<'YAML'
schema_version: codegen_policy.v1
description: Canonical top-level policy for code generation layer.

pipeline:
  task_to_spec_enabled: true
  spec_to_module_enabled: true
  diff_generation_enabled: true
  proposal_packaging_enabled: true

defaults:
  direct_apply_forbidden: true
  human_review_required: true
  manifest_generation_required: true
  tests_required_before_promotion: true

rules:
  - code generation is proposal-oriented, not direct authority
  - generated code must remain bounded by module and governance contracts
  - codegen must not write to CORE_ROOT
YAML

cat > sandbox_policy.yaml <<'YAML'
schema_version: codegen_sandbox_policy.v1
description: Canonical sandbox policy for generated code execution and validation.

sandbox:
  isolated_workspace_required: true
  no_upward_write: true
  artifact_export_only: true
  network_disabled_by_default: true
  resource_limits_required: true

limits:
  cpu_limit_required: true
  memory_limit_required: true
  timeout_required: true

rules:
  - generated code must execute only inside sandbox
  - sandbox outputs are evidence and artifacts, not deployment
  - sandbox must not mutate privileged runtime state
YAML

cat > proposal_policy.yaml <<'YAML'
schema_version: codegen_proposal_policy.v1
description: Canonical policy for proposal creation and promotion of generated code.

proposal:
  diff_required: true
  spec_reference_required: true
  review_summary_required: true
  approval_required: true

promotion:
  auto_promote_forbidden: true
  failing_eval_blocks_promotion: true
  failing_tests_block_promotion: true
  lint_fail_blocks_promotion: true
  typecheck_fail_blocks_promotion: true

rules:
  - no generated diff may bypass proposal stage
  - approval remains mandatory before any promotion
  - failed validation artifacts must remain visible
YAML

cat > lint_typecheck_test_policy.yaml <<'YAML'
schema_version: codegen_validation_policy.v1
description: Canonical validation policy for generated code quality gates.

validation:
  lint_required: true
  typecheck_required: true
  tests_required: true
  structured_reports_required: true

gates:
  lint_must_pass: true
  typecheck_must_pass: true
  tests_must_pass: true
  partial_success_not_sufficient: true

rules:
  - generated code must pass all declared validation gates
  - reports must remain attached to proposal package
  - validation cannot be silently skipped
YAML

echo "codegen configs filled successfully"
