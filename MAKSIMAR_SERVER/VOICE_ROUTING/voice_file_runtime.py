"""Real, bounded Voice Organ file pipeline.

Audio plumbing only: the supplied callable is the existing canonical Semantic
Spine; this module performs no intent or operation routing.
"""
from __future__ import annotations
import hashlib, json, os, subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME"
STT_PYTHON = RUNTIME_ROOT / "venvs/faster_whisper_stt/bin/python"
VOICE_PYTHON = RUNTIME_ROOT / "venvs/silero_tts/bin/python"
STT_MODEL_ROOT = RUNTIME_ROOT / "runtime_models/faster_whisper"
VAD_HUB_ROOT = RUNTIME_ROOT / "voice_models/silero/torch_hub"
OUTPUT_ROOT = RUNTIME_ROOT / "jarvis_live/voice_outputs"

@dataclass(frozen=True, slots=True)
class VoiceInputResult:
    status: str
    audio_path: str
    duration_seconds: float
    speech_segments: tuple[dict[str, int], ...]
    transcript: str
    stt_provider: str
    content_sha256: str
    evidence: dict[str, Any]

@dataclass(frozen=True, slots=True)
class VoiceOutputResult:
    status: str
    audio_path: str
    duration_seconds: float
    tts_provider: str
    evidence: dict[str, Any]

def _run_json(python: Path, source: str, *, timeout: float) -> dict[str, Any]:
    completed = subprocess.run([str(python), "-c", source], check=False,
                               capture_output=True, text=True, timeout=timeout,
                               env={**os.environ, "PYTHONUNBUFFERED": "1"})
    if completed.returncode:
        raise RuntimeError(completed.stderr[-2000:] or "voice_runtime_failed")
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError("voice_runtime_empty_result")
    return json.loads(lines[-1])

def detect_speech(audio_path: str | Path) -> tuple[float, tuple[dict[str, int], ...]]:
    path = str(Path(audio_path).resolve())
    source = f'''from pathlib import Path
import json, torch, soundfile as sf
from torchaudio.functional import resample
torch.hub.set_dir({str(VAD_HUB_ROOT)!r})
model, utils = torch.hub.load("snakers4/silero-vad", "silero_vad", trust_repo=True)
get_speech_timestamps = utils[0]
a, sr = sf.read({path!r}, dtype="float32")
if getattr(a, "ndim", 1) > 1: a = a.mean(axis=1)
if int(sr) != 16000:
    a = resample(torch.from_numpy(a), int(sr), 16000).numpy()
    sr = 16000
audio = torch.from_numpy(a)
segments = get_speech_timestamps(audio, model, sampling_rate=int(sr))
print(json.dumps({{"duration_seconds": len(audio)/int(sr), "segments": segments}}))'''
    result = _run_json(VOICE_PYTHON, source, timeout=120)
    return float(result["duration_seconds"]), tuple(dict(x) for x in result["segments"])

def transcribe(audio_path: str | Path, *, model: str = "small") -> str:
    path = str(Path(audio_path).resolve())
    source = f'''import json
from faster_whisper import WhisperModel
m = WhisperModel({model!r}, device="cpu", compute_type="int8", download_root={str(STT_MODEL_ROOT)!r})
segments, info = m.transcribe({path!r}, language=None, beam_size=5, vad_filter=True)
text = " ".join(s.text.strip() for s in segments).strip()
print(json.dumps({{"text": text, "language": info.language, "probability": info.language_probability}}, ensure_ascii=False))'''
    return str(_run_json(STT_PYTHON, source, timeout=240).get("text", "")).strip()

def synthesize(text: str, *, output_path: str | Path | None = None) -> VoiceOutputResult:
    if not text.strip():
        raise ValueError("tts_text_must_not_be_empty")
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    path = Path(output_path) if output_path else OUTPUT_ROOT / "voice_reply.wav"
    source = f'''from pathlib import Path
import json, torch, soundfile as sf
torch.hub.set_dir({str(VAD_HUB_ROOT)!r})
model, _ = torch.hub.load(repo_or_dir="snakers4/silero-models", model="silero_tts", language="ru", speaker="v4_ru", trust_repo=True)
audio = model.apply_tts(text={text!r}, speaker="eugene", sample_rate=48000, put_accent=True, put_yo=True)
sf.write({str(path)!r}, audio, 48000)
print(json.dumps({{"duration_seconds": len(audio)/48000}}))'''
    result = _run_json(VOICE_PYTHON, source, timeout=180)
    duration = float(result["duration_seconds"])
    if duration <= 0 or not path.exists() or path.stat().st_size <= 44:
        raise RuntimeError("tts_artifact_invalid")
    return VoiceOutputResult("COMPLETE", str(path), duration, "silero_tts",
                             {"kind": "voice_synthesis", "provider": "silero_tts",
                              "duration_seconds": duration})

def run_voice_file_e2e(audio_path: str | Path, semantic_turn: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    path = Path(audio_path).resolve()
    if not path.exists():
        raise FileNotFoundError(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    duration, segments = detect_speech(path)
    base = {"audio_path": str(path), "duration_seconds": duration}
    if not segments:
        return {"status": "NO_SPEECH", "input": base}
    transcript = transcribe(path)
    if not transcript:
        return {"status": "TRANSCRIPTION_UNAVAILABLE", "input": base}
    inp = VoiceInputResult("COMPLETE", str(path), duration, segments, transcript,
                           "faster_whisper_small", digest,
                           {"kind": "voice_transcript", "audio_path": str(path),
                            "duration_seconds": duration, "speech_segments": segments,
                            "speech_segment_sample_rate": 16000,
                            "transcript": transcript, "stt_provider": "faster_whisper_small",
                            "content_sha256": digest})
    semantic = semantic_turn(transcript)
    answer = str(semantic.get("response_text", "")).strip()
    output = synthesize(answer) if answer else None
    semantic_complete = semantic.get("operation_status") == "COMPLETE"
    return {"status": "COMPLETE" if semantic_complete and output else "PARTIAL", "input": inp, "semantic": semantic, "output": output,
            "voice_evidence": {"input": inp.evidence,
                               "output": output.evidence if output else {"status": "UNAVAILABLE"}}}
