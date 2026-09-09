# Leg 426 — unit `R3` PRE-REGISTRATION (`THE DEPENDENCY DAG AND THE SPINE`)

**COMMITTED BEFORE THE RUNNER EXISTS AND BEFORE ANY GRAPH IS COMPUTED.** The charter: *"PRE-COMMIT,
in writing, before checking anything: which nodes are THE SPINE — the statements that, if false,
sink the theorem. Expect the spine to run through §4, §7 and §9; confirm or refute that from the
DAG, do not assume it."* What follows is fixed. A change after a graph exists is a `CORRECTIONS.md`
entry, not an edit.

## 1. What the graph is built from, and the direction rules

The ledger's `cites` strings (leg 425) mix three relations. R3 separates them by **named rules**,
applied mechanically to every string, with every firing banked in `dag.json`:

| rule | string pattern | edge produced |
|---|---|---|
| `DEP` (default) | a statement reference, or a string beginning *proved in / proved from* | citer **depends on** cited |
| `USED-BY` | a string beginning *used by / used in / used throughout / used after* | **reversed**: each listed statement depends on the citer |
| `PLURAL` | *Propositions A.4, A.7, … and Lemmas A.5, …* | one `DEP` edge per listed item (the R2 evidence regex counted none of these) |
| `TARGET` | override by name: `Proposition 9.9 → Theorem 3.1`, `Proposition C.3 → Theorem 4.6` (the citer's conclusion **is** the cited statement) | dropped |
| `POINTER` | override by name: `Theorem 1.1 → Corollary 10.6` (*"for alternative (D)"*), `Lemma A.5 → Proposition B.2` (*"the axis construction requires this datum"*) | dropped |

Any cycle surviving these five rules is reported as a cycle. **No further override is permitted
without a `CORRECTIONS.md` entry naming it.**

Cite strings that are neither a statement nor a displayed equation are classified as `REFERENCE`
(`[13]`, `[20]`), `CLASSICAL` (Duhamel, Rolle, Cauchy estimates, chain rule, integration by parts,
commutator identities), or `UNNUMBERED` (a Section pointer, a Remark, *"after (6.21)"*). **Every
`UNNUMBERED` target reachable from Theorem 1.1 is a dangling node** and is named.

## 2. THE SPINE — my judgment, written before the graph

The statements that, if false, sink Theorem 1.1, in dependency order:

```
Theorem 1.1
  Lemma 10.5 (uniqueness against a bounded-energy competitor)   Lemma 10.3 (force extension)
  Proposition 10.1 (localisation)                                Lemma 10.4 (energy)
Theorem 3.1
  Proposition 9.9 (realisation)   Lemma 5.4 (summation)   Proposition 5.5 (background)
  Proposition 9.6 (the +1/10 cycle)   Proposition 9.3 (the invariant)   Proposition 9.5 (stage 0)
  Proposition 9.1 / Lemma 9.2 (residual estimates)
  Proposition 7.2 (pulse inverse)   Lemma 7.1 (frame; λ₀² = 2aF₀²(1−2/v_s))
  Proposition 7.5 (positive representation)   Proposition 7.6 (signed inverse)   Lemma 7.7 (curls)
  Lemma 8.2 (compact radial inverse)   Lemma 8.6 (fast-time inverse)   Lemma 8.7 (five moments)
  Lemma 6.2 (common torus)   Definition 6.4 (classes)
Theorem 4.6
  Proposition C.3   Proposition C.2   Lemma C.1
  Proposition A.4   Proposition A.7   Lemma A.8   Proposition A.10
  Proposition B.2   Proposition B.5   Proposition B.8   Corollary B.10
  Lemma 4.5 (the cone test)   Lemma 4.4 (moment propagation)
```

**36 nodes.** Sections represented: 1, 3, 4, 5, 6, 7, 8, 9, 10, A, B, C. **§4, §7 and §9 are all
present**, as the charter expects. What I expect to be **outside** the spine: `Lemma 4.3`,
`Lemma 6.3`, `Corollary 7.3`, `Lemma 7.4`, `Corollary 7.8`, `Proposition 8.4`/`Corollary 8.5`
(consumed inside 9.6 but replaceable), `Lemma 9.7`/`Lemma 9.8` (bookkeeping), `Corollary 10.6`
(a consequence, not a support), `Lemma A.1`/`A.2`/`A.9`, `Lemma B.1`/`B.4`/`B.7`, `Corollary A.3`/`B.6`.

## 3. The mechanical spine, and the pre-committed numbers

The runner computes, on the dependency closure of `Theorem 1.1`:
- **`CHAIN`** — the longest `Theorem 1.1 → leaf` path (ties broken by lexicographic id);
- **`FAN`** — the number of statements in the closure that depend on each node, directly or
  transitively (transitive fan-in);
- **`SPINE_M`** := nodes on `CHAIN` ∪ nodes with transitive fan-in `≥ 20`.

| quantity | pre-committed expectation |
|---|---|
| acyclic after the five rules | **`YES`** |
| statements in Theorem 1.1's closure | **≥ 60** of 79 |
| statements NOT in the closure | **≤ 8**, named |
| dangling `UNNUMBERED` nodes reachable from Theorem 1.1 | **≥ 1** — I expect `Remark B.9` (the parameter order (B.40) lives in a Remark, not a proved statement) |
| longest chain length (edges) | **≥ 8** |
| `SPINE_M` contains §4, §7, §9 | **`YES`** |
| overlap: `SPINE_M ∩ §2-list` / `SPINE_M` | **≥ 0.75** |
| §2-list nodes absent from `SPINE_M` | named, each with its transitive fan-in |

## 4. THE GATE, in the charter's words

> *Is the DAG acyclic and complete — does every hypothesis of Theorem 1.1's proof trace to a
> proved statement, an appendix, or a cited reference? Name every dangling node.*

Answer format: **acyclic `YES`/`NO`** (with cycles named on `NO`); **complete
`YES`/`NO-AND-HERE-ARE-THE-DANGLING-NODES`**; then the spine confirmation §3 line by line, and
the §4/§7/§9 expectation **confirmed or refuted from the graph**.

## 5. Planted controls (both directions), fixed now
- `C1` an inserted back-edge makes the acyclicity check fail; removing it restores `YES`.
- `C2` deleting a leaf statement from a copy of the ledger makes completeness name it as dangling.
- `C3` switching the `USED-BY` rule off makes cycles reappear (the raw count is banked).
- `C4` a ledger in which `Theorem 1.1` cites nothing gives closure size 1 and every spine test fails.
- `C5` a five-node hand-built DAG with known longest chain (3) and known transitive fan-in.

**Ceiling.** A citation graph is a picture of what the manuscript *says* it uses. It cannot see a
step that is wrong, and it cannot see an unstated dependency. Nothing here is a verification;
`R4` is. **UNVERIFIED under §3f rule 1**, like every arc-6 answer.
