import hashlib
import os
import sys

GENESIS_FILE = os.path.expanduser("~/.local/share/maksimar/trust/genesis_hash.bin")

CRITICAL_FILES = [
    "CORE_ROOT/core_integrity_verifier.py",
    "BOOT/system_bootstrap.py",
]


def calculate_hash(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()


def load_genesis_hash():
    if not os.path.exists(GENESIS_FILE):
        print("Genesis hash not found. System not initialized.")
        sys.exit(1)

    with open(GENESIS_FILE, "r") as f:
        return f.read().strip()


def calculate_system_hash():
    combined = hashlib.sha256()

    for file in CRITICAL_FILES:
        if not os.path.exists(file):
            print(f"Critical file missing: {file}")
            sys.exit(1)

        file_hash = calculate_hash(file)
        combined.update(file_hash.encode())

    return combined.hexdigest()


def main():
    expected = load_genesis_hash()
    current = calculate_system_hash()
    print(current)

    if current != expected:
        print("SYSTEM INTEGRITY FAILURE")
        print("Switching to DEGRADED MODE")
        sys.exit(2)

    print("System integrity verified.")


if __name__ == "__main__":
    main()
