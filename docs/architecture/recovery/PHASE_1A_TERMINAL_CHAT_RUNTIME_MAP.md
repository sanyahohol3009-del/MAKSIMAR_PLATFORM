# Phase 1A: карта terminal chat runtime

Дата проверки: 2026-07-17, Europe/Berlin.

## Фактическое разрешение команды

В интерактивном login Bash `type -a chat` и `command -v chat` возвращают alias:

```bash
alias chat='cd ~/MAKSIMAR_PLATFORM && source .venv/bin/activate && python tools/jarvis_live_runtime/jarvis_live_terminal_chat.py'
```

Shell-функция `chat` также присутствует в `tools/jarvis_live_runtime/activate_hook_snippet.sh`, но фактический alias запускает terminal client напрямую. Канонический пользовательский путь не использует `jarvis_live_chat_launcher.py`.

## Почему старый путь обращался к 8765 и disabled stream

`tools/jarvis_live_runtime/jarvis_live_terminal_chat.py` содержал собственные константы:

- исторически `API_BASE_URL = http://127.0.0.1:8765`; канонический ingress теперь `127.0.0.1:8000`;
- `STREAM_URL = .../jarvis-live/chat/stream`;
- `COMMAND_URL = .../jarvis-live/command`.

Обычный текст попадал через `_dispatch_user_text` → `_run_jarvis_turn` → `_print_stream_response` → `_stream_json_lines(STREAM_URL, payload)`. Payload состоял из `text`, `session_id=terminal_chat` и `pc_control_allowed=false`. Клиент читал JSON-lines через `httpx.Client.stream(...).iter_lines()`, обрабатывал события `start`, `route_selected`, `thinking`, `chunk`, `error`, `done` и печатал `chunk`, `text` или `llm_response`.

Сам terminal client uvicorn не запускает. Старый parallel-runtime launcher на 8765 удалён как dead path; terminal adapter не создаёт, не перезапускает и не останавливает API. Параметр `--restart` остаётся явно диагностируемым legacy no-op.

## Канонический путь после ремонта

Обычный `chat` по-прежнему запускает только terminal client, а тот теперь использует:

```text
CORE_ROOT.runtime_paths.CONTROL_PLANE_HOST = 127.0.0.1
CORE_ROOT.runtime_paths.CONTROL_PLANE_PORT = 8000
POST http://127.0.0.1:8000/jarvis-live/hot
```

Опциональный `MAKSIMAR_CONTROL_PLANE_BASE_URL` переопределяет base URL целиком; default берётся из единой runtime-конфигурации. Второй API не запускается, legacy command/stream endpoints не вызываются, ответ ожидается завершённым JSON без streaming.

Canonical payload:

```json
{
  "text": "<обычный текст>",
  "session_id": "terminal_chat",
  "input_channel": "terminal",
  "identity": {
    "identity_id": "aleksandr",
    "source": "local_terminal_session",
    "profile_type": "owner",
    "verified": true,
    "trusted_session": true
  }
}
```

`identity_context_from_http_payload` признаёт verified local terminal owner trusted без требования voice gate. Поэтому существующая policy сохраняет owner low-risk autonomy и поля owner/screen/keyboard_mouse/browser/direct action. Запрос без валидного identity остаётся anonymous/untrusted и получает false для owner permissions.

Текст извлекается по порядку: верхний `response_text`, верхний `llm_response`, затем те же поля во вложенном `result`. При `error_message`, `error_kind` или полностью пустом envelope печатается непустое честное сообщение о деградации. Timeout и недоступность Control Plane также отображаются непустым диагностическим сообщением.
