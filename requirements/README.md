# Development dependency profiles

`dev.txt` pins the existing Codegraph Python structural extraction/test toolchain.
It does not enable LLM extras, invoke models, start services or rebuild a graph.
Other requirement profiles retain their existing scope.

## Managed Codegraph 0.3.29 patch

Owner: the existing Codegraph extract/cache implementation and this requirements
directory. No alternate graph engine, loader, registry or answer authority is
introduced. `patches/codegraph-tools-0.3.29.patch` consolidates the already-used
project-relative identities, import resolution, local import sites, method-owner
and cache-identity fixes. No new extractor implementation was authored here.
Keep `patches/codegraph-tools-LICENSE.txt` with the patch: it contains the upstream
MIT notice.

Upstream release metadata: https://pypi.org/pypi/codegraph-tools/0.3.29/json

Wheel: `codegraph_tools-0.3.29-py3-none-any.whl`

Wheel SHA256: `75349ac4769058504dac3c8d2f68702ed53187fd96b19cee0bf05d81e901f71c`

Current upstream acceptance of the project patches is NOT_PROVEN. Do not upgrade
or replace the pinned tool implicitly.

## Reproduction procedure

Use a fresh disposable CPython 3.12 virtual environment without system or live
project site packages. Install the pinned `dev.txt` wheels, then run `pip check`.
Do not alter a running project environment.

Locate that environment's site-packages directory. Before applying the patch,
verify the two original source hashes below. Reject any mismatch, including an
already-patched package. Use the existing standard `patch` utility with strip
level 1, batch/forward mode and fuzz 0, targeting only that environment's
site-packages. Run its dry-run first, then apply the same patch once. Verify the
two resulting hashes. There is no retry loop or implicit source replacement.

The distributed unified patch uses zero context so context-only blank lines do
not require disabling Git whitespace checks. Full original-file hashes remain
mandatory before application. This serialization was separately applied to the
original sources and produced the identical bytes tested in the clean venv.
Patch SHA256: `7bb4eef26f6cb00be4edc00c25503daa7171b5ad72044b755f25329e11500870`.

| File | Original upstream SHA256 | Managed patched SHA256 |
|---|---|---|
| `codegraph/cache.py` | `f667ce0de4135f635cddafe0c1471fa836bee50e42b4641b80c914395ae86dac` | `37621f49455640d433a189a4a688d43664882ae04bc7d2d54c10dde7e1a7a204` |
| `codegraph/extract.py` | `b6d314099bc4071f5829a42da70ba2810d0b8ede2d76f962949678f7fc0d0811` | `182d86123b681457f51c0e7faa94c66ca9e2b1804fe95809bdfd9211cbd5ce21` |

## Proof and limits

The owner audit installed 28 pinned downloaded wheels offline into a fresh venv.
Nine unchanged existing Python structural regression tests gave 7 FAIL / 2 PASS
against the original release and 9 PASS after the patch. Both patched hashes
exactly matched the working implementation; the live environment was unchanged.

Evidence remains with the existing local audit owner in
`RUNTIME/audits/WSL_RECOVERY_ACTIVATION_20261011/owner_20261018_canonical_audit_retention.json`,
section `codegraph_portability_reconciliation`. Original failures are retained.

This proves scoped Python extraction/cache reproducibility, not all language
integrations, natural acceptance, model readiness or platform activation. The
upstream installed RECORD is deliberately not rewritten: its two hashes differ
after this known source patch. Check the explicit post-patch hashes rather than
hiding the provenance. No full vendor import or publication of `.venv` is needed.
