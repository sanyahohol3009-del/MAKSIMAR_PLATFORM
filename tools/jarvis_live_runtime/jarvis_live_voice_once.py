from __future__ import annotations

import os

from tools.jarvis_live_runtime.jarvis_live_background_loop import (
    FASTER_WHISPER_MODEL_ROOT,
    run_voice_once,
)


MICROPHONE_BRIDGE = "RDPSource"
DOWNLOAD_ROOT = FASTER_WHISPER_MODEL_ROOT


def main() -> int:
    seconds = _listen_seconds()
    payload = run_voice_once(seconds=seconds)
    print("JARVIS_LIVE_VOICE_ONCE")
    print(f"owner_detected={str(payload['owner_detected']).lower()}")
    print(f"transcript={payload['transcript']}")
    print(f"reply={payload['reply']}")
    print("pc_control_allowed=false")
    return int(payload["exit_code"])


def _listen_seconds() -> int:
    raw_value = os.environ.get("JARVIS_LIVE_LISTEN_SECONDS", "6")
    if not raw_value.isdigit():
        return 6
    return max(1, min(int(raw_value), 30))


if __name__ == "__main__":
    raise SystemExit(main())
