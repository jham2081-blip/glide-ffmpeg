# Pre-Merge Checklist

Run when a change is ready to merge. Every item is a yes/no with evidence. A "no" is either fixed or explicitly accepted in the change description — never silently passed.

## Correctness

- [ ] **New behavior is tested.** Each behavior this change introduces has a test that fails without the change. *(from [testing](../skills/testing.md))*
- [ ] **Failure paths are handled and tested.** Bad input, missing dependencies, and partial failure do something deliberate — not something accidental. *(from [testing](../skills/testing.md))*
- [ ] **The affected flow was exercised end-to-end** and observed working — not just unit tests. *(from [implementing-changes](../skills/implementing-changes.md))*
- [ ] **The full relevant suite passes deterministically.** No skipped tests or weakened assertions introduced to get to green.

## Completeness

- [ ] **All references swept.** Call sites, configuration, fixtures, and generated artifacts consistent with the change — the bug outside the diff is the common one. *(from [code-review](../skills/code-review.md))*
- [ ] **Documentation synchronized.** Any doc, help text, or comment this change invalidates is updated or deleted in this change. *(from [writing-documentation](../skills/writing-documentation.md))*
- [ ] **New failure modes are observable.** Anything this change can newly do wrong leaves a diagnosable record. *(from [building-observable-systems](../skills/building-observable-systems.md))*

## Scope and Decisions

- [ ] **The diff matches the stated intent.** No unrelated refactoring, no surprise scope; adjacent problems recorded, not absorbed. *(from [implementing-changes](../skills/implementing-changes.md))*
- [ ] **Hard-to-reverse elements are surfaced.** New dependencies, interface changes, data-format changes are named in the description — with a [decision record](../templates/DECISION_RECORD.md) where warranted. *(from [decision framework](../doctrine/DECISION_FRAMEWORK.md))*
- [ ] **Known shortcuts are recorded** as debt items, in or linked from this change. *(from [managing-technical-debt](../skills/managing-technical-debt.md))*

## Honesty

- [ ] **The description matches reality.** What changed, how it was verified, what remains — with no claims the evidence doesn't support. *(from [AI collaboration](../doctrine/AI_COLLABORATION.md))*
- [ ] **You reviewed your own full diff** as a reviewer would, and can justify every line in it.
