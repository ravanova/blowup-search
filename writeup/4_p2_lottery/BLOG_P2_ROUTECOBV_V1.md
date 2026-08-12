# Reading your own obligations document back to itself

*Leg 384, Route-COBV. Figure: fig105. Companion: `TECHNICAL_P2_ROUTECOBV_V1.md`.*

Two legs ago this repository wrote down what it would still owe the Clay Institute if the
programme ever worked — a document called `CLAY_OBLIGATIONS.md`, headed **STATUS: DRAFT,
UNVERIFIED**. Then leg 381 checked one section of it against Fefferman's official problem
statement and found the reviewer's reading was mostly right and twice wrong. Integration landed
those corrections. Someone read the edit and reported that it matched.

That last sentence is the interesting one, because *someone read it and it looked right* is
exactly the standard this repository is supposed to be refusing. So this leg read the document
back to itself **mechanically**: 23 clauses, each one compared against the artifact it claims to
rest on. Leg 381's banked verdicts. The four rigidity theorems' landed records. And, for the
first time, the Clay Institute's actual prize rules.

**17 matched. 6 did not.** No clause was unverifiable — the Clay rules answered **HTTP 200**,
so nothing had to be banked as a refusal.

## First, proving the checker could fail

A leg elsewhere in this cycle discovered a fabricated zero in its own instrument: a variable
initialised to `0.0`, never written, faithfully reported as a measurement. "Zero mismatches" has
precisely that shape. So each of the 23 checks carries a plant of its own, in both directions —
every MATCH had to be forced to read MISMATCH by corrupting the thing it checks, and every
MISMATCH had to be forced to read MATCH by repairing it. **23 controls, 23 fired.**

Three of them didn't fire at first, and each failure was the checker's fault rather than the
document's. The most instructive: the check on the `L³` tail could not be made to fail, because
the banked rows step **two** decades at a time and the naive difference was silently double the
per-decade figure. Fixing the control turned a false green light into one of the six real
findings. A green light that cannot go red isn't evidence — it's furniture.

## What was actually wrong

**A tolerance quoted from the best row.** §4 says a repaired energy law was *"verified to
`2.6e-5`"*. That is the error of the single best of four exponents (α = 0.8). The banked
worst case is **`2.57e-2`**, at α = 1.4 — **988 times larger**. And at α = 1, the exponent §4
is actually about, it's `2.65e-4`. The conclusion survives; the advertised precision doesn't.

**Three missing words.** §4 reports that *"the critical `L³` tail grows 326.875 per decade of
window"*. The source says *"the **cube of** the critical-norm tail"*. The norm itself goes
`8.679 → 14.841` over the same range. The physics is unchanged — the tail is log-divergent
either way, and never small however far out you cut — but the number is attached to the wrong
quantity.

**A strengthening flattened into a confirmation.** Running the comparison backwards, one of
leg 381's verdicts never made it into the document at all. On decay, leg 381 banked *CONFIRMED
**AND STRENGTHENED***: Fefferman's condition (4) bounds *every derivative*, not just the
function, and the reviewer's phrase understated it. The landed text says decay "stands as
stated."

**And the prize rules, which nobody had ever fetched.** §7 listed three requirements from
memory: a refereed journal, two years, general acceptance. Two years is right. The other two
aren't quite, and there's a fourth condition missing entirely:

- the rules say a refereed *publication* — and offer a **second qualifying route** the document
  omits;
- they say general acceptance in the **global** mathematics community, **"as determined in the
  sole discretion of CMI"** — not a fact the repository could ever observe for itself;
- Section 4(d) requires that the solution has *satisfactorily answered the questions raised by
  the Problem's official description*, again at CMI's sole discretion. That was simply absent.

Two more facts worth having: CMI **will not accept solutions submitted directly**, and — the one
that actually matters to this programme — Section 5(b) says that for Navier–Stokes **"a
resolution in either direction will be evaluated by the standard evaluation procedure"**. The
breakdown direction is explicitly in scope. Nobody here had checked that.

## One citation with nothing behind it

Not a mismatch, but worth saying. §2's first row cites "legs 253, 341". Leg 341's record carries
the claim word for word. **No banked JSON in the repository declares leg 253 at all.** The claim
is fine — it's independently confirmed by executing the screen module, which returns
`NOT-REACHED-BY-ANSATZ` on the object as specified — but half the citation points nowhere.

## What this doesn't mean

This leg edited nothing. A verifier reports gaps; it doesn't repair them. The exact replacement
text for all six findings is written out in the technical companion and routed to integration,
whose call it is to land.

And nothing here moved the mathematics. `CLAY_OBLIGATIONS.md` §6's two obligations still have no
method behind them, no link of the `L1 → L4` chain moved, and the honest number is unchanged:
**Clay stays ~0.05%.** What changed is smaller and duller and worth having anyway — the document
that says what we owe is now, clause by clause, something we've checked rather than something we
wrote down confidently.
