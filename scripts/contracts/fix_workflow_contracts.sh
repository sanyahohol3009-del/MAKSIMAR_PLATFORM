#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/workflow"

cat > workflow_definition.v1.yaml <<'YAML'
contract_name: workflow_definition
schema_version: workflow_definition.v1
description: Canonical workflow definition for orchestration layer.

required:
  - workflow_id
  - name
  - source
  - steps
  - risk_level
  - approval_required
  - status

fields:
  workflow_id:
    type: string
    description: Unique workflow identifier.

  name:
    type: string
    description: Human-readable workflow name.

  description:
    type: string
    description: Short semantic description of workflow purpose.

  source:
    type: string
    enum:
      - voice_generated
      - text_generated
      - manual_debug
      - optimization_suggested
      - imported
    description: Origin of workflow creation.

  trigger_phrases:
    type: array
    items:
      type: string
    description: Bound trigger phrases or aliases for workflow activation.

  steps:
    type: array
    items:
      type: object
    description: Ordered action-step sequence executed by the workflow.

  risk_level:
    type: string
    enum:
      - safe
      - sensitive
      - dangerous
      - blocked
    description: Aggregate workflow risk classification.

  approval_required:
    type: boolean
    description: Whether approval is required before workflow execution.

  contexts:
    type: array
    items:
      type: string
    description: Supported execution contexts for the workflow.

  created_at:
    type: string
    format: date-time
    description: UTC creation timestamp.

  last_used_at:
    type: string
    format: date-time
    description: UTC timestamp of last successful or attempted use.

  usage_count:
    type: integer
    minimum: 0
    description: Execution count tracked for analytics and optimization.

  status:
    type: string
    enum:
      - draft
      - active
      - disabled
      - archived
    description: Workflow lifecycle status.

validation_rules:
  - workflow_id must be unique
  - steps must contain at least one element
  - risk_level must match allowed enum
  - blocked workflows must not be executable
  - usage_count must not be negative

security_rules:
  - workflow definition is not execution authority by itself
  - workflow risk must not override action-level blocking
  - workflow metadata must not embed hidden privileged commands
YAML

cat > action_step.v1.yaml <<'YAML'
contract_name: action_step
schema_version: action_step.v1
description: Canonical action step inside a workflow definition.

required:
  - step_id
  - action_type
  - parameters
  - risk_level

fields:
  step_id:
    type: string
    description: Unique workflow-local step identifier.

  action_type:
    type: string
    description: Action primitive referenced from action library.

  parameters:
    type: object
    additional_properties: true
    description: Structured parameter payload for this step.

  preconditions:
    type: array
    items:
      type: string
    description: Preconditions that should hold before execution.

  postconditions:
    type: array
    items:
      type: string
    description: Expected state assertions after execution.

  timeout_sec:
    type: number
    minimum: 0.1
    description: Maximum allowed runtime for this step.

  rollback_policy:
    type: string
    enum:
      - none
      - best_effort
      - strict
    description: Rollback policy if step fails or chain aborts.

  risk_level:
    type: string
    enum:
      - safe
      - sensitive
      - dangerous
      - blocked
    description: Step-level risk classification.

validation_rules:
  - action_type must reference approved action library entry
  - timeout_sec must be positive when present
  - risk_level must match allowed enum
  - blocked steps must not be executable

security_rules:
  - step must remain bounded by action permission policy
  - parameters must not contain freeform hidden shell authority
  - rollback policy does not bypass governance
YAML

cat > trigger_phrase.v1.yaml <<'YAML'
contract_name: trigger_phrase
schema_version: trigger_phrase.v1
description: Canonical trigger phrase record for workflow activation.

required:
  - trigger_id
  - phrase
  - language
  - enabled
  - linked_workflow_id

fields:
  trigger_id:
    type: string
    description: Unique trigger identifier.

  phrase:
    type: string
    description: Primary activation phrase.

  aliases:
    type: array
    items:
      type: string
    description: Optional alternative phrases mapped to the same workflow.

  language:
    type: string
    description: Language code associated with this trigger.

  enabled:
    type: boolean
    description: Whether the trigger is currently allowed to resolve.

  linked_workflow_id:
    type: string
    description: Workflow identifier bound to this trigger.

  created_at:
    type: string
    format: date-time
    description: UTC creation timestamp.

  last_used_at:
    type: string
    format: date-time
    description: UTC timestamp of most recent trigger use.

validation_rules:
  - phrase must not be empty
  - linked_workflow_id required
  - disabled triggers must not execute
  - aliases should not duplicate phrase or each other

security_rules:
  - trigger phrases do not bypass approval policy
  - disabled triggers must remain non-executable
  - trigger resolution must respect context and trust policies
YAML

cat > workflow_execution.v1.yaml <<'YAML'
contract_name: workflow_execution
schema_version: workflow_execution.v1
description: Canonical execution record for workflow runs.

required:
  - execution_id
  - workflow_id
  - started_at
  - status

fields:
  execution_id:
    type: string
    description: Unique workflow execution identifier.

  workflow_id:
    type: string
    description: Workflow being executed.

  trigger_source:
    type: string
    enum:
      - voice
      - text
      - manual_run
      - scheduled
      - api
    description: Source of activation for this workflow run.

  started_at:
    type: string
    format: date-time
    description: UTC start timestamp.

  finished_at:
    type: string
    format: date-time
    description: UTC finish timestamp.

  status:
    type: string
    enum:
      - success
      - failed
      - cancelled
      - blocked_by_policy
      - awaiting_approval
      - partial_success
    description: Final or current execution status.

  executed_steps:
    type: array
    items:
      type: string
    description: Step identifiers that executed before terminal state.

  failed_step:
    type: string
    description: Step identifier that caused failure or halt.

  failure_reason:
    type: string
    description: Human-readable or structured failure reason.

  approval_path:
    type: object
    additional_properties: true
    description: Approval trace used for this execution.

  operator_context:
    type: object
    additional_properties: true
    description: Runtime operator or shell context associated with the run.

validation_rules:
  - workflow_id required
  - status must match allowed enum
  - started_at required
  - failed and blocked statuses should carry reason
  - executed_steps should preserve execution order

security_rules:
  - execution record is evidence only
  - blocked_by_policy status must remain visible
  - approval trace must not be silently dropped
YAML

cat > optimization_suggestion.v1.yaml <<'YAML'
contract_name: optimization_suggestion
schema_version: optimization_suggestion.v1
description: Suggestion record generated from repeated execution patterns.

required:
  - suggestion_id
  - suggested_name
  - suggested_steps
  - confidence
  - risk_level
  - status

fields:
  suggestion_id:
    type: string
    description: Unique optimization suggestion identifier.

  based_on_executions:
    type: array
    items:
      type: string
    description: Supporting execution identifiers used to derive the suggestion.

  suggested_name:
    type: string
    description: Proposed human-readable workflow name.

  suggested_trigger_phrase:
    type: string
    description: Proposed trigger phrase for accepted workflow creation.

  suggested_steps:
    type: array
    items:
      type: object
    description: Proposed workflow steps inferred from repeated behavior.

  confidence:
    type: number
    minimum: 0.0
    maximum: 1.0
    description: Confidence score assigned to the suggestion.

  risk_level:
    type: string
    enum:
      - safe
      - sensitive
      - dangerous
      - blocked
    description: Risk level of the proposed optimization.

  requires_human_confirmation:
    type: boolean
    description: Whether explicit human confirmation is required before promotion.

  status:
    type: string
    enum:
      - pending
      - accepted
      - rejected
      - expired
    description: Suggestion lifecycle state.

  created_at:
    type: string
    format: date-time
    description: UTC creation timestamp.

validation_rules:
  - suggested_steps required
  - confidence must remain within 0.0..1.0
  - risk_level must match allowed enum
  - blocked suggestions must not be auto-promoted

security_rules:
  - suggestions do not create workflows automatically
  - human confirmation required where policy demands
  - inferred suggestions must preserve supporting execution lineage
YAML

cat > action_result.v1.yaml <<'YAML'
contract_name: action_result
schema_version: action_result.v1
description: Canonical result of one workflow action step.

required:
  - action_result_id
  - step_id
  - status

fields:
  action_result_id:
    type: string
    description: Unique action-result identifier.

  step_id:
    type: string
    description: Workflow step identifier this result belongs to.

  status:
    type: string
    enum:
      - success
      - failed
      - skipped
      - blocked
    description: Step result status.

  started_at:
    type: string
    format: date-time
    description: UTC step start timestamp.

  finished_at:
    type: string
    format: date-time
    description: UTC step finish timestamp.

  output:
    type: object
    additional_properties: true
    description: Structured step output payload.

  error:
    type: string
    description: Human-readable or structured error reason when step fails.

validation_rules:
  - blocked and failed should carry reason
  - status must match allowed enum
  - step_id required
  - finished_at should not be earlier than started_at when both exist

security_rules:
  - output must not include secrets unless allowed by policy
  - blocked step results must remain visible to diagnostics
  - action results do not imply future approval reuse
YAML

cat > workflow_template.v1.yaml <<'YAML'
contract_name: workflow_template
schema_version: workflow_template.v1
description: Reusable template for workflow creation.

required:
  - template_id
  - name
  - steps

fields:
  template_id:
    type: string
    description: Unique workflow template identifier.

  name:
    type: string
    description: Human-readable template name.

  description:
    type: string
    description: Short semantic description of template purpose.

  steps:
    type: array
    items:
      type: object
    description: Ordered template steps used to create workflow instances.

  target_contexts:
    type: array
    items:
      type: string
    description: Execution contexts this template is designed for.

validation_rules:
  - steps required
  - template_id must be unique
  - target_contexts should be explicit when template is context-bound

security_rules:
  - template itself does not execute
  - template must still pass workflow validation before activation
  - templates do not bypass approval requirements
YAML

echo "workflow contracts restored successfully"
