#!/usr/bin/env python3

import hashlib
import time
from pathlib import Path


CORE_DIR = Path("CORE_ROOT")
CHECK_INTERVAL = 5


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def snapshot():
    hashes = {}

    for p in CORE_DIR.rglob("*.py"):
        hashes[str(p)] = file_hash(p)

    return hashes


def main():

    print("[RUNTIME] Guard started")

    baseline = snapshot()

    while True:

        time.sleep(CHECK_INTERVAL)

        current = snapshot()

        if current != baseline:

            print("[RUNTIME] CORE MODIFICATION DETECTED")
            print("[RUNTIME] EMERGENCY LOCKDOWN")

            exit(1)


if __name__ == "__main__":
    main()
