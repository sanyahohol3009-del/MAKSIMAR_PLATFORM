from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any


RUNTIME_ROOT = Path(
    os.environ.get("JARVIS_LIVE_RUNTIME_ROOT", str(Path.home() / "MAKSIMAR_RUNTIME" / "jarvis_live"))
).expanduser()
STATE_DIR = RUNTIME_ROOT / "state"
LOG_DIR = RUNTIME_ROOT / "logs"
STATE_FILE = STATE_DIR / "jarvis_live_state.json"
HEARTBEAT_FILE = STATE_DIR / "jarvis_live_heartbeat.json"
PID_FILE = STATE_DIR / "jarvis_live.pid"
BACKGROUND_STDOUT_LOG = LOG_DIR / "background_loop.stdout.log"
BACKGROUND_STDERR_LOG = LOG_DIR / "background_loop.stderr.log"


def main() -> int:
    status = build_status()
    print("JARVIS_LIVE_RUNTIME_STATUS")
    print(f"supervisor_running={str(status['supervisor_running']).lower()}")
    print(f"runtime_alive={str(status['runtime_alive']).lower()}")
    print(f"runtime_dead_reason={status['runtime_dead_reason']}")
    print(f"latest_state_is_stale={str(status['latest_state_is_stale']).lower()}")
    print(f"state_truth_source={status['state_truth_source']}")
    print(f"pid={status['pid']}")
    print(f"background_pid={status['background_pid']}")
    print(f"background_runtime_alive={str(status['background_runtime_alive']).lower()}")
    print(f"runtime_python={status['runtime_python']}")
    print(f"heartbeat_age_seconds={status['heartbeat_age_seconds']}")
    print(f"voice_loop_enabled={str(status['voice_loop_enabled']).lower()}")
    print(f"voice_loop_enabled_state={str(status['voice_loop_enabled_state']).lower()}")
    print(f"always_listening_enabled={str(status['always_listening_enabled']).lower()}")
    print(f"always_listening_enabled_state={str(status['always_listening_enabled_state']).lower()}")
    print(f"passive_listening={str(status['passive_listening']).lower()}")
    print(f"listening_suppressed={str(status['listening_suppressed']).lower()}")
    print(f"suppress_reason={status['suppress_reason']}")
    print(f"post_tts_suppress_ms={status['post_tts_suppress_ms']}")
    print(f"last_tts_playback_ended_at={status['last_tts_playback_ended_at']}")
    print(f"assistant_awake={str(status['assistant_awake']).lower()}")
    print(f"wake_word_detected={str(status['wake_word_detected']).lower()}")
    print(f"wake_word={status['wake_word']}")
    print(f"wake_phrase={status['wake_phrase']}")
    print(f"command_text={status['command_text']}")
    print(f"passive_ignore_reason={status['passive_ignore_reason']}")
    print(f"wake_gate_mode={status['wake_gate_mode']}")
    print(f"owner_voice_verified={str(status['owner_voice_verified']).lower()}")
    print(f"owner_voice_verification_mode={status['owner_voice_verification_mode']}")
    print(f"owner_voice_required={str(status['owner_voice_required']).lower()}")
    print(f"owner_detected={str(status['owner_detected']).lower()}")
    print(f"screen_observer_enabled={str(status['screen_observer_enabled']).lower()}")
    print(f"screen_read_only={str(status['screen_read_only']).lower()}")
    print("pc_control_allowed=false")
    print(f"latest_transcript={status['latest_transcript']}")
    print(f"latest_voice_reply={status['latest_voice_reply']}")
    print(f"audio_input_path={status['audio_input_path']}")
    print(f"audio_input_size_bytes={status['audio_input_size_bytes']}")
    print(f"audio_duration_seconds={status['audio_duration_seconds']}")
    print(f"rms_peak={status['rms_peak']}")
    print(f"rms_avg={status['rms_avg']}")
    print(f"speech_duration_ms={status['speech_duration_ms']}")
    print(f"vad_reason={status['vad_reason']}")
    print(f"stt_model_used={status['stt_model_used']}")
    print(f"stt_model_cached={str(status['stt_model_cached']).lower()}")
    print(f"stt_model_cache_key={status['stt_model_cache_key']}")
    print(f"language={status['language']}")
    print(f"stt_done={str(status['stt_done']).lower()}")
    print(f"stt_reason={status['stt_reason']}")
    print(f"response_inflight={str(status['response_inflight']).lower()}")
    print(f"duplicate_suppressed={str(status['duplicate_suppressed']).lower()}")
    print(f"last_processed_transcript={status['last_processed_transcript']}")
    print(f"last_processed_at={status['last_processed_at']}")
    print(f"response_mode={status['response_mode']}")
    print(f"ollama_num_predict={status['ollama_num_predict']}")
    print(f"ollama_temperature={status['ollama_temperature']}")
    print(f"ollama_model_used={status['ollama_model_used']}")
    print(f"fast_path_used={str(status['fast_path_used']).lower()}")
    print(f"fast_path_reason={status['fast_path_reason']}")
    print(f"llm_response={status['llm_response']}")
    print(f"tts_engine={status['tts_engine']}")
    print(f"tts_voice={status['tts_voice']}")
    print(f"tts_done={str(status['tts_done']).lower()}")
    print(f"tts_reason={status['tts_reason']}")
    print(f"tts_cache_hit={str(status['tts_cache_hit']).lower()}")
    print(f"tts_cache_path={status['tts_cache_path']}")
    print(f"tts_cache_prewarmed={str(status['tts_cache_prewarmed']).lower()}")
    print(f"tts_model_cached={str(status['tts_model_cached']).lower()}")
    print(f"tts_error_class={status['tts_error_class']}")
    print(f"tts_error_message={status['tts_error_message']}")
    print(
        "voice_playback_attempted="
        f"{str(status['voice_playback_attempted']).lower()}"
    )
    print(f"voice_playback_done={str(status['voice_playback_done']).lower()}")
    print(f"voice_playback_reason={status['voice_playback_reason']}")
    print(f"playback_pid={status['playback_pid']}")
    print(f"playback_interrupted={str(status['playback_interrupted']).lower()}")
    print(f"playback_interrupt_reason={status['playback_interrupt_reason']}")
    print(f"barge_in_detected={str(status['barge_in_detected']).lower()}")
    print(f"response_cancelled={str(status['response_cancelled']).lower()}")
    print(f"audio_output_path={status['audio_output_path']}")
    print(f"vad_elapsed_seconds={status['vad_elapsed_seconds']}")
    print(f"stt_elapsed_seconds={status['stt_elapsed_seconds']}")
    print(f"wake_gate_elapsed_seconds={status['wake_gate_elapsed_seconds']}")
    print(f"fast_path_elapsed_seconds={status['fast_path_elapsed_seconds']}")
    print(f"ollama_elapsed_seconds={status['ollama_elapsed_seconds']}")
    print(f"tts_elapsed_seconds={status['tts_elapsed_seconds']}")
    print(f"playback_elapsed_seconds={status['playback_elapsed_seconds']}")
    print(f"total_turn_elapsed_seconds={status['total_turn_elapsed_seconds']}")
    print(f"latency_profile={status['latency_profile']}")
    print(f"latest_screen_frame={status['latest_screen_frame']}")
    print(f"latest_screen_summary={status['latest_screen_summary']}")
    print(f"background_stdout_log={status['background_stdout_log']}")
    print(f"background_stderr_log={status['background_stderr_log']}")
    return 0


def build_status() -> dict[str, Any]:
    state = _read_json(STATE_FILE)
    heartbeat = _read_json(HEARTBEAT_FILE)
    pid = _read_pid()
    heartbeat_updated_at = heartbeat.get("updated_at")
    heartbeat_age = None
    if isinstance(heartbeat_updated_at, int | float):
        heartbeat_age = round(time.time() - float(heartbeat_updated_at), 3)
    supervisor_running = pid is not None and _process_alive(pid)
    runtime_dead_reason = _runtime_dead_reason(pid, supervisor_running, heartbeat_age)
    runtime_alive = supervisor_running and runtime_dead_reason == "ok"
    latest_state_is_stale = not runtime_alive
    voice_loop_enabled_state = bool(state.get("voice_loop_enabled", False))
    always_listening_enabled_state = bool(state.get("always_listening_enabled", False))
    return {
        "supervisor_running": supervisor_running,
        "runtime_alive": runtime_alive,
        "runtime_dead_reason": runtime_dead_reason,
        "latest_state_is_stale": latest_state_is_stale,
        "state_truth_source": "current_turn" if runtime_alive else "stale_state",
        "pid": pid or "",
        "background_pid": pid or "",
        "background_runtime_alive": runtime_alive,
        "runtime_python": str(state.get("runtime_python", "")),
        "heartbeat_age_seconds": heartbeat_age if heartbeat_age is not None else "",
        "voice_loop_enabled": voice_loop_enabled_state and runtime_alive,
        "voice_loop_enabled_state": voice_loop_enabled_state,
        "always_listening_enabled": always_listening_enabled_state and runtime_alive,
        "always_listening_enabled_state": always_listening_enabled_state,
        "passive_listening": bool(state.get("passive_listening", False)),
        "listening_suppressed": bool(state.get("listening_suppressed", False)),
        "suppress_reason": str(state.get("suppress_reason", "")),
        "post_tts_suppress_ms": int(state.get("post_tts_suppress_ms", 1200) or 1200),
        "last_tts_playback_ended_at": float(
            state.get("last_tts_playback_ended_at", 0.0) or 0.0
        ),
        "assistant_awake": bool(state.get("assistant_awake", False)),
        "wake_word_detected": bool(state.get("wake_word_detected", False)),
        "wake_word": str(state.get("wake_word", "")),
        "wake_phrase": str(state.get("wake_phrase", "")),
        "command_text": str(state.get("command_text", "")),
        "passive_ignore_reason": str(state.get("passive_ignore_reason", "")),
        "wake_gate_mode": str(state.get("wake_gate_mode", "")),
        "owner_voice_verified": bool(state.get("owner_voice_verified", False)),
        "owner_voice_verification_mode": str(
            state.get("owner_voice_verification_mode", "")
        ),
        "owner_voice_required": bool(state.get("owner_voice_required", False)),
        "owner_detected": bool(state.get("owner_detected", False)),
        "screen_observer_enabled": bool(state.get("screen_observer_enabled", False)),
        "screen_read_only": bool(state.get("screen_read_only", True)),
        "pc_control_allowed": False,
        "latest_transcript": str(state.get("latest_transcript", "")),
        "latest_voice_reply": str(state.get("latest_voice_reply", "")),
        "audio_input_path": str(state.get("audio_input_path", "")),
        "audio_input_size_bytes": int(state.get("audio_input_size_bytes", 0) or 0),
        "audio_duration_seconds": float(
            state.get("audio_duration_seconds", 0.0) or 0.0
        ),
        "rms_peak": float(state.get("rms_peak", 0.0) or 0.0),
        "rms_avg": float(state.get("rms_avg", 0.0) or 0.0),
        "speech_duration_ms": int(state.get("speech_duration_ms", 0) or 0),
        "vad_reason": str(state.get("vad_reason", "")),
        "stt_model_used": str(state.get("stt_model_used", "")),
        "stt_model_cached": bool(state.get("stt_model_cached", False)),
        "stt_model_cache_key": str(state.get("stt_model_cache_key", "")),
        "language": str(state.get("language", "")),
        "stt_done": bool(state.get("stt_done", False)),
        "stt_reason": str(state.get("stt_reason", "")),
        "response_inflight": bool(state.get("response_inflight", False)),
        "duplicate_suppressed": bool(state.get("duplicate_suppressed", False)),
        "last_processed_transcript": str(state.get("last_processed_transcript", "")),
        "last_processed_at": float(state.get("last_processed_at", 0.0) or 0.0),
        "response_mode": str(state.get("response_mode", "")),
        "ollama_num_predict": int(state.get("ollama_num_predict", 0) or 0),
        "ollama_temperature": float(state.get("ollama_temperature", 0.0) or 0.0),
        "ollama_model_used": str(state.get("ollama_model_used", "")),
        "fast_path_used": bool(state.get("fast_path_used", False)),
        "fast_path_reason": str(state.get("fast_path_reason", "")),
        "llm_response": str(state.get("llm_response", "")),
        "tts_engine": str(state.get("tts_engine", "")),
        "tts_voice": str(state.get("tts_voice", "")),
        "tts_done": bool(state.get("tts_done", False)),
        "tts_reason": str(state.get("tts_reason", "")),
        "tts_cache_hit": bool(state.get("tts_cache_hit", False)),
        "tts_cache_path": str(state.get("tts_cache_path", "")),
        "tts_cache_prewarmed": bool(state.get("tts_cache_prewarmed", False)),
        "tts_model_cached": bool(state.get("tts_model_cached", False)),
        "tts_error_class": str(state.get("tts_error_class", "")),
        "tts_error_message": str(state.get("tts_error_message", "")),
        "voice_playback_attempted": bool(
            state.get("voice_playback_attempted", False)
        ),
        "voice_playback_done": bool(state.get("voice_playback_done", False)),
        "voice_playback_reason": str(state.get("voice_playback_reason", "")),
        "playback_pid": str(state.get("playback_pid", "")),
        "playback_interrupted": bool(state.get("playback_interrupted", False)),
        "playback_interrupt_reason": str(state.get("playback_interrupt_reason", "")),
        "barge_in_detected": bool(state.get("barge_in_detected", False)),
        "response_cancelled": bool(state.get("response_cancelled", False)),
        "audio_output_path": str(state.get("audio_output_path", "")),
        "vad_elapsed_seconds": float(state.get("vad_elapsed_seconds", 0.0) or 0.0),
        "stt_elapsed_seconds": float(state.get("stt_elapsed_seconds", 0.0) or 0.0),
        "wake_gate_elapsed_seconds": float(
            state.get("wake_gate_elapsed_seconds", 0.0) or 0.0
        ),
        "fast_path_elapsed_seconds": float(
            state.get("fast_path_elapsed_seconds", 0.0) or 0.0
        ),
        "ollama_elapsed_seconds": float(
            state.get("ollama_elapsed_seconds", 0.0) or 0.0
        ),
        "tts_elapsed_seconds": float(state.get("tts_elapsed_seconds", 0.0) or 0.0),
        "playback_elapsed_seconds": float(
            state.get("playback_elapsed_seconds", 0.0) or 0.0
        ),
        "total_turn_elapsed_seconds": float(
            state.get("total_turn_elapsed_seconds", 0.0) or 0.0
        ),
        "latency_profile": str(state.get("latency_profile", "")),
        "latest_screen_frame": str(state.get("latest_screen_frame", "")),
        "latest_screen_summary": str(state.get("latest_screen_summary", "")),
        "background_stdout_log": str(BACKGROUND_STDOUT_LOG),
        "background_stderr_log": str(BACKGROUND_STDERR_LOG),
    }


def _runtime_dead_reason(
    pid: int | None,
    supervisor_running: bool,
    heartbeat_age: float | None,
) -> str:
    if pid is None:
        return "pid_missing"
    if not supervisor_running:
        return "pid_not_running"
    if heartbeat_age is None:
        return "heartbeat_stale"
    if heartbeat_age > _heartbeat_stale_seconds():
        return "heartbeat_stale"
    return "ok"


def _heartbeat_stale_seconds() -> int:
    raw_value = os.environ.get("JARVIS_LIVE_HEARTBEAT_STALE_SECONDS", "120")
    if not raw_value.isdigit():
        return 120
    return max(10, min(int(raw_value), 3600))


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if isinstance(payload, dict):
        return payload
    return {}


def _read_pid() -> int | None:
    if not PID_FILE.exists():
        return None
    value = PID_FILE.read_text(encoding="utf-8").strip()
    if not value.isdigit():
        return None
    return int(value)


def _process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


if __name__ == "__main__":
    raise SystemExit(main())
