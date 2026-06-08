from __future__ import annotations

import argparse
import shutil
import time
from pathlib import Path


BLOCK_START = "# >>> JARVIS_LIVE_AUTO_START >>>"
BLOCK_END = "# <<< JARVIS_LIVE_AUTO_START <<<"
HOOK_LINE = "source tools/jarvis_live_runtime/activate_hook_snippet.sh"
HOOK_BLOCK = f"{BLOCK_START}\n{HOOK_LINE}\n{BLOCK_END}\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--remove", action="store_true")
    args = parser.parse_args(argv)
    activate_path = Path(".venv") / "bin" / "activate"

    if args.remove:
        return _remove_block(activate_path, apply=args.apply)
    return _ensure_block(activate_path, apply=args.apply)


def _ensure_block(activate_path: Path, apply: bool) -> int:
    current = _read_activate(activate_path)
    updated = _insert_block(current)
    _print_preview(updated)
    if apply and updated != current:
        _backup(activate_path)
        activate_path.write_text(updated, encoding="utf-8")
    return 0


def _remove_block(activate_path: Path, apply: bool) -> int:
    current = _read_activate(activate_path)
    updated = _strip_block(current)
    _print_preview(updated)
    if apply and updated != current:
        _backup(activate_path)
        activate_path.write_text(updated, encoding="utf-8")
    return 0


def _read_activate(activate_path: Path) -> str:
    if not activate_path.exists():
        return ""
    return activate_path.read_text(encoding="utf-8")


def _insert_block(content: str) -> str:
    if BLOCK_START in content and BLOCK_END in content:
        return content
    separator = "" if content.endswith("\n") or not content else "\n"
    return f"{content}{separator}{HOOK_BLOCK}"


def _strip_block(content: str) -> str:
    start = content.find(BLOCK_START)
    end = content.find(BLOCK_END)
    if start == -1 or end == -1 or end < start:
        return content
    end += len(BLOCK_END)
    if end < len(content) and content[end] == "\n":
        end += 1
    return content[:start] + content[end:]


def _backup(activate_path: Path) -> None:
    timestamp = time.strftime("%Y%m%d%H%M%S")
    backup_path = activate_path.with_name(f"activate.bak.{timestamp}")
    shutil.copy2(activate_path, backup_path)


def _print_preview(content: str) -> None:
    print("JARVIS_LIVE_ACTIVATION_HOOK_PREVIEW")
    print(content)


if __name__ == "__main__":
    raise SystemExit(main())
