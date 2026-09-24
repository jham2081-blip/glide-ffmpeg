# Implementing Changes

## Purpose

Execute a planned change with discipline: conforming to the codebase, staying in scope, keeping the system working at every step, and producing a change that is honest about what it does. This is the skill of *not making things worse while making things better*.

## When To Use

- Every code change, from bug fix to feature. This is the default working discipline.
- Especially when working as an AI agent, where volume of output makes discipline the differentiator.

## Principles

- **Conform to the codebase you're in.** Match its naming, structure, error handling, comment density, and test style — even where you'd personally choose differently. Consistency is a feature of the codebase; your preference is not.
- **Keep the system green.** Prefer sequences of small, working states over one long broken excursion. If the build or tests are broken by your intermediate state, shorten the intermediate state.
- **Change what the task requires — nothing else.** No drive-by reformatting, no opportunistic renames, no unrelated fixes in the same change. Adjacent problems get recorded (see [managing-technical-debt](managing-technical-debt.md)), not absorbed.
- **Make the change explain itself.** Clear names, code that reads top-to-bottom, comments only for constraints the code cannot express. A commit message that states *why*.
- **Handle failure paths with the same care as success paths.** Errors should be caught where they can be handled, reported with context, and never swallowed. A silent failure is a bug with a delay on it.
- **Verify by exercising, not by inspecting.** Code that looks right and code that is right are different populations. Run the changed path.

## Workflow

1. **Confirm the baseline.** Run the relevant tests before changing anything. A pre-existing failure discovered afterward becomes indistinguishable from one you caused.
2. **Work the plan in small increments.** Implement one coherent piece, verify it, continue. When the plan proves wrong mid-implementation, stop and revise the plan — don't improvise a new design inside the diff.
3. **Write or extend tests alongside the code.** Each behavior the change introduces gets a test that fails without the change (see [testing](testing.md)).
4. **Sweep for completeness.** Search for all call sites, config references, fixtures, and docs that encode the thing you changed. Half-propagated changes are a leading source of review churn and production surprises.
5. **Synchronize documentation.** Any README, usage doc, or comment invalidated by the change gets updated in the same change (see [writing-documentation](writing-documentation.md)).
6. **Verify end-to-end.** Exercise the actual affected flow — run the app, hit the endpoint, invoke the CLI — not just the unit tests. Observe the new behavior happening.
7. **Review your own diff before handing it over.** Read the full diff as a reviewer would. Remove debug artifacts, leftover comments, and anything you can't justify. Then report honestly: what changed, how it was verified, what remains.

## Common Failure Modes

- **The ever-growing diff.** Fix leads to refactor leads to rename leads to a 40-file change nobody can review. Scope discipline decays one "while I'm here" at a time.
- **Convention override.** Introducing a personally-preferred pattern into a codebase that consistently does it another way, creating a permanent "why are there two?" for every future reader.
- **Green-tests fallacy.** Declaring done because existing tests pass, when no test exercises the new behavior. Passing tests you didn't write test the code you didn't change.
- **Silent adaptation.** Discovering mid-implementation that the plan is wrong and quietly building something different from what was agreed. Surface it.
- **Claim inflation.** Reporting "done and tested" when the truth is "written and compiles." Trust, once spent, makes all future work slower.

## Success Criteria

- The diff contains exactly what the plan promised — a reviewer finds no surprises.
- New behavior is covered by tests that fail without the change.
- The changed flow was exercised end-to-end and observed working.
- Documentation, config, and call sites are consistent with the change.
- The report of what was done matches what the diff and test output show.

## Checklist

- [ ] Baseline tests run before starting
- [ ] Change conforms to local conventions
- [ ] Scope matches the plan; adjacent problems recorded, not absorbed
- [ ] New behavior tested; tests fail without the change
- [ ] All call sites / references / fixtures / docs swept and updated
- [ ] Affected flow exercised end-to-end
- [ ] Self-reviewed the full diff; report matches reality

## Related Skills

- [designing-a-change.md](designing-a-change.md) — the plan this skill executes.
- [testing.md](testing.md) — verifying behavior.
- [code-review.md](code-review.md) — the receiving end of your diff.
- [debugging.md](debugging.md) — when the change doesn't behave.
