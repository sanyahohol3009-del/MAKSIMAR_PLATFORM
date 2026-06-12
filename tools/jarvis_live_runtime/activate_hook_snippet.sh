if [ -f "tools/jarvis_live_runtime/jarvis_live_chat_launcher.py" ]; then
  chat() {
    python tools/jarvis_live_runtime/jarvis_live_chat_launcher.py "$@"
  }
fi
