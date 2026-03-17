#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/VISUAL_ENGINEERING_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > image_ingest.yaml <<'YAML'
schema_version: visual_image_ingest_config.v1
description: Canonical ingest policy for images and visual source assets.

sources:
  file_enabled: true
  camera_enabled: true
  screenshot_enabled: true
  imported_dataset_enabled: true

validation:
  source_ref_required: true
  source_type_required: true
  provenance_required_for_dataset_imports: true
  normalize_metadata_on_ingest: true

rules:
  - all visual inputs must preserve provenance
  - dataset imports must not become trusted examples without review
  - ingest does not imply transformation authority
YAML

cat > image_editing.yaml <<'YAML'
schema_version: visual_image_editing_config.v1
description: Canonical transformation and editing policy for visual engineering workflows.

transforms:
  cleanup_enabled: true
  crop_enabled: true
  threshold_enabled: true
  vectorize_enabled: true
  background_remove_enabled: true
  machine_prepare_enabled: true
  image_to_depth_enabled: true
  image_to_model_hint_enabled: true

validation:
  output_snapshot_required_for_destructive_edits: true
  parameters_must_be_explicit: true
  transform_trace_required: true

rules:
  - destructive visual edits must remain auditable
  - every transformation must preserve input-output traceability
  - editing does not imply downstream manufacturing approval
YAML

cat > machine_asset_export.yaml <<'YAML'
schema_version: visual_machine_asset_export_config.v1
description: Canonical export policy for machine-ready visual assets.

targets:
  laser_enabled: true
  cnc_enabled: true
  print_enabled: true
  vinyl_enabled: true

validation:
  target_machine_type_required: true
  export_format_required: true
  machine_readiness_check_required: true
  approval_required_before_machine_use: true

rules:
  - machine-ready export is not machine-start authority
  - outputs must remain target-specific and validated
  - unsafe outputs must remain blocked
YAML

cat > image_to_3d.yaml <<'YAML'
schema_version: visual_image_to_3d_config.v1
description: Canonical policy for image-derived 3D preparation.

conversion:
  image_to_depth_enabled: true
  image_to_model_hint_enabled: true
  confidence_required: true
  output_geometry_validation_required: true

promotion:
  unvalidated_geometry_blocked_for_manufacturing: true
  simulation_recommended_before_hardware_path: true

rules:
  - image-derived geometry requires downstream validation
  - confidence must remain explicit
  - conversion output is proposal/evidence, not manufacturing authority
YAML

cat > visual_training_policy.yaml <<'YAML'
schema_version: visual_training_policy.v1
description: Canonical policy for learning from approved visual examples.

training_examples:
  approved_examples_only: true
  unreviewed_dataset_forbidden_for_trusted_learning: true
  provenance_required: true
  label_required: true

safety:
  restricted_examples_require_policy: true
  export_of_training_examples_policy_gated: true

rules:
  - learning must use approved examples only for trusted paths
  - provenance of training examples must remain visible
  - training policy must not bypass review and approval layers
YAML

cat > visual_eval_policy.yaml <<'YAML'
schema_version: visual_eval_policy.v1
description: Canonical evaluation policy for visual outputs and machine-ready assets.

evaluation:
  artifact_quality_check_required: true
  machine_readiness_check_required: true
  confidence_reporting_required: true
  reviewer_notes_recommended: true

thresholds:
  minimum_quality_score_for_promotion: 0.80
  minimum_machine_readiness_for_export: 0.85
  hard_block_on_critical_visual_failure: true

rules:
  - weak visual outputs must not silently promote downstream
  - evaluation must remain attached to visual artifacts
  - approval remains separate from evaluation
YAML

echo "visual_engineering configs filled successfully"
