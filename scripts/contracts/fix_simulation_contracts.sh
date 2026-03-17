#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/simulation"

cat > simulation_request.v1.yaml <<'YAML'
contract_name: simulation_request
schema_version: simulation_request.v1
description: Canonical simulation request entering backend-agnostic simulation layer.

required:
  - request_id
  - created_at
  - source_module
  - scenario_type
  - environment_id
  - robot_model_id
  - candidate_id
  - controller_ref
  - metrics_required
  - stop_conditions
  - runtime_policy

fields:
  request_id:
    type: string
    description: Unique simulation request identifier.

  created_at:
    type: string
    format: date-time
    description: UTC timestamp when the request was created.

  source_module:
    type: string
    enum:
      - EVOLUTION_ENGINE
      - ROBOTICS_MODULE
      - ENGINEERING_INTERPRETER
      - CONTROL_PLANE
    description: Originating module for the simulation request.

  scenario_type:
    type: string
    enum:
      - cartpole
      - quadruped_locomotion
      - manipulator_pick_place
      - cnc_motion
      - printer_motion
      - digital_twin_validation
    description: High-level scenario type requested for execution.

  environment_id:
    type: string
    description: Identifier of the simulation environment contract.

  robot_model_id:
    type: string
    description: Identifier of the robot or mechanism model used in the run.

  candidate_id:
    type: string
    description: Identifier of controller, policy, or candidate artifact under evaluation.

  controller_ref:
    type: object
    description: Structured reference to controller or policy artifact.
    required:
      - type
      - location
      - format
    properties:
      type:
        type: string
        enum:
          - policy
          - controller
          - trajectory_profile
          - motion_profile
      location:
        type: string
      hash:
        type: string
      format:
        type: string
        enum:
          - json
          - yaml
          - npz
          - pkl
          - onnx
          - pt

  input_payload:
    type: object
    additional_properties: true
    description: Scenario-specific structured input parameters.

  constraints:
    type: object
    additional_properties: true
    description: Explicit physical, safety, or engineering constraints for simulation.

  metrics_required:
    type: array
    items:
      type: string
    description: Required metrics to be produced by the simulation pipeline.

  stop_conditions:
    type: object
    description: Explicit stop conditions for the run.
    required:
      - timeout_sec
    properties:
      timeout_sec:
        type: number
      max_steps:
        type: integer
      first_collision:
        type: boolean
      first_fall:
        type: boolean
      goal_reached:
        type: boolean

  runtime_policy:
    type: object
    description: Runtime sandbox policy for execution.
    required:
      - timeout_sec
      - sandbox_profile
      - gpu_allowed
    properties:
      priority:
        type: string
        enum:
          - low
          - normal
          - high
      timeout_sec:
        type: number
      retries:
        type: integer
      sandbox_profile:
        type: string
        enum:
          - sim_cpu_small
          - sim_cpu_large
          - sim_gpu_small
          - sim_gpu_large
      gpu_allowed:
        type: boolean
      cpu_limit:
        type: number
      memory_limit_mb:
        type: integer

  artifacts_policy:
    type: object
    description: Policy describing which artifacts should be retained.
    properties:
      save_logs:
        type: boolean
      save_trace:
        type: boolean
      save_video:
        type: boolean
      save_metrics:
        type: boolean
      save_failure_snapshot:
        type: boolean

validation_rules:
  - request_id must be unique within simulation queue
  - stop_conditions.timeout_sec must be defined
  - controller_ref.location must point to existing artifact before execution
  - metrics_required must not be empty
  - runtime_policy.gpu_allowed=false must be respected by backend
  - no engine-specific fields may leak into portable simulation request

security_rules:
  - no direct deploy authority
  - sandbox only
  - no write to CORE_ROOT
  - no write to approval state
  - request is execution intent, not execution permission
YAML

cat > simulation_result.v1.yaml <<'YAML'
contract_name: simulation_result
schema_version: simulation_result.v1
description: Canonical result contract for one concrete simulation run.

required:
  - request_id
  - run_id
  - started_at
  - finished_at
  - status
  - success
  - primary_outcome

fields:
  request_id:
    type: string
    description: Parent simulation request identifier.

  run_id:
    type: string
    description: Unique simulation run identifier.

  started_at:
    type: string
    format: date-time
    description: UTC timestamp when the run started.

  finished_at:
    type: string
    format: date-time
    description: UTC timestamp when the run finished.

  status:
    type: string
    enum:
      - pending
      - running
      - done
      - failed
      - aborted
      - timeout
      - invalid_request
    description: Final or current simulation run state.

  success:
    type: boolean
    description: High-level success flag for the run.

  primary_outcome:
    type: string
    enum:
      - goal_reached
      - timeout
      - fell_down
      - collision
      - constraint_exceeded
      - sim_error
      - invalid_model
      - unstable_control
      - aborted_by_policy
    description: Primary interpreted outcome of the run.

  summary:
    type: object
    description: Short normalized run summary.
    properties:
      score:
        type: number
      rank_hint:
        type: string
      notes:
        type: string
      recommendation:
        type: string

  raw_metrics:
    type: object
    additional_properties: true
    description: Numeric metrics produced by the run.

  constraint_report:
    type: object
    description: Constraint violation summary.
    properties:
      violated:
        type: boolean
      violations:
        type: array
        items:
          type: object
          required:
            - constraint_name
            - observed_value
            - allowed_value
            - severity
          properties:
            constraint_name:
              type: string
            observed_value:
              type: number
            allowed_value:
              type: number
            severity:
              type: string
              enum:
                - low
                - medium
                - high
                - critical
            timestamp_sec:
              type: number

  failure_report:
    type: object
    description: Structured failure information when run did not succeed.
    properties:
      failure_type:
        type: string
      first_failure:
        type: string
      cascade_failures:
        type: array
        items:
          type: string
      sim_trace_ref:
        type: string
      debug_hint:
        type: string

  artifacts:
    type: object
    description: Artifact references generated by simulation.
    properties:
      log_path:
        type: string
      metrics_path:
        type: string
      trace_path:
        type: string
      video_path:
        type: string
      snapshot_path:
        type: string

  environment_fingerprint:
    type: object
    description: Environment signature used for reproducibility.
    properties:
      environment_id:
        type: string
      environment_hash:
        type: string
      simulator_backend:
        type: string
      simulator_version:
        type: string

  candidate_fingerprint:
    type: object
    description: Candidate signature used during run.
    properties:
      candidate_id:
        type: string
      artifact_hash:
        type: string
      controller_format:
        type: string

validation_rules:
  - run_id must be unique
  - if status=done then raw_metrics should be present
  - if success=false then primary_outcome must not be goal_reached
  - if constraint_report.violated=true then violations must be non-empty
  - artifact paths must remain inside allowed simulation areas

security_rules:
  - result is evidence only
  - result does not grant deploy authority
  - artifact paths must remain inside sandbox or artifact areas
  - backend output must be normalized before leaving simulation layer
YAML

cat > evaluator_result.v1.yaml <<'YAML'
contract_name: evaluator_result
schema_version: evaluator_result.v1
description: Engineering interpretation of a simulation result.

required:
  - request_id
  - run_id
  - evaluator_id
  - evaluated_at
  - decision
  - score_breakdown
  - recommended_next_action

fields:
  request_id:
    type: string
    description: Parent simulation request identifier.

  run_id:
    type: string
    description: Simulation run identifier being evaluated.

  evaluator_id:
    type: string
    description: Identifier of evaluator or evaluator composition used.

  evaluated_at:
    type: string
    format: date-time
    description: UTC timestamp of evaluation.

  decision:
    type: string
    enum:
      - accept
      - reject
      - needs_review
      - rerun_required
      - candidate_promising
      - candidate_unsafe
    description: Evaluator decision for the candidate and run.

  score_breakdown:
    type: object
    description: Structured score components for the run.
    required:
      - overall_score
    properties:
      stability_score:
        type: number
      safety_score:
        type: number
      efficiency_score:
        type: number
      task_success_score:
        type: number
      overall_score:
        type: number

  risk_assessment:
    type: object
    description: Risk-oriented interpretation of simulation evidence.
    properties:
      risk_level:
        type: string
        enum:
          - low
          - medium
          - high
          - critical
      risk_tags:
        type: array
        items:
          type: string
      critical_issues:
        type: array
        items:
          type: string

  readiness:
    type: string
    enum:
      - simulation_only
      - ready_for_human_review
      - ready_for_limited_hardware_test
      - not_ready
    description: Readiness class derived from evaluation evidence.

  explanations:
    type: object
    description: Human-readable explanation package.
    properties:
      top_positive_factors:
        type: array
        items:
          type: string
      top_negative_factors:
        type: array
        items:
          type: string
      first_failure_reason:
        type: string
      dominant_constraint:
        type: string

  recommended_next_action:
    type: string
    enum:
      - promote_to_proposal
      - discard_candidate
      - run_more_seeds
      - tighten_constraints
      - test_on_hardware_sandbox
      - request_human_review
    description: Recommended next step in the engineering pipeline.

validation_rules:
  - overall_score must be present
  - if decision=accept then recommended_next_action must not be discard_candidate
  - if risk_level=critical then readiness must not be ready_for_limited_hardware_test
  - evaluator_id must be explicit

security_rules:
  - evaluator output is advisory only
  - evaluator cannot approve deployment
  - evaluator cannot modify core state
  - high-risk assessment must remain visible in downstream review
YAML

cat > proposal_package.v1.yaml <<'YAML'
contract_name: proposal_package
schema_version: proposal_package.v1
description: Upward-facing simulation proposal package carrying validated evidence into human review.

required:
  - proposal_id
  - created_at
  - origin
  - candidate_id
  - request_id
  - selected_runs
  - executive_summary
  - technical_summary
  - risk_summary
  - recommended_action
  - approval_requirements

fields:
  proposal_id:
    type: string
    description: Unique proposal identifier.

  created_at:
    type: string
    format: date-time
    description: UTC timestamp when proposal package was created.

  origin:
    type: string
    enum:
      - EVOLUTION_ENGINE
      - ROBOTICS_MODULE
      - SIMULATION_LAYER
    description: Originating subsystem that assembled this proposal package.

  candidate_id:
    type: string
    description: Candidate identifier promoted into proposal form.

  request_id:
    type: string
    description: Parent simulation request identifier.

  selected_runs:
    type: array
    items:
      type: string
    description: Run identifiers selected as evidence base for the proposal.

  executive_summary:
    type: object
    description: Human-facing high-level summary.
    required:
      - what_was_tested
      - best_result
      - why_selected
      - high_level_recommendation
    properties:
      what_was_tested:
        type: string
      best_result:
        type: string
      why_selected:
        type: string
      high_level_recommendation:
        type: string

  technical_summary:
    type: object
    description: Technical summary for engineering review.
    properties:
      environment:
        type: string
      controller_version:
        type: string
      constraint_status:
        type: string
      metrics_summary:
        type: object
        additional_properties: true
      comparison_with_baseline:
        type: string

  risk_summary:
    type: object
    description: Structured risk framing of the proposal.
    properties:
      known_risks:
        type: array
        items:
          type: string
      unknowns:
        type: array
        items:
          type: string
      hardware_risk:
        type: string
      safety_risk:
        type: string
      sim_to_real_risk:
        type: string

  recommended_action:
    type: string
    enum:
      - approve_hardware_sandbox_test
      - approve_limited_deployment
      - request_more_simulation
      - reject_candidate
    description: Recommended next action for human-controlled approval path.

  approval_requirements:
    type: object
    description: Required gates before any promotion beyond proposal.
    required:
      - human_review_required
      - hardware_key_required
      - voice_confirmation_required
    properties:
      human_review_required:
        type: boolean
      hardware_key_required:
        type: boolean
      voice_confirmation_required:
        type: boolean
      second_operator_required:
        type: boolean

  attachments:
    type: object
    description: Optional structured references to supporting artifacts.
    properties:
      simulation_report:
        type: string
      evaluator_result:
        type: string
      comparison_chart:
        type: string
      video:
        type: string
      failure_snapshot:
        type: string

validation_rules:
  - selected_runs must reference existing simulation_result entries
  - recommended_action must be compatible with risk_summary
  - proposal_package does not equal approval
  - approval_requirements must be present for every proposal
  - origin must be explicit

security_rules:
  - proposal is the only upward-facing simulation artifact
  - no direct deploy authority
  - human approval remains mandatory
  - no write to immutable core
YAML

cat > environment_contract.v1.yaml <<'YAML'
contract_name: environment_contract
schema_version: environment_contract.v1
description: Canonical backend-agnostic environment descriptor used by simulation layer.

required:
  - environment_id
  - scenario_type
  - model_type

fields:
  environment_id:
    type: string
    description: Unique environment identifier.

  scenario_type:
    type: string
    description: Scenario type implemented by this environment.

  model_type:
    type: string
    description: Abstract model class for the environment, such as control_benchmark or industrial_twin.

  required_inputs:
    type: array
    items:
      type: string
    description: Inputs required to instantiate or execute the environment.

  supported_metrics:
    type: array
    items:
      type: string
    description: Metrics natively supported by the environment.

  default_constraints:
    type: object
    additional_properties: true
    description: Default constraints applied unless overridden by request.

  default_stop_conditions:
    type: object
    additional_properties: true
    description: Default stop conditions applied unless overridden by request.

validation_rules:
  - environment_id required
  - scenario_type required
  - model_type required
  - environment contract must remain backend-agnostic

security_rules:
  - environment contract does not imply runtime authority
  - backend-specific leakage into core contract is forbidden
  - environment defaults must still respect governance and safety policies
YAML

cat > engine_registry.v1.yaml <<'YAML'
contract_name: engine_registry
schema_version: engine_registry.v1
description: Canonical registry of simulation backends and declared capabilities.

required:
  - default_engine
  - engines

fields:
  default_engine:
    type: string
    description: Default simulation backend identifier.

  engines:
    type: object
    additional_properties: true
    description: Mapping of engine identifiers to engine capability declarations.

validation_rules:
  - default_engine required
  - engines must not be empty
  - default_engine must exist inside engines registry
  - engine registry must remain backend metadata, not execution authority

security_rules:
  - registry does not grant backend execution rights by itself
  - disabled engines must not be selected automatically
  - backend capabilities must not override governance or sandbox policy
YAML

echo "simulation contracts restored successfully"
