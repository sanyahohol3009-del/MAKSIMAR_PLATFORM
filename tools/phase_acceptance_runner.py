from __future__ import annotations

import argparse
import subprocess
import sys


def run(command: list[str], label: str) -> None:
    print(f"===== {label} =====")
    completed = subprocess.run(command, text=True, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description="MAKSIMAR phase acceptance runner.")
    parser.add_argument("--phase", required=True)
    parser.add_argument("--compile", nargs="*", default=[])
    parser.add_argument("--local-tests", nargs="*", default=[])
    parser.add_argument("--related-tests", nargs="*", default=[])
    parser.add_argument("--full-auto", action="store_true")
    parser.add_argument("--tb", default="short")
    parser.add_argument("--skip-pre-step", action="store_true")
    parser.add_argument("--skip-post-step", action="store_true")
    args = parser.parse_args()

    run(["git", "restore", ".pymon"], "RESTORE GENERATED MONITOR FILE")

    if not args.skip_pre_step:
        run([sys.executable, "tools/roadmap_pre_step_check.py"], f"{args.phase} ROADMAP PRE-STEP CHECK")

    if args.compile:
        run([sys.executable, "-m", "py_compile", *args.compile], f"PY_COMPILE {args.phase}")

    if args.local_tests:
        run(
            [sys.executable, "-m", "pytest", *args.local_tests, "-q", f"--tb={args.tb}"],
            f"{args.phase} LOCAL TESTS",
        )

    if args.related_tests:
        run(
            [sys.executable, "-m", "pytest", *args.related_tests, "-q", f"--tb={args.tb}"],
            f"{args.phase} RELATED PACK",
        )

    if args.full_auto:
        run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-n",
                "auto",
                "--dist=loadfile",
                "--import-mode=importlib",
                "-q",
                f"--tb={args.tb}",
            ],
            f"{args.phase} FULL AUTO PARALLEL",
        )

    if not args.skip_post_step:
        run([sys.executable, "tools/roadmap_post_step_drift_check.py"], f"{args.phase} ROADMAP POST-STEP FULL DRIFT CHECK")

    run(["git", "status", "--short"], f"{args.phase} STATUS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
