#!/usr/bin/env python3
"""Production heartbeat writer for MAKSIMAR."""

from __future__ import annotations

import argparse
import signal
import time
from pathlib import Path

from heartbeat_io import atomic_write_json, build_heartbeat


class HeartbeatWriter:
    """Atomic heartbeat writer loop."""

    def __init__(self, output_file: Path, source: str, interval_sec: float) -> None:
        self.output_file = output_file
        self.source = source
        self.interval_sec = interval_sec
        self._running = True

    def write(self, status: str) -> None:
        payload = build_heartbeat(source=self.source, status=status)
        atomic_write_json(self.output_file, payload)

    def stop(self) -> None:
        self._running = False

    def run(self) -> None:
        self.write("alive")

        while self._running:
            self.write("alive")
            time.sleep(self.interval_sec)

        self.write("stopped")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MAKSIMAR heartbeat writer")

    parser.add_argument(
        "--file",
        required=True,
        help="Heartbeat JSON file path",
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Heartbeat source name",
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Write interval seconds",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    writer = HeartbeatWriter(
        output_file=Path(args.file),
        source=args.source,
        interval_sec=args.interval,
    )

    def handle_signal(_sig, _frame):
        writer.stop()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    writer.run()


if __name__ == "__main__":
    main()
