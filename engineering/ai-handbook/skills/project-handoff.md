# Project Handoff

## Purpose

Transfer a project so the next contributor — human or AI agent, next week or next year — can continue the work without the original author. A handoff is complete when the recipient can build, run, change, and ship the project using only what was handed off. Everything else is a warm goodbye, not a handoff.

## When To Use

- Leaving a project, rotating off, or pausing work for more than a few weeks.
- Ending a significant AI agent session — the agent's working context dies with the session; handoff is how its discoveries survive.
- Delivering contract or prototype work.
- Continuously, in small doses: the best handoff is a project that was always ready to be handed off.

## Principles

- **The repository is the handoff.** Knowledge that lives in your head, your chat history, or a private note transfers nothing. The test of every handoff item is: is it in the repo (or the project's canonical tracker), and would someone find it there?
- **Hand off state, not just artifacts.** Code transfers automatically; *situation* doesn't. What's in flight, what's known-broken, what was tried and abandoned (and why), what the next steps were going to be — this is the content that otherwise gets rediscovered at full price.
- **Distinguish fact from intention.** "The importer handles X" (fact, verifiable) vs. "the importer should eventually handle Y" (intention). A handoff that blurs these leaves the recipient unable to trust either.
- **Verify by cold start.** The only honest test of a handoff is executing it as the recipient would: fresh clone, follow the written steps, no access to the author. Every gap found this way is a gap found cheaply.
- **Unwritten warnings become incidents.** The known flaky test, the migration that must run in order, the third-party quirk — each unwritten warning is a trap left armed for the recipient.

## Workflow

1. **Bring the baseline to true.** README accurate, setup steps current, tests passing (or failures documented as known), build reproducible from fresh clone. Fix drift now — the recipient can't tell drift from breakage.
2. **Write the state-of-the-project note.** Short and dated, in the repo: what works today, what's in flight (and its exact state), what's known-broken, what was deliberately not done. Use the [handoff template](../templates/HANDOFF.md).
3. **Capture the "why" that isn't written yet.** Sweep decisions made along the way; any hard-to-reverse choice without a [decision record](../templates/DECISION_RECORD.md) gets one now — including roads not taken, the most valuable and least recorded knowledge.
4. **Inventory the operational surface.** Credentials and access (who grants them — never the secrets themselves), scheduled jobs, external services, deploy process, monitoring. The recipient must learn what exists before any of it pages them.
5. **List next steps with context.** Not just "do X" but why X is next, what's already known about it, and where the sharp edges are. Prioritized, honest about confidence.
6. **Cold-start test the handoff.** Fresh environment, follow only the written material, get to a running system and a shipped trivial change. Fix what snags. If a colleague or a fresh agent session can do this, the handoff works.

## Common Failure Modes

- **The heroic goodbye document.** One enormous essay written on the last day, duplicating (and contradicting) the README, unmaintained from the moment it's written. Handoff content belongs in the project's normal documents; the handoff note itself covers only *state*.
- **Happy-path handoff.** Documenting how everything works, omitting the flaky test, the manual step everyone forgets, and the reason the previous approach was abandoned. The recipient re-learns each omission as a small crisis.
- **Secrets in the handoff.** Credentials pasted into docs so "it keeps working." Hand off the *path to access*, never the keys.
- **Assumed context.** "Deploy as usual" — the words "as usual" mark exactly the knowledge that isn't transferring.
- **Handoff as event, not property.** A project that only becomes handoff-able the week someone leaves has been accumulating transfer-debt the whole time. Decision records, accurate docs, and clean setup are handoff paid in installments.
- **AI-session evaporation.** An agent ends a session with discoveries, dead ends, and half-done work living only in its context window. Anything worth keeping gets written to the repo before the session ends.

## Success Criteria

- A recipient with no author access reaches: running system, passing tests, one shipped change — using written material alone.
- Questions back to the author trend to zero after the first week (each one marks a handoff gap).
- In-flight work is either completed, cleanly parked with written state, or explicitly abandoned — nothing ambiguous.
- Six months later, "why is it like this?" has written answers.

## Checklist

- [ ] Fresh-clone setup verified; tests pass or failures documented
- [ ] State note written: works / in flight / broken / deliberately not done
- [ ] Decision records exist for hard-to-reverse choices, including roads not taken
- [ ] Operational surface inventoried (access paths, jobs, services, deploys) — no secrets in docs
- [ ] Next steps listed with rationale and known sharp edges
- [ ] Cold-start test executed by someone (or some session) other than the author

## Related Skills

- [writing-documentation.md](writing-documentation.md) — the medium of handoff.
- [orienting-in-a-codebase.md](orienting-in-a-codebase.md) — the recipient's side of the same transaction.
- [../doctrine/AI_COLLABORATION.md](../doctrine/AI_COLLABORATION.md) — session-end discipline for agents.
