#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/voice"

cat > stt_request.v1.yaml <<'YAML'
contract_name: stt_request
schema_version: stt_request.v1
description: Speech-to-text request contract.

required:
  - request_id
  - audio_ref
  - language

fields:
  request_id:
    type: string
    description: Unique STT request identifier.

  audio_ref:
    type: string
    description: Reference to input audio artifact or stream.

  language:
    type: string
    description: Expected language of the input audio.

  device_ref:
    type: string
    description: Reference to originating device or shell.

validation_rules:
  - request_id required
  - audio_ref required
  - language required
  - device_ref should be explicit for routed voice requests

security_rules:
  - audio handling follows privacy policy
  - request metadata does not imply execution authority
  - source device context must remain traceable
YAML

cat > stt_result.v1.yaml <<'YAML'
contract_name: stt_result
schema_version: stt_result.v1
description: Speech-to-text result.

required:
  - request_id
  - transcript

fields:
  request_id:
    type: string
    description: Reference to originating STT request.

  transcript:
    type: string
    description: Produced transcript text.

  confidence:
    type: number
    description: Confidence estimate for the produced transcript.

  language:
    type: string
    description: Detected or confirmed transcript language.

validation_rules:
  - request_id required
  - transcript required
  - confidence should be explicit when available
  - transcript must not be empty

security_rules:
  - transcript access follows privacy policy
  - STT result is evidence only
  - transcript output must not bypass downstream intent or approval layers
YAML

cat > tts_request.v1.yaml <<'YAML'
contract_name: tts_request
schema_version: tts_request.v1
description: Text-to-speech request.

required:
  - request_id
  - text
  - voice_profile

fields:
  request_id:
    type: string
    description: Unique TTS request identifier.

  text:
    type: string
    description: Text content to be synthesized.

  voice_profile:
    type: string
    description: Allowed voice profile or persona reference.

  target_device:
    type: string
    description: Target output device or shell reference.

validation_rules:
  - request_id required
  - text required
  - voice_profile required
  - target_device should be explicit for routed output

security_rules:
  - voice profile selection follows allowed personas
  - TTS request does not imply authority beyond output generation
  - sensitive output remains subject to privacy policy
YAML

cat > tts_result.v1.yaml <<'YAML'
contract_name: tts_result
schema_version: tts_result.v1
description: Text-to-speech result metadata.

required:
  - request_id
  - audio_ref

fields:
  request_id:
    type: string
    description: Reference to originating TTS request.

  audio_ref:
    type: string
    description: Reference to synthesized audio artifact.

  duration_sec:
    type: number
    description: Duration of generated audio in seconds.

validation_rules:
  - request_id required
  - audio_ref required
  - duration_sec should be explicit when known

security_rules:
  - audio output follows privacy policy
  - result metadata does not imply playback authority by itself
  - audio artifacts must remain traceable to request
YAML

cat > wake_event.v1.yaml <<'YAML'
contract_name: wake_event
schema_version: wake_event.v1
description: Wake phrase activation event.

required:
  - wake_event_id
  - detected_at
  - device_ref

fields:
  wake_event_id:
    type: string
    description: Unique wake event identifier.

  detected_at:
    type: string
    format: date-time
    description: UTC timestamp of wake phrase detection.

  device_ref:
    type: string
    description: Reference to device that detected the wake phrase.

  confidence:
    type: number
    description: Confidence score for wake phrase detection.

validation_rules:
  - wake_event_id required
  - detected_at required
  - device_ref required
  - confidence should be explicit when available

security_rules:
  - wake event alone grants no execution
  - wake detection remains subject to privacy and routing policy
  - false positive handling must remain possible downstream
YAML

cat > voice_routing.v1.yaml <<'YAML'
contract_name: voice_routing
schema_version: voice_routing.v1
description: Routing decision for voice handling across local, hybrid, or server-assisted modes.

required:
  - routing_id
  - mode
  - target_service

fields:
  routing_id:
    type: string
    description: Unique voice routing decision identifier.

  mode:
    type: string
    enum:
      - local
      - hybrid
      - server_assisted
    description: Voice routing mode selected for this request.

  target_service:
    type: string
    description: Target service or adapter selected to process the voice operation.

  policy_ref:
    type: string
    description: Reference to routing or privacy policy used for the decision.

validation_rules:
  - routing_id required
  - mode must match allowed enum
  - target_service required
  - policy_ref should be explicit for governed routing

security_rules:
  - routing respects privacy and trust policy
  - routing does not bypass shell or governance boundaries
  - server-assisted routing must remain policy-gated
YAML

echo "voice contracts restored successfully"
