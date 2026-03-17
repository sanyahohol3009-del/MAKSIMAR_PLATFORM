#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/VOICE_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > voice_policy.yaml <<'YAML'
schema_version: voice_policy.v1
description: Canonical top-level policy for voice interaction layer.

voice:
  wake_word_enabled: true
  continuous_listening_optional: true
  voice_session_tracking_required: true
  multi_language_support_allowed: true

safety:
  voice_execution_authority_forbidden: true
  approval_required_for_sensitive_commands: true
  voice_identity_verification_supported: true

rules:
  - voice layer converts speech to intent only
  - voice must not execute actions directly
  - sensitive commands must remain approval-gated
YAML


cat > voice_identity_policy.yaml <<'YAML'
schema_version: voice_identity_policy.v1
description: Canonical policy for voice identity and speaker verification.

identity:
  speaker_verification_supported: true
  enrollment_required_for_trusted_identity: true
  multi_user_supported: true

validation:
  confidence_required: true
  identity_reference_required: true
  fallback_to_untrusted_mode_when_uncertain: true

rules:
  - voice identity must remain probabilistic and explicit
  - low-confidence identity must not gain privileged authority
  - identity checks must remain auditable
YAML


cat > voice_command_policy.yaml <<'YAML'
schema_version: voice_command_policy.v1
description: Canonical policy for voice command parsing and routing.

commands:
  intent_mapping_required: true
  workflow_binding_allowed: true
  direct_action_binding_forbidden: true

validation:
  command_trace_required: true
  context_reference_required: true
  ambiguous_command_requires_clarification: true

rules:
  - voice commands must resolve to intents, not direct execution
  - command routing must remain auditable
  - ambiguous commands must trigger clarification
YAML


echo "voice configs filled successfully"
