if [ -f "tools/jarvis_live_runtime/jarvis_live_chat_launcher.py" ]; then
  chat() {
    python tools/jarvis_live_runtime/jarvis_live_chat_launcher.py "$@"
  }
fi

if [ "${JARVIS_LIVE_AUTO_START:-0}" != "1" ]; then
  return 0 2>/dev/null || exit 0
fi

if [ ! -f "tools/jarvis_live_runtime/jarvis_live_start.py" ]; then
  echo "JARVIS Live: not inside MAKSIMAR_PLATFORM root"
  return 0 2>/dev/null || exit 0
fi

export JARVIS_LIVE_ALWAYS_LISTEN="${JARVIS_LIVE_ALWAYS_LISTEN:-0}"
export JARVIS_LIVE_LISTEN_SECONDS="${JARVIS_LIVE_LISTEN_SECONDS:-6}"
export JARVIS_LIVE_LISTEN_INTERVAL_SECONDS="${JARVIS_LIVE_LISTEN_INTERVAL_SECONDS:-2}"

echo "JARVIS Live: starting/background/status always-listen=${JARVIS_LIVE_ALWAYS_LISTEN}"
python tools/jarvis_live_runtime/jarvis_live_start.py --background >/dev/null 2>&1 &
