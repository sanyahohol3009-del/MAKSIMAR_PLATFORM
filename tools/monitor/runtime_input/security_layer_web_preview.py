from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.monitor.runtime_input.security_layer_terminal_preview import build_preview_payload


def render_html(payload: dict[str, object]) -> str:
    escaped_json = html.escape(json.dumps(payload, indent=2, ensure_ascii=False))
    status = html.escape(str(payload["status"]))
    layer_id = html.escape(str(payload["layer_id"]))
    batch_id = html.escape(str(payload["batch_id"]))

    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\">\n"
        "  <title>SECURITY_LAYER Preview</title>\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "  <style>\n"
        "    body { font-family: system-ui, sans-serif; background: #101318; color: #eef2f6; margin: 2rem; }\n"
        "    main { max-width: 980px; margin: 0 auto; }\n"
        "    .card { border: 1px solid #2c3440; border-radius: 16px; padding: 20px; background: #171c24; }\n"
        "    pre { white-space: pre-wrap; word-break: break-word; background: #0c0f14; padding: 16px; border-radius: 12px; }\n"
        "  </style>\n"
        "</head>\n"
        "<body>\n"
        "  <main>\n"
        "    <section class=\"card\">\n"
        f"      <h1>{layer_id}</h1>\n"
        f"      <p>Batch: {batch_id}</p>\n"
        f"      <p>Status: {status}</p>\n"
        "      <p>Read-only preview. No execution path is exposed.</p>\n"
        f"      <pre>{escaped_json}</pre>\n"
        "    </section>\n"
        "  </main>\n"
        "</body>\n"
        "</html>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render SECURITY_LAYER read-only HTML preview.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--blocked", action="store_true")
    args = parser.parse_args()

    payload = build_preview_payload(blocked=args.blocked)
    document = render_html(payload)

    if args.output:
        args.output.write_text(document, encoding="utf-8")
        print(str(args.output))
    else:
        print(document)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
