from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "jarvis_live"
STATE_DIR = RUNTIME_ROOT / "state"
LOG_DIR = RUNTIME_ROOT / "logs"
AUDIO_SMOKE_DIR = RUNTIME_ROOT / "audio_smoke"
STATE_FILE = STATE_DIR / "jarvis_live_state.json"
HEARTBEAT_FILE = STATE_DIR / "jarvis_live_heartbeat.json"
PID_FILE = STATE_DIR / "jarvis_live.pid"
EVENT_LOG_FILE = LOG_DIR / "jarvis_live_events.jsonl"
VOICE_SAMPLE_CANDIDATES = (
    Path.home()
    / "MAKSIMAR_RUNTIME"
    / "voice_profiles"
    / "jarvis_ru_eugene_deep_01.wav",
    Path.home()
    / "MAKSIMAR_RUNTIME"
    / "speech_smoke"
    / "outputs"
    / "jarvis_ru_eugene_deep_01.wav",
)
OWNER_REPLY_TEXT = "Александр, я тебя слышу. JARVIS Live готов."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--oneshot-audio-smoke", action="store_true")
    args = parser.parse_args(argv)
    _ensure_runtime_dirs()
    if not args.oneshot_audio_smoke:
        PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    _write_state("starting", "background_loop_starting")

    if args.oneshot_audio_smoke:
        return _run_audio_smoke()

    try:
        _write_state("listening", "background_loop_active")
        while True:
            _write_heartbeat("listening")
            if os.environ.get("JARVIS_LIVE_ENABLE_AUDIO_SMOKE") == "1":
                _run_audio_smoke()
                os.environ["JARVIS_LIVE_ENABLE_AUDIO_SMOKE"] = "0"
            time.sleep(2)
    except KeyboardInterrupt:
        _write_state("stopped", "keyboard_interrupt")
        return 0
    except Exception as exc:
        _write_state("error", f"{type(exc).__name__}: {exc}")
        return 1


def _run_audio_smoke() -> int:
    seconds = _audio_seconds()
    _write_heartbeat("audio_smoke")
    if shutil.which("parec") is None:
        _write_state("error", "parec_missing")
        return 2
    AUDIO_SMOKE_DIR.mkdir(parents=True, exist_ok=True)
    audio_path = AUDIO_SMOKE_DIR / "rdpsource_smoke.wav"
    recorder = subprocess.Popen(  # noqa: S603 - allowed local audio smoke command.
        [
            "parec",
            "--device=RDPSource",
            "--file-format=wav",
            str(audio_path),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(seconds)
    recorder.terminate()
    try:
        recorder.wait(timeout=3)
    except subprocess.TimeoutExpired:
        recorder.kill()
        recorder.wait(timeout=3)
    transcript = _transcribe_audio(audio_path)
    owner_detected = _owner_detected(transcript)
    reply = OWNER_REPLY_TEXT if owner_detected else ""
    _write_state(
        "listening",
        "audio_smoke_complete",
        latest_transcript=transcript,
        latest_voice_reply=reply,
        owner_detected=owner_detected,
    )
    if owner_detected:
        _play_voice_sample_if_available()
    return 0


def _transcribe_audio(audio_path: Path) -> str:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return ""
    model_root = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_models" / "faster_whisper"
    model = WhisperModel(
        "medium",
        device="cpu",
        compute_type="int8",
        download_root=str(model_root),
    )
    segments, _info = model.transcribe(str(audio_path), language="ru")
    text = " ".join(segment.text.strip() for segment in segments if segment.text.strip())
    return text.strip()


def _play_voice_sample_if_available() -> None:
    if shutil.which("paplay") is None:
        return
    for sample_path in VOICE_SAMPLE_CANDIDATES:
        if sample_path.exists():
            subprocess.run(  # noqa: S603 - allowed local playback command.
                ["paplay", str(sample_path)],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return


def _owner_detected(transcript: str) -> bool:
    lowered = transcript.casefold()
    return "александр" in lowered or "джарвис" in lowered


def _audio_seconds() -> int:
    raw_value = os.environ.get("JARVIS_LIVE_AUDIO_SECONDS", "6")
    if not raw_value.isdigit():
        return 6
    return max(1, min(int(raw_value), 30))


def _ensure_runtime_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_SMOKE_DIR.mkdir(parents=True, exist_ok=True)


def _write_heartbeat(state: str) -> None:
    payload = {
        "state": state,
        "pid": os.getpid(),
        "updated_at": time.time(),
        "pc_control_allowed": False,
    }
    HEARTBEAT_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2),
        encoding="utf-8",
    )


def _write_state(
    state: str,
    reason: str,
    latest_transcript: str = "",
    latest_voice_reply: str = "",
    owner_detected: bool = False,
) -> None:
    payload = {
        "state": state,
        "pid": os.getpid(),
        "reason": reason,
        "updated_at": time.time(),
        "voice_loop_enabled": state in {"starting", "listening"},
        "pc_control_allowed": False,
        "latest_transcript": latest_transcript,
        "latest_voice_reply": latest_voice_reply,
        "owner_detected": owner_detected,
    }
    STATE_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2),
        encoding="utf-8",
    )
    _append_event({"event": "state", "state": state, "reason": reason})


def _append_event(payload: dict[str, Any]) -> None:
    payload = {"updated_at": time.time(), **payload, "pc_control_allowed": False}
    with EVENT_LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
