# PERSONAL_OWNER_AUTONOMY_POLICY

Owner authorization is `identity resolver + trusted session policy`; a voice gate is evidence, not
the sole authority. Accepted v1 sources are verified voice identity, trusted local terminal session,
trusted authenticated HTTP session and trusted UI session. HTTP/UI claims require an explicit
trusted-session assertion. Missing, invalid, unknown or untrusted remote identity is fail-closed.

| Identity profile | Action risk | Permission | Confirmation |
|---|---|---|---|
| Verified owner Aleksandr, trusted session | READ_ONLY | allow within capability policy | none |
| Verified owner Aleksandr, trusted session | LOW_RISK / REVERSIBLE PC action | allow existing owner action path | explicit owner command is approval |
| Verified owner Aleksandr, trusted session | HIGH_RISK / DESTRUCTIVE | deny direct execution | separate explicit confirmation required |
| Trusted family | allowed READ_ONLY | allow within family profile | per policy |
| Trusted family | PC mutation/execution | existing family policy; never owner autonomy | approval required where supported |
| Unknown / invalid / unverified / untrusted remote | allowed READ_ONLY | read-only profile only | none |
| Unknown / invalid / unverified / untrusted remote | any PC mutation/execution | deny | cannot self-approve |

This Phase 1A change is only the common identity boundary. It does not modify the PC Control
implementation, route semantics, action allowlist or the verified owner's low-risk autonomy.
