# BLOCKS_INDEX

Subproject ID: `SP-20260530-b1-boss-rollout`
ID rule: canonical block IDs use `BLOCK-NNN_slug`; `B1` is layer label only.

| Canonical Block ID | Name | Status | Purpose | Depends on | Canonical Inputs | Runtime Outputs |
|---|---|---|---|---|---|---|
| `BLOCK-001-task-control-pack-smoke` | Task Control Pack smoke | `closed_by_user_with_report` | Historical smoke block closed administratively after user stopped old `B1/BOS` system | `none` | `BLOCK_PLAN.md`, `CONTEXT_PACK.md` | `BLOCK_REPORT.md` |
| `BLOCK-002-subproject-linkage-validator` | Subproject linkage validator | `cancelled_with_system_shutdown` | Planned follow-up block that must not start because old `B1/BOS` system was closed by user | `BLOCK-001 accepted by Boss review` | `TBD after BLOCK-001` | `not created` |

## Notes

- Do not add runtime report paths before files exist.
- Do not mark any block `accepted` before `Boss review`.
- `BLOCK-001` ended as closure evidence, not system proof.
- Do not continue old `B1/BOS` hierarchy from this index.
