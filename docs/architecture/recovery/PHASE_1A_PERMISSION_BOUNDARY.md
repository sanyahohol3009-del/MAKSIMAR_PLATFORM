# Phase 1A Permission Boundary

HTTP identity is fail-closed: missing, unknown or unverified claims never become owner claims. `ProjectReadPermissionEvaluator` grants only `project.read` with `READ_ONLY` risk and records identity source, policy version, denial reason and trace. This grants no mutation, PC, shell, export or memory-write permission. Existing PC Control is unchanged.
