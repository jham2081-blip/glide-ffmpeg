# AI Collaboration

How humans and AI agents should work together on software. This document is written for both parties: it tells agents how to behave as engineers, and it tells humans what to expect and demand from agents.

It is vendor neutral and model neutral. It applies to any AI coding agent, current or future.

---

## The Core Stance

An AI agent working in a codebase is a **new engineer with excellent recall and no tenure**. It can read fast and write fast, but it starts every session without the accumulated context a human teammate carries. Everything in this document follows from that asymmetry:

- The agent must **rebuild context deliberately** before acting (see [orienting-in-a-codebase](../skills/orienting-in-a-codebase.md)).
- The repository must **externalize context** so it can be rebuilt — through documentation, tests, decision records, and structure. A repo that lives in one person's head is hostile to agents and to future humans alike.
- Trust is earned through **verifiable work**, not confident prose. Claims must come with evidence: test output, diffs, measurements.

## Principles for Agents

### 1. Speed is not the bottleneck — judgment is

An agent can produce more code per hour than any human. That makes *restraint* the scarce skill. Unrequested refactors, speculative abstractions, and drive-by "improvements" multiply review burden faster than they add value. Solve the problem asked, completely, and stop.

### 2. Say what you did, exactly

Report outcomes faithfully. If tests fail, say so and show the output. If a step was skipped, say so. If a fix is a guess, label it a guess. An agent that shades its reports poisons the collaboration, because the human must then re-verify everything — erasing the productivity the agent exists to provide.

### 3. Prefer evidence to plausibility

Language models generate plausible text by default. Engineering requires *true* text. Before asserting how a system behaves: run it, read it, or test it. Before claiming a fix works: exercise the fixed path and observe the result. "This should work" is a hypothesis, not a conclusion.

### 4. Escalate decisions, not tasks

Handle everything within the stated scope autonomously, including errors and missing information that can be gathered. Escalate to the human only what is genuinely theirs to decide: irreversible actions, scope changes, tradeoffs the requirements don't resolve. When escalating, bring options and a recommendation, not a blank question.

### 5. Leave the campsite better documented

Every session ends and the agent's working memory ends with it. Anything discovered that future contributors need — a surprising constraint, a decision made, a debt identified — must be written down in the repository before the session ends, or it is lost. See [project-handoff](../skills/project-handoff.md).

## Principles for Humans

### 1. Give problems, not keystrokes

Agents perform best with a clear problem statement, constraints, and definition of done — and freedom in the middle. Over-specified instructions produce compliance; well-specified goals produce engineering.

### 2. Make the task contract inspectable

A strong request gives the agent enough evidence to work and enough criteria to know when it is done without dictating the implementation. Include the pieces that materially constrain the result:

- **Outcome:** the observable result you want.
- **Constraints and exclusions:** compatibility requirements, boundaries, and what must not change.
- **Source artifacts:** the actual error, log, screenshot, diff, issue, data file, or plan when one exists; direct evidence is better than a retelling.
- **Reference patterns:** an existing implementation, test, document, or convention worth matching.
- **Measurable completion:** a threshold, expected behavior, or verification command when success can be stated objectively.
- **Deliverable shape:** the format, audience, or level of detail when it changes how the result will be used.

Do not add detail merely to make the prompt longer. If a constraint does not change the work, leave it out. If the repository can discover a file path or implementation detail safely, prefer stating the outcome over prescribing the route.

### 3. Review the decision, not just the diff

Agent-written code reads clean at a glance. The risk concentrates in the decisions embedded in it: a new dependency, a changed interface, a silent assumption. Review agent work with [code-review](../skills/code-review.md) discipline: verify behavior, and interrogate the choices.

### 4. Invest in the repository, not in prompt folklore

If an agent keeps making the same mistake, the durable fix is rarely a longer prompt. It is a clearer repository: a test that catches the mistake, a document that states the constraint, a lint rule that enforces it. Fixes installed in the repo work for every agent and every human; fixes installed in a prompt work for one tool until it changes.

When a task pattern proves repeatedly useful, promote it from chat history into the repository's reusable skill, checklist, template, or thin activation prompt. When a correction reflects a project-specific invariant, record it in the project's canonical agent guidance or enforce it mechanically. Repeated rediscovery is a documentation defect.

### 5. Keep the human accountable

The human merging the change owns the change. "The agent wrote it" is not a provenance that survives an incident review. Scale your verification to the blast radius of the change.

## Where AI Belongs in a System

Distinct from *collaborating with* agents: deciding where AI-powered behavior belongs *inside* the software you build.

- Prefer deterministic solutions wherever a rule can be written down ([doctrine §2](ENGINEERING_DOCTRINE.md#2-prefer-deterministic-solutions)).
- Use AI where judgment over unstructured input genuinely adds value — and wrap it in deterministic validation, logging, and fallbacks.
- Never let probabilistic components fail silently. Make their confidence, inputs, and outputs observable.

## Related

- [ENGINEERING_DOCTRINE.md](ENGINEERING_DOCTRINE.md) — the principles both parties are upholding.
- [skills/orienting-in-a-codebase.md](../skills/orienting-in-a-codebase.md) — how an agent rebuilds context.
- [skills/project-handoff.md](../skills/project-handoff.md) — how context survives the end of a session.
- [templates/AGENTS_TEMPLATE.md](../templates/AGENTS_TEMPLATE.md) — installing agent guidance in a project.
