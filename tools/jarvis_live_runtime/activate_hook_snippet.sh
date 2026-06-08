if [ "${JARVIS_LIVE_AUTO_START:-1}" = "0" ]; then
  echo "JARVIS Live: auto-start disabled"
  return 0 2>/dev/null || exit 0
fi

if [ ! -f "tools/jarvis_live_runtime/jarvis_live_start.py" ]; then
  echo "JARVIS Live: not inside MAKSIMAR_PLATFORM root"
  return 0 2>/dev/null || exit 0
fi

echo "JARVIS Live: starting/background/status"
python tools/jarvis_live_runtime/jarvis_live_start.py --background >/dev/null 2>&1 &
