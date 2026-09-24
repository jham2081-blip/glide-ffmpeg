# Session-End Checklist

Run when ending a work session — especially an AI agent session, whose working context is destroyed at session end. The question behind every item: *if this session's memory vanished right now, what would be lost?* Anything valuable must already be in the repository.

Full reasoning: [project-handoff](../skills/project-handoff.md) and [AI collaboration](../doctrine/AI_COLLABORATION.md).

## Work State

- [ ] **In-flight work is in a named state**: completed, cleanly parked (committed/stashed with a written note of where it stands), or explicitly abandoned. Nothing ambiguous.
- [ ] **The working tree is intentional.** No stray debug files, half-edits, or uncommitted changes whose purpose isn't recorded.
- [ ] **Tests reflect reality.** The suite passes, or known failures are documented as known — the next session must be able to trust the baseline.

## Knowledge Capture

- [ ] **Discoveries are written down.** Surprising constraints, system behavior learned the hard way, and verified facts that contradict existing docs — recorded in the appropriate document, not left in the conversation.
- [ ] **Dead ends are recorded where expensive.** Approaches tried and abandoned, with the reason — so the next session doesn't re-run the same experiment at full price.
- [ ] **Decisions made this session are recorded** if hard to reverse. *(template: [DECISION_RECORD](../templates/DECISION_RECORD.md))*
- [ ] **Shortcuts taken are recorded as debt.** *(from [managing-technical-debt](../skills/managing-technical-debt.md))*

## Continuity

- [ ] **Next steps are written, with context**: not just what, but why it's next and what's already known about it.
- [ ] **The final report matches reality**: what was done, how it was verified, what was not done — no inflation.
