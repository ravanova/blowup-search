# Leg 438 — amendment to `leg_438_prereg.md`: slot 3 re-scoped after the `K1` follow-on

**Written and pushed BEFORE slot 3 is dispatched.** The pre-registration is not edited; this sits beside it.

## Why
Between the prereg's push and this wave's dispatch, a `K1` follow-on (`leg/437-k1-phaseB`, landed 1b9f9ea)
ran the comparator — `lean4export`, statement identity, axiom check, Lean-kernel and nanoda replay — on
phase B's prebuilt tree, in the SAME Conductor lineage. That is the substance of what slot 3 was to do.

## Ruling (Conductor; recorded in `CORRECTIONS.md` §76)
Slot 3 is **not retired** and **not narrowed**. §3f rule 1: a lineage cannot verify itself, and a second
machine plus a second kernel is still not a second agent. Slot 3 runs as pre-registered, with three things
fixed:

1. **Blind.** Slot 3 is told nothing of the follow-on — not its result, its logs, its artefact directory,
   nor this amendment or §76. Its brief is `STATE.md`'s `K2` gate item (3) and the pin, nothing more. The
   Conductor compares the two afterwards: agreement is then a two-route agreement on a quantity no worker
   chose; disagreement is an ESCALATION, not an adjudication.
2. **Its own tree.** The laptop's freshly rebuilt tree (`build_rc` 0, 11251 jobs, 2486 oleans, `total_s`
   4287, same pin `8937a8f4`), not the container's.
3. **The sandbox deviation closed if it can be.** `go` 1.22.2 is present here, so slot 3 attempts REAL
   `landrun` and records the outcome either way; the follow-on used the comparator's own
   `scripts/fake-landrun.sh` shim. If landrun cannot be built, that is `NOT-ESTABLISHED` with a cost, per
   prereg §5 — never a `FAIL`.

## Unchanged
Ownership (§3: one file, one owner, one branch, cherry-picked unedited), the pre-committed readings (§4),
resourcing (§5), integration (§6). Slot 5 is unchanged and remains the only thing that can move `K1` to
`VERIFIED`.
