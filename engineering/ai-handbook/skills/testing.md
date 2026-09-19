# Testing

## Purpose

Use tests as executable evidence for the promises that matter. Good tests catch regressions, document intended behavior, and let people change software confidently. Unnecessary tests add maintenance cost and can make a codebase harder to change without increasing confidence.

## When To Use

- Alongside meaningful new or changed behavior whose promise should survive future refactors.
- Before fixing a bug when a deterministic regression test can reproduce the defect.
- Around contracts, boundaries, failure paths, data integrity, concurrency, security, or other behavior where regression cost is material.
- When inheriting untested behavior you must change and a characterization test is the safest way to establish the current contract.
- When deciding whether an existing check, type system, lint rule, build, or end-to-end exercise is sufficient instead of adding another test.

Do not add a test automatically for a reversible, low-impact mechanical change when the test would merely mirror the implementation and existing validation already proves the intended outcome.

## Principles

- **Test behavior, not implementation.** Assert what the system promises callers, users, or neighboring components.
- **Verification is proportional to risk.** The goal is sufficient evidence for the blast radius, not the maximum number of checks.
- **A test must be capable of catching a meaningful regression.** A test that only echoes a mock or restates the implementation is maintenance cost without protection.
- **Prefer the smallest durable proof.** A unit test may be enough for pure logic; an integration test may be the right proof for a contract; sometimes a build, lint rule, schema validator, or focused end-to-end check is better than a new test.
- **Bug regressions deserve executable memory when practical.** A reproduced defect converted into a test is far more valuable than a prose warning.
- **Deterministic or repaired.** Flaky tests train contributors to ignore red and erode the whole suite's value.
- **Failure paths are part of the behavior.** Invalid input, partial failure, missing dependencies, and boundary conditions deserve coverage when they are material to the promise.
- **Fast feedback shapes behavior.** Keep common checks cheap enough that people and agents actually run them.

## Workflow

1. **Identify the promise and its risk.** What could regress, who would notice, and what would it cost? If there is no meaningful persistent behavior to protect, a new test may not be needed.
2. **Choose the smallest proof that genuinely exercises that promise.** Prefer an existing check when it already covers the risk. Otherwise choose unit, integration, contract, or end-to-end testing at the lowest useful level.
3. **For bugs, reproduce before fixing when practical.** Capture the defect with a failing test or deterministic reproduction so the fix is proven rather than guessed.
4. **For new behavior, prove the check can detect absence or breakage.** This may mean observing the test fail before implementation, temporarily reverting the relevant line, or otherwise demonstrating that the check is not vacuous.
5. **Use real collaborators when cheap; fake only at genuine boundaries.** Do not replace your own domain behavior with mocks and then congratulate the mock for returning what you configured.
6. **Keep tests independent and readable.** Own setup and data; avoid hidden ordering, shared mutable state, or accidental network/time dependence.
7. **Run the checks appropriate to the change.** Once the relevant checks pass, broaden only when the blast radius, failures, or unresolved concerns justify it. Do not repeat broad suites without a reason.

## Common Failure Modes

- **Testing the mock.** Configure X, assert X, learn nothing.
- **Mirror tests.** Re-encode a trivial implementation detail in a test so both must change together.
- **Change-detector tests.** Snapshot or assertion styles that fail on any edit regardless of correctness.
- **Verification maximalism.** Running or adding every conceivable test for a small change, burning time while adding little confidence.
- **Verification minimalism.** Calling a high-risk change done because one happy-path unit test passed.
- **Weakening tests to make them pass.** Deleting assertions, broadening tolerances, or skipping checks to get green.
- **Happy-path-only suites.** Ignoring the error path where the real incident will happen.
- **Coverage worship.** Optimizing a percentage rather than meaningful failure detection.
- **The unrunnable suite.** Tests that require undocumented setup and therefore rot into decoration.

## Success Criteria

- Meaningful behavior changes and bug fixes have durable executable protection when that protection adds real value.
- Low-impact mechanical changes are verified without manufacturing mirror tests.
- The chosen checks match the change's blast radius and failure modes.
- A regression test for a bug fails without the fix and passes with it when practical.
- The suite remains deterministic and readable.
- Contributors can tell what promise broke from a failure without archaeology.

## Checklist

- [ ] Identified the behavior promise and regression risk
- [ ] Chosen the smallest meaningful proof
- [ ] Reused existing validation when it already covers the risk
- [ ] Bug fix reproduced before fixing when practical
- [ ] New test/check shown capable of detecting the relevant breakage
- [ ] Failure paths covered where material
- [ ] No mock-echo or implementation-mirror test added
- [ ] Relevant checks run; broader checks added only when justified

## Related Skills

- [implementing-changes.md](implementing-changes.md) — verification as part of the change.
- [debugging.md](debugging.md) — reproduction and regression protection for defects.
- [code-review.md](code-review.md) — evaluating whether verification matches the risk.
