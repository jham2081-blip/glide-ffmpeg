# Code Review

## Purpose

Catch defects and bad decisions while they are still cheap, and spread understanding of the codebase across its contributors. Review is the last gate where a mistake costs a comment instead of an incident — and the main channel through which a team's standards actually propagate.

## When To Use

- Reviewing any change before it merges — human-written or AI-written.
- Reviewing your own diff before requesting review (self-review is the highest-ROI review).
- Receiving review: responding to feedback is half the skill.

## Principles

- **Review the decisions first, the syntax last.** The expensive mistakes are embedded choices: a new dependency, a changed contract, a silent assumption, a missing failure path. Style nits are cheap to fix anytime; wrong decisions calcify.
- **Correctness requires adversarial reading.** Don't ask "does this look right?" — ask "what input, what timing, what failure makes this wrong?" Read the change the way production will exercise it, not the way the author intended it.
- **Tests are part of the diff.** Review them with equal weight: do they fail without the change? Do they cover the failure paths? A behavior change with weakened or missing tests is an incomplete change, however clean the code.
- **Verify claims, don't inherit them.** "Tested manually, works" is a claim. For consequential changes, run it, or require evidence (test output, reproduction steps). This applies doubly to AI-authored changes, where fluent prose and correct behavior are independent variables.
- **Comment on the code, calibrate by severity.** Distinguish clearly: *blocking* (correctness, security, data loss), *should-fix* (maintainability, missing tests), *optional* (preference — and say so). A review where everything sounds equally important teaches the author nothing.
- **Review size is a shared responsibility.** Beyond a few hundred lines, defect-detection collapses and "LGTM" becomes a reflex. Authors owe reviewers small, coherent changes; reviewers are entitled to ask for a split.

## Workflow

1. **Read the description and the problem before the diff.** What was the change supposed to do? A diff can be perfect code for the wrong task.
2. **First pass — the shape.** Does the approach fit the plan and the codebase's conventions? Are there surprise files, surprise dependencies, surprise scope? If the shape is wrong, say so now, before line-level effort is spent by anyone.
3. **Second pass — adversarial correctness.** Walk the failure paths: bad input, empty collections, concurrent access, partial failure, boundary values. Check every place the change *should* have touched but didn't — call sites, config, docs, fixtures (sins of omission hide outside the diff).
4. **Third pass — the tests.** Would these tests catch the bugs you just looked for? Were any existing tests weakened to get to green?
5. **Verify behavior for consequential changes.** Check out and run it, or demand evidence. Scale this to blast radius.
6. **Write the review.** Lead with the blocking items and the overall verdict. Mark severity on everything. Ask questions where you're unsure instead of asserting — "what happens if X is empty?" finds bugs and teaches, in both directions.
7. **As the author: respond to substance, re-request after real changes.** Push back with evidence where the reviewer is wrong — review is a dialogue, not a compliance exercise. Never resolve a blocking comment with silence.

## Common Failure Modes

- **Nit-storm, decision-blindness.** Twenty comments on naming, zero on the new unvetted dependency or the swallowed exception. The review *felt* thorough and checked nothing that mattered.
- **Rubber-stamping large diffs.** Approval latency held constant while diff size grows — meaning scrutiny per line silently went to zero.
- **Reviewing the author, not the code.** Trusting a diff because of who (or what) wrote it. Seniority and fluency both fail; the review exists because everyone fails.
- **Style wars in review.** Relitigating preferences the codebase has already settled. If it matters, encode it in a linter; if a linter can't check it and doctrine doesn't cover it, it's probably taste.
- **Sin-of-omission blindness.** Reviewing only the lines that changed. The bug is often the line that *didn't* change: the un-updated call site, the missing migration, the doc now describing the old behavior.
- **Approval under social pressure.** "It's urgent" compresses the timeline, not the correctness bar. An urgent broken change is strictly worse than a slightly later working one.

## Success Criteria

- Blocking issues are found in review, not in production — and the ones found are decision-level, not just typo-level.
- Every behavior change merged has tests a reviewer actually evaluated.
- Review comments carry explicit severity; authors can tell what must change.
- Diff sizes stay reviewable because both sides enforce it.
- Knowledge moves: reviewers can maintain code they reviewed.

## Checklist

- [ ] Understood the intended change before reading the diff
- [ ] Shape reviewed: approach, conventions, scope, surprise dependencies
- [ ] Failure paths and boundaries walked adversarially
- [ ] Omissions checked: call sites, config, docs, migrations outside the diff
- [ ] Tests reviewed as first-class code; would they catch the likely bugs?
- [ ] Behavior verified or evidence required, scaled to blast radius
- [ ] All comments severity-marked; blocking items stated as blocking

## Related Skills

- [implementing-changes.md](implementing-changes.md) — producing reviewable diffs.
- [testing.md](testing.md) — what good test coverage looks like.
- [../doctrine/AI_COLLABORATION.md](../doctrine/AI_COLLABORATION.md) — reviewing AI-authored changes.
