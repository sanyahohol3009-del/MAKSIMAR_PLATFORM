#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/visual_engineering"

cat > image_ingest.v1.yaml <<'YAML'
contract_name: image_ingest
schema_version: image_ingest.v1
description: Canonical image ingest request.

required:
  - image_id
  - source_type
  - source_ref

fields:
  image_id:
    type: string
    description: Unique ingested image identifier.

  source_type:
    type: string
    enum:
      - file
      - camera
      - screenshot
      - imported_dataset
    description: Origin type of the image asset.

  source_ref:
    type: string
    description: Reference to the source file, stream, or dataset artifact.

  tags:
    type: array
    items:
      type: string
    description: Semantic tags attached to the ingested image.

validation_rules:
  - image_id required
  - source_type must match allowed enum
  - source_ref required
  - tags should be explicit even when empty

security_rules:
  - imported datasets follow provenance policy
  - ingest metadata does not imply transform authority
  - source traceability must be preserved
YAML

cat > image_transform.v1.yaml <<'YAML'
contract_name: image_transform
schema_version: image_transform.v1
description: Canonical visual transformation request.

required:
  - transform_id
  - input_image_ref
  - transform_type

fields:
  transform_id:
    type: string
    description: Unique transform request identifier.

  input_image_ref:
    type: string
    description: Reference to input image asset.

  transform_type:
    type: string
    enum:
      - cleanup
      - crop
      - threshold
      - vectorize
      - background_remove
      - machine_prepare
      - image_to_depth
      - image_to_model_hint
    description: Requested transformation class.

  parameters:
    type: object
    additional_properties: true
    description: Structured transform parameters.

validation_rules:
  - transform_id required
  - input_image_ref required
  - transform_type must match allowed enum
  - transform parameters should be explicit for non-default processing

security_rules:
  - destructive transforms require output snapshot
  - transform request does not imply production use authority
  - input and output lineage must remain reviewable
YAML

cat > machine_ready_asset.v1.yaml <<'YAML'
contract_name: machine_ready_asset
schema_version: machine_ready_asset.v1
description: Prepared asset for machine workflow.

required:
  - asset_id
  - source_image_ref
  - target_machine_type

fields:
  asset_id:
    type: string
    description: Unique machine-ready asset identifier.

  source_image_ref:
    type: string
    description: Reference to source image asset.

  target_machine_type:
    type: string
    enum:
      - laser
      - cnc
      - print
      - vinyl
    description: Target machine class for prepared output.

  export_format:
    type: string
    description: Output format used by the machine-ready asset.

  validation_status:
    type: string
    description: Validation state of the asset for downstream use.

validation_rules:
  - asset_id required
  - source_image_ref required
  - target_machine_type must match allowed enum
  - export_format should be explicit
  - validation_status required for downstream machine-facing artifacts

security_rules:
  - machine-ready does not imply machine-start authority
  - output must remain subject to visual approval policy
  - asset lineage must remain traceable to source image
YAML

cat > image_to_3d.v1.yaml <<'YAML'
contract_name: image_to_3d
schema_version: image_to_3d.v1
description: Request and result contract for image-derived 3D preparation.

required:
  - conversion_id
  - input_image_ref

fields:
  conversion_id:
    type: string
    description: Unique image-to-3D conversion identifier.

  input_image_ref:
    type: string
    description: Reference to source image asset.

  target_geometry_type:
    type: string
    description: Requested target geometry class.

  output_geometry_ref:
    type: string
    description: Reference to generated geometry artifact.

  confidence:
    type: number
    description: Confidence estimate of the generated result.

validation_rules:
  - conversion_id required
  - input_image_ref required
  - confidence should be explicit when output is generated
  - output_geometry_ref should exist for completed conversion records

security_rules:
  - output requires validation before manufacturing
  - conversion output does not imply geometry approval
  - generated geometry must remain linked to source image lineage
YAML

cat > visual_eval.v1.yaml <<'YAML'
contract_name: visual_eval
schema_version: visual_eval.v1
description: Evaluation of visual transform or prepared asset.

required:
  - eval_id
  - target_ref
  - score

fields:
  eval_id:
    type: string
    description: Unique visual evaluation identifier.

  target_ref:
    type: string
    description: Reference to evaluated transform output or machine-ready asset.

  score:
    type: number
    description: Aggregate evaluation score.

  artifact_quality:
    type: string
    description: Human-readable quality classification.

  machine_readiness:
    type: string
    description: Human-readable machine readiness classification.

  notes:
    type: string
    description: Additional evaluation notes.

validation_rules:
  - eval_id required
  - target_ref required
  - score must be explicit
  - machine_readiness should be explicit for machine-facing outputs

security_rules:
  - poor eval blocks downstream proposal promotion where policy applies
  - evaluation is evidence only
  - unsafe outputs must remain visibly flagged
YAML

cat > visual_approval.v1.yaml <<'YAML'
contract_name: visual_approval
schema_version: visual_approval.v1
description: Approval contract for visual outputs going to machine or product use.

required:
  - approval_id
  - target_ref
  - decision

fields:
  approval_id:
    type: string
    description: Unique visual approval identifier.

  target_ref:
    type: string
    description: Reference to visual artifact under review.

  decision:
    type: string
    enum:
      - approved
      - rejected
      - needs_review
    description: Approval decision.

  reviewer:
    type: string
    description: Reviewer or operator responsible for the decision.

  rationale:
    type: string
    description: Human-readable explanation for the decision.

validation_rules:
  - approval_id required
  - target_ref required
  - decision must match allowed enum
  - reviewer should be explicit for approved outputs

security_rules:
  - approval required before hardware or production use
  - approval does not bypass machine-specific safeguards
  - rejected or needs_review outputs must remain blocked downstream
YAML

echo "visual_engineering contracts restored successfully"
