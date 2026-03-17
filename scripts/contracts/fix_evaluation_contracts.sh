#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/evaluation"

cat > benchmark_case.v1.yaml <<'YAML'
contract_name: benchmark_case
schema_version: benchmark_case.v1
description: Canonical benchmark test case.

required:
  - case_id
  - domain
  - prompt_or_input
  - expected_behavior

fields:
  case_id:
    type: string
    description: Unique benchmark case identifier.

  domain:
    type: string
    description: Evaluation domain this case belongs to.

  prompt_or_input:
    type: object
    additional_properties: true
    description: Structured prompt, request, or input payload used by the benchmark.

  expected_behavior:
    type: string
    description: Expected outcome or rubric-aligned target behavior.

  grading_policy_ref:
    type: string
    description: Reference to grading policy or rubric used for scoring.

validation_rules:
  - case_id required
  - domain required
  - expected_behavior required
  - prompt_or_input must be explicit

security_rules:
  - benchmark input may include restricted fixtures only under policy
  - benchmark case does not grant execution authority
  - grading policy reference must remain explicit
YAML

cat > benchmark_result.v1.yaml <<'YAML'
contract_name: benchmark_result
schema_version: benchmark_result.v1
description: Benchmark execution result.

required:
  - result_id
  - case_id
  - status
  - score

fields:
  result_id:
    type: string
    description: Unique benchmark result identifier.

  case_id:
    type: string
    description: Reference to benchmark case that produced this result.

  status:
    type: string
    enum:
      - pass
      - fail
      - partial
    description: Final benchmark status.

  score:
    type: number
    description: Numeric score assigned to the result.

  notes:
    type: string
    description: Optional human-readable notes for the result.

validation_rules:
  - result_id required
  - case_id required
  - status must match allowed enum
  - score must be explicit

security_rules:
  - result is evidence only
  - result must not imply deployment authority
  - benchmark outputs must preserve evaluation traceability
YAML

cat > turing_style_eval.v1.yaml <<'YAML'
contract_name: turing_style_eval
schema_version: turing_style_eval.v1
description: Human-likeness conversational evaluation signal.

required:
  - eval_id
  - dialogue_ref
  - score

fields:
  eval_id:
    type: string
    description: Unique Turing-style evaluation identifier.

  dialogue_ref:
    type: string
    description: Reference to dialogue session or transcript under evaluation.

  score:
    type: number
    description: Human-likeness score assigned by rubric, human, or model judge.

  evaluator_type:
    type: string
    enum:
      - human
      - rubric
      - model
    description: Type of evaluator that produced the score.

  notes:
    type: string
    description: Optional evaluator notes.

validation_rules:
  - eval_id required
  - dialogue_ref required
  - evaluator_type must match allowed enum
  - turing-style eval is one signal only

security_rules:
  - cannot be sole deployment gate
  - conversational realism must not override safety evaluation
  - turing-style result is advisory only
YAML

cat > workflow_eval.v1.yaml <<'YAML'
contract_name: workflow_eval
schema_version: workflow_eval.v1
description: Evaluation of workflow correctness and safety.

required:
  - eval_id
  - workflow_id
  - correctness_score

fields:
  eval_id:
    type: string
    description: Unique workflow evaluation identifier.

  workflow_id:
    type: string
    description: Reference to evaluated workflow.

  correctness_score:
    type: number
    description: Score describing whether workflow behavior matches intended logic.

  safety_score:
    type: number
    description: Score describing workflow safety and policy compliance.

  policy_violations:
    type: array
    items:
      type: string
    description: Explicit list of policy violations detected during workflow evaluation.

validation_rules:
  - eval_id required
  - workflow_id required
  - correctness_score must be explicit
  - policy_violations should be explicit even when empty

security_rules:
  - policy violations block promotion
  - workflow evaluation does not grant execution authority
  - safety score must not be omitted in high-risk workflows
YAML

cat > tool_use_eval.v1.yaml <<'YAML'
contract_name: tool_use_eval
schema_version: tool_use_eval.v1
description: Evaluation of tool calling and action selection behavior.

required:
  - eval_id
  - tool_path_ref
  - score

fields:
  eval_id:
    type: string
    description: Unique tool-use evaluation identifier.

  tool_path_ref:
    type: string
    description: Reference to evaluated tool invocation path or execution trace.

  score:
    type: number
    description: Aggregate tool-use quality score.

  misuse_events:
    type: array
    items:
      type: string
    description: Explicit list of tool misuse or unsafe selection events.

validation_rules:
  - eval_id required
  - tool_path_ref required
  - score must be explicit
  - misuse_events should be explicit even when empty

security_rules:
  - unsafe tool use must be flagged
  - tool-use evaluation is evidence only
  - dangerous misuse events must remain visible in downstream review
YAML

cat > knowledge_eval.v1.yaml <<'YAML'
contract_name: knowledge_eval
schema_version: knowledge_eval.v1
description: Evaluation of retrieval quality, grounding, and citation fidelity.

required:
  - eval_id
  - retrieval_ref
  - grounding_score

fields:
  eval_id:
    type: string
    description: Unique knowledge evaluation identifier.

  retrieval_ref:
    type: string
    description: Reference to evaluated retrieval result or query trace.

  grounding_score:
    type: number
    description: Score for groundedness against approved sources.

  citation_fidelity_score:
    type: number
    description: Score for correctness and fidelity of citation use.

  hallucination_detected:
    type: boolean
    description: Whether unsupported or hallucinated content was detected.

validation_rules:
  - eval_id required
  - retrieval_ref required
  - grounding_score must be explicit
  - hallucination_detected must be explicit

security_rules:
  - hallucination flag must be preserved
  - knowledge eval does not authorize promotion by itself
  - poor grounding must block unsafe downstream automation where policy applies
YAML

cat > codegen_eval.v1.yaml <<'YAML'
contract_name: codegen_eval
schema_version: codegen_eval.v1
description: Evaluation of generated code quality.

required:
  - eval_id
  - spec_ref
  - diff_ref
  - score

fields:
  eval_id:
    type: string
    description: Unique code generation evaluation identifier.

  spec_ref:
    type: string
    description: Reference to source specification used for generation.

  diff_ref:
    type: string
    description: Reference to generated diff package under evaluation.

  score:
    type: number
    description: Aggregate code quality score.

  test_status:
    type: string
    description: Structured summary of test outcome.

  lint_status:
    type: string
    description: Structured summary of lint outcome.

  typecheck_status:
    type: string
    description: Structured summary of typecheck outcome.

validation_rules:
  - eval_id required
  - spec_ref required
  - diff_ref required
  - score must be explicit

security_rules:
  - failing eval blocks proposal promotion
  - codegen eval is evidence only
  - evaluation results must not bypass review and approval flow
YAML

echo "evaluation contracts restored successfully"
