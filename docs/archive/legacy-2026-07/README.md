# Legacy policy docs — archived, NOT authoritative

Imported 2026-08-21 during the all-branch merge into `main`.

Source: `desktop-pc` / `feat/theme-pools-lifestyle-scoped` (last active 2026-07-20).
Those branches forked from the root commit and evolved their own numbering, so
these files collide with live docs that use the same numbers but cover different
topics:

| archived file | live doc at that number (authoritative) |
|---|---|
| `00_POLICY_INDEX.md` | `docs/00_MASTER_RULES.md` |
| `07_QUALITY_MEMORY.md` | `config/QUALITY_MEMORY.json` |
| `18_MASTER_CATALOG_CONSISTENCY_POLICY.md` | `docs/18_ZERO_TOLERANCE_QC_POLICY.md` |
| `19_RECOVERY_CHECKPOINT.md` | `docs/19_ZERO_CONFIRMATION_POLICY.md` |
| `20_MASTER_PROMPT_LIBRARY.md` | `docs/20_ZERO_INTERNAL_OUTPUT_POLICY.md` |
| `21_CATALOG_BRIEF_SPEC.md` | `docs/21_HIGGSFIELD_ENGINE_LOCK.md` |

Rules here are **superseded**. They are kept for reference/learning only: never
load them at session start, never cite them in a prompt, and never let them
override the live docs, `prompts/`, `config/model.json`, `config/gates.json` or
`config/angle_matrix.json`.

The image generation flow is unchanged by this import: **Higgsfield only**,
model lock `nano_banana_2`, 1:1 / 2K, one render per slot.
