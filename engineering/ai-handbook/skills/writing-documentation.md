# Writing Documentation

## Purpose

Produce documentation that stays true and gets used. Documentation is the interface to a system for everyone who can't (or shouldn't have to) read all the code — future maintainers, operators, and AI agents rebuilding context from zero. Its two failure modes are absence and lies; lies are worse.

## When To Use

- In the same change as any behavior, interface, or workflow modification (sync is a property of the change, not a follow-up).
- When the same question gets asked (or investigated) twice — the second occurrence is the signal to write it down.
- When designing what to document for a new project or component.
- When deciding what *not* to write — every page created is a page to keep true.

## Principles

- **Documentation describes reality, not aspiration.** It documents what the system does today. Plans and wishes belong in issues and design docs, clearly labeled as such. A reader must never have to guess which parts are real.
- **Wrong documentation is worse than none.** Missing docs send the reader to the code, which is slow but truthful. Wrong docs send the reader confidently in the wrong direction. This asymmetry drives everything: write less, keep it true.
- **Write for the reader's moment, and say which moment.** Orientation ("what is this?"), task ("how do I do X?"), reference ("what are the exact options?"), and rationale ("why is it this way?") are different documents. A page that mixes them serves none of them.
- **Closer to the code is truer.** Ordered by durability: code and names, then tests, then comments, then in-repo docs, then external wikis. Push each fact to the truest medium that can hold it — and prefer making the system self-explanatory over documenting its confusion.
- **Comments carry what code cannot.** A comment earns its place by stating a *why* or a constraint invisible in the code — not by narrating what the next line does. Narration comments rot fastest and are read least.
- **Every document needs an owner-moment for truth-checking.** Docs stay synchronized only if some step forces the question "did this change invalidate any docs?" That step is the change itself — grep for references to what you changed.

## Workflow

1. **Choose the reader and the moment.** Who is reading, what are they trying to do, what do they already know? A README for a new contributor and a runbook for a 3 a.m. operator share no assumptions.
2. **Pick the smallest true form.** Can the fact live in a name? A type? A test? An error message? Only what remains needs prose. (A great error message is documentation delivered at the perfect moment.)
3. **Structure for the impatient.** Lead with what the thing is and the most common task. Make it skimmable: headings that answer questions, examples that actually run, links instead of repetition — every duplicated fact is a future contradiction.
4. **Show, verify, then explain.** Working examples first, prose second. Any command or snippet in the doc gets run before it's committed; untested examples are pre-rotted.
5. **Wire it into the graph.** Link from where readers will be when they need it (the README index, the code near the behavior, the error message). An unfindable doc has the same value as an unwritten one, minus the maintenance.
6. **On every code change: sweep the docs.** Search documentation for the names, flags, commands, and behaviors your change touched. Update or delete what the change invalidated — deletion is a fully legitimate outcome.

## Common Failure Modes

- **Aspirational drift.** Docs written from the design doc rather than the implementation, describing the system that was planned instead of the one that shipped.
- **The write-only wiki.** Documentation accumulating where no change process touches it, aging silently until readers learn to distrust all of it — which defeats even the accurate parts.
- **Narration comments.** `// increment the counter` above `counter++`. Noise at birth, lie after the next edit.
- **The everything-page.** One document trying to be tutorial, reference, and rationale at once — too long to read at any of those moments.
- **Duplicated truths.** The same setup steps in three places, updated in one. Single source, linked everywhere else.
- **Documenting around a defect.** Writing a paragraph explaining confusing behavior instead of fixing the behavior. Docs are not a place to store apologies.

## Success Criteria

- A newcomer (human or agent) reaches productive work from the docs alone, without oral tradition.
- Spot-checking claims against the code finds no lies; examples run as written.
- Behavior changes and doc updates land in the same change, verifiable in history.
- Each document has one job (orient / do / look up / explain-why) and a reader could say which.

## Checklist

- [ ] Reader and moment identified; one job per document
- [ ] Facts pushed to the truest medium (names, types, tests, errors) before prose
- [ ] Examples and commands executed before committing
- [ ] Linked from where readers will actually be
- [ ] Docs swept for invalidated content on every behavior change
- [ ] No duplicated truths; links instead

## Related Skills

- [implementing-changes.md](implementing-changes.md) — doc sync as part of every change.
- [project-handoff.md](project-handoff.md) — documentation as the vehicle of handoff.
- [operator-experience.md](operator-experience.md) — error messages and runbooks as documentation.
