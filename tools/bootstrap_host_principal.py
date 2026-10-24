"""Local OS-bound bootstrap for a short-lived HOST approval principal."""
from __future__ import annotations

import argparse

from MAKSIMAR_CORE_LIB.security_layer.host_principal import bootstrap_local_owner_token


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-id", required=True)
    args = parser.parse_args()
    # The token is intentionally emitted only to the invoking local owner
    # process; the signing secret is never printed.
    print(bootstrap_local_owner_token(session_id=args.session_id))


if __name__ == "__main__":
    main()
