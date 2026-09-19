# Orienting in a Codebase

## Purpose

Build enough of an accurate working model to change a codebase safely without loading irrelevant context. Most bad changes come from acting on a wrong model of the system; most wasted agent context comes from reading far beyond what the task needs.

## When To Use

- Starting nontrivial work in a repository you have not worked in recently.
- Touching an unfamiliar subsystem in a familiar repository.
- Before estimating, planning, or advising where architecture or local convention matters.
- When the task's blast radius is large enough that a wrong assumption would be expensive.

For a trivial, contained edit with an obvious local precedent, orient minimally: read the governing project instructions and the affected area. Do not force the full workflow.

## Principles

- **The repository is the primary source; documentation is a map, not the territory.** Read the documentation that governs the affected area, then verify important claims against code, tests, or runtime behavior.
- **Context is a budget.** Load what the task needs. A complete repository map is not automatically better than a precise local model.
- **Orient to conventions before inventing.** Find how the project already names, structures, tests, and handles the kind of change you are making.
- **Depth proportional to blast radius.** A typo fix may need one nearby file; a schema, security, or cross-service change may need architecture, history, and end-to-end tracing.
- **Expand on evidence.** Start narrow, then widen when the code, failure, dependency graph, or uncertainty shows that the task crosses boundaries.
- **Material orientation produces an artifact.** For nontrivial work, state the model in the plan, PR, or handoff so assumptions can be checked.

## Workflow

1. **Read the governing instructions.** Start with the project's `AGENTS.md` or equivalent. Read README or contributor material when it is relevant to the requested work; do not load every top-level document by reflex.
2. **Locate the affected path and local precedent.** Find the entry point, implementation, tests, configuration, and one representative nearby pattern. Identify generated files before editing.
3. **Find the relevant commands.** Learn the build, test, lint, or run command needed to verify this change. Do not run unrelated broad checks merely as an orientation ritual.
4. **Expand only where the task crosses boundaries.** Read architecture, decision records, recent history, or additional subsystems when the change actually depends on them or when local evidence is ambiguous.
5. **Trace the risky path.** For consequential work, follow one representative flow end-to-end and identify side effects, contracts, and failure boundaries. For a contained edit, the local call path may be enough.
6. **Establish a useful baseline.** Run the smallest pre-change check that will distinguish a regression you might cause from a pre-existing failure. Broaden the baseline when risk warrants it; skip an expensive broad baseline when it adds no diagnostic value.
7. **State the working model when it matters.** Summarize where the change belongs, the conventions it must follow, the main risk, and how it will be verified.

## Common Failure Modes

- **Pattern-matching from other projects.** Assuming this repo works like the last one with a similar stack.
- **Context flooding.** Reading the whole architecture, history, and handbook before a local change, consuming time and context without changing the decision.
- **Trusting stale documentation.** Building on a doc claim without checking the implementation when the claim matters.
- **Grep-and-go.** Editing the first matching string without checking the local call path, generated copy, fixture, or configuration that encodes the same behavior.
- **Ceremonial baselining.** Running a huge suite before a tiny change even though a failure would not help localize responsibility.
- **Under-orienting a high-blast-radius change.** Treating a cross-service, schema, authorization, or persistence change like a local edit.
- **Unbounded exploration.** Continuing to map the system after the task-relevant uncertainty has already been resolved.

## Success Criteria

- You can explain where the change belongs and which local pattern it should follow.
- You know how the intended outcome will be verified.
- The amount of context gathered is proportionate to the task: no important boundary was missed, and irrelevant subsystems were not loaded by default.
- For consequential work, risky assumptions and pre-existing failures relevant to the change are known before implementation.
- Surprises during implementation are rare or trigger deliberate expansion of orientation rather than improvisation.

## Checklist

- [ ] Read the governing project instructions
- [ ] Located the affected path, tests/config, and a local precedent
- [ ] Identified generated vs. hand-written files where relevant
- [ ] Found the verification commands needed for this task
- [ ] Expanded into architecture/history/other subsystems only where evidence required it
- [ ] Established a useful baseline when regression attribution would benefit from one
- [ ] Stated the working model for nontrivial work

## Related Skills

- [designing-a-change.md](designing-a-change.md) — the next step when the task needs design.
- [testing.md](testing.md) — choosing proportionate executable verification.
- [bootstrapping-a-repository.md](bootstrapping-a-repository.md) — making a repo easy to orient in.
- [project-handoff.md](project-handoff.md) — preserving important context for the next contributor.
