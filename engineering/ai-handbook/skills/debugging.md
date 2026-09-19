# Debugging

## Purpose

Find the actual cause of a defect through evidence, and fix the cause rather than the symptom. Debugging is applied science: hypotheses tested against observations, not guesses stacked on guesses.

## When To Use

- Any behavior that differs from expectation: failing test, wrong output, crash, performance cliff.
- Intermittent or "impossible" bugs — this discipline matters most exactly when the bug seems to defy it.
- Post-incident, when the pressure is off and the goal shifts from restoring service to understanding cause.

## Principles

- **Reproduce before you reason.** A reliable reproduction is the single most valuable debugging asset: it verifies the bug exists, enables experimentation, and later proves the fix. Effort spent shrinking a reproduction is almost never wasted.
- **Evidence over plausibility.** The plausible explanation and the true explanation coincide less often than intuition suggests. Read the actual error, the actual logs, the actual values — not your memory of what they usually say.
- **Change one thing at a time.** Each experiment should test one hypothesis. Shotgun changes that "fix" the bug leave you with working code and no knowledge — the bug's cause is still loose in your model of the system.
- **Keep a ledger.** For any bug that survives past the first hour: record hypotheses, experiments, and results, append-only. The ledger prevents circular investigation, enables handoff, and often reveals the answer by forcing precision.
- **The bug is a message about the system.** Every real bug reveals a gap — in tests, in validation, in observability, in understanding. The fix isn't finished until that gap is addressed.

## Workflow

1. **Capture the failure precisely.** Exact error text, inputs, environment, frequency. "It fails sometimes" becomes "fails on ~1/5 runs with input X since version Y."
2. **Reproduce it, then minimize it.** Get it failing on demand, then shrink: fewer steps, smaller input, fewer components — until what remains is nearly the cause itself.
3. **Locate before explaining.** Use bisection to corner the bug: which commit, which layer, which function, which input segment? Halving the search space beats theorizing about the whole of it. Recent changes are the leading suspects.
4. **Form a falsifiable hypothesis and test it.** "The cache returns stale entries after eviction" is testable; "something's wrong with the cache" is not. Design the cheapest experiment that could prove it false. Record the result either way.
5. **Confirm the mechanism.** When a hypothesis survives, trace the full causal chain from root cause to observed symptom. If any link is fuzzy ("somehow this leads to…"), keep digging — fixes applied to fuzzy mechanisms are symptom patches.
6. **Fix the cause; prove it with the reproduction.** Turn the reproduction into a permanent regression test. Confirm the test fails without the fix and passes with it.
7. **Close the gap the bug revealed.** Sweep for the same defect class elsewhere; add the validation or observability whose absence made this bug expensive to find; record the finding if it changes how others should work.

## Common Failure Modes

- **Fixing the symptom.** Adding a null check where the null appears, instead of asking why it's null. The cause resurfaces elsewhere, now with a workaround hiding it.
- **Debugging by superstition.** Restarting, clearing caches, reordering imports — sometimes these "work," and the cost is that the bug remains unexplained and will return.
- **Anchoring.** Deciding early what the bug "must be" and reading all subsequent evidence as confirmation. If two experiments contradict the theory, the theory is dead; let it die.
- **Trusting the report over the trace.** Bug reports describe perceptions ("saves are broken") not causes. Verify the reported behavior yourself before hunting for it.
- **The heroic all-nighter spiral.** Hours of unrecorded, undirected poking. Past the first hour without progress, the discipline (ledger, minimization, bisection) *is* the fast path — it only feels slow.
- **Declaring victory on "can't reproduce anymore."** If you don't know why it stopped, it didn't stop.

## Success Criteria

- The root cause is stated as a mechanism: *this* condition causes *this* behavior via *this* path.
- A regression test reproduces the bug and passes only with the fix.
- The fix removes the cause, not just the visible symptom.
- The investigation left artifacts: the test, the ledger (for long hunts), and any systemic gap recorded or fixed.

## Checklist

- [ ] Failure captured exactly (message, input, environment, frequency)
- [ ] Reliable reproduction obtained and minimized
- [ ] Search space narrowed by bisection before deep theorizing
- [ ] Hypotheses tested one at a time; results recorded
- [ ] Full causal mechanism understood before fixing
- [ ] Reproduction converted to a regression test; fix verified against it
- [ ] Same defect class swept for; revealed gaps closed or recorded

## Related Skills

- [testing.md](testing.md) — reproduction-as-test discipline.
- [building-observable-systems.md](building-observable-systems.md) — the infrastructure that makes debugging cheap.
- [implementing-changes.md](implementing-changes.md) — landing the fix with discipline.
