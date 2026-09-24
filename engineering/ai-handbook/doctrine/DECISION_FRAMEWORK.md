# Decision Framework

How to make engineering decisions, when to record them, and how to keep them honest.

The [Engineering Doctrine](ENGINEERING_DOCTRINE.md) defines *what to value*. This document defines *how to decide* when values conflict or when the right choice is not obvious.

---

## When a Decision Deserves a Process

Most choices do not need a framework. Apply doctrine, follow the surrounding code, move on.

Use this framework when a decision is:

- **Hard to reverse** — schema changes, public interfaces, dependencies, data formats.
- **Expensive to revisit** — anything that other code will be built on top of.
- **Contested** — reasonable engineers (or agents) would choose differently.
- **Repeated** — the same question keeps coming up, which means the answer should be written down once.

Everything else is a routine choice. Do not manufacture ceremony for routine choices.

## The Reversibility Test

Before anything else, classify the decision:

- **Reversible** (a code change undoes it): decide quickly, prefer the simplest option, and let evidence from real use correct you.
- **Hard to reverse** (data, interfaces, dependencies, published behavior): slow down, gather evidence, and record the decision.

Spending decision effort proportional to reversibility is the single highest-leverage habit in this framework.

## The Decision Process

1. **State the problem, not the solution.**
   "We need caching" is a solution. "Requests to X take 4 seconds and users abandon at 2" is a problem. Solutions smuggled in as problems skip the step where alternatives get considered.

2. **Gather evidence before opinions.**
   Measure current behavior. Read the existing code. Find how the codebase already solves similar problems. A decision made against imagined constraints will be wrong in ways that are expensive to discover later.

3. **Enumerate real options, including "do nothing."**
   At least two genuine options. "Do nothing" or "extend what exists" must be one of them — the burden of proof is always on the *new* thing.

4. **Evaluate against the priority order.**
   Correctness → Simplicity → Maintainability → Observability → Determinism → Performance. When two options tie on a higher priority, the lower priority breaks the tie — not personal preference.

5. **Decide, and state what would change your mind.**
   Every decision should name its assumptions. "We chose polling over webhooks because volume is under 100 events/day" tells a future maintainer exactly when to revisit.

6. **Record decisions that are hard to reverse.**
   Use the [decision record template](../templates/DECISION_RECORD.md). The record is for the future reader who asks "why is it like this?" — the most common and most expensive question in maintenance.

## The Dependency Test

For multi-step work, do not confuse the order in which a plan is described with the order in which the system must execute it.

A downstream step should depend on an upstream step only when at least one of these is true:

- **Data (`D`)** — it consumes the upstream result.
- **Authority (`A`)** — policy, approval, capability, or permission must be established first.
- **Resource (`R`)** — both steps contend for an exclusive/shared resource and must be coordinated.
- **Timing (`T`)** — an external readiness, freshness, settlement, or scheduling condition must hold first.

If none applies, the dependency is probably fake. Remove it rather than paying permanent latency and failure-coupling cost.

This test does not mean "parallelize everything." Hidden shared resources create real `R` dependencies; consequential actions create real `A` dependencies; simple work may remain linear because its data flow is genuinely linear.

When independent work fans out, the merge must account for the expected result set. A required child that failed or disappeared is not equivalent to an empty result. Completion is a decision about the whole required set, not merely the successful responses that arrived.

## Resolving Common Tradeoffs

| Tension | Default resolution |
|---|---|
| New abstraction vs. duplication | Duplicate until the pattern has occurred three times and its shape is stable. |
| New dependency vs. writing it yourself | Take a dependency only for problems outside your project's core domain; own your core. |
| Deterministic rule vs. AI/heuristic judgment | Deterministic wherever the rule can be written down; use judgment only where it clearly adds value. |
| General solution vs. specific solution | Solve the case in front of you completely; generalize when the second real case arrives. |
| Sequential vs. parallel work | Keep sequencing only for a real `D`, `A`, `R`, or `T` dependency. Remove fake edges; do not parallelize across hidden shared resources or authority gates. |
| Workflow/graph framework vs. ordinary code | Express the real dependency/state model first with the simplest existing mechanisms. Add a framework only when measured complexity, recovery, or observability needs justify its operational cost. |
| Multiple model judgments vs. authoritative evidence | Authoritative source facts, deterministic checks, and observed external results outrank worker agreement. Independent reviewers can challenge judgment; they do not create truth by voting. |
| Speed of delivery vs. completeness | Ship the smallest complete vertical slice — smaller in scope, never partial in depth. |
| Fixing adjacent problems vs. staying in scope | Note adjacent problems (as debt records or issues); fix only what the current change requires. |

These are defaults, not laws. Overriding a default is fine — but the override is exactly the kind of decision worth recording.

## Anti-Patterns

- **Decision by momentum.** Continuing an approach because work has already been invested in it. Sunk cost is not evidence.
- **Decision by novelty.** Choosing a technology or pattern because it is interesting. Interest is not a requirement.
- **Decision by authority quote.** "Best practice says…" without checking whether the practice's assumptions hold here.
- **Graph by fashion.** Turning ordinary sequential work into a workflow graph, or adding a graph framework, simply because graph-shaped systems are fashionable. Topology should follow real dependencies.
- **Consensus laundering.** Treating several agreeing probabilistic workers as a substitute for an authoritative source, deterministic check, or observed external result.
- **Invisible decisions.** Making a hard-to-reverse choice inside an implementation detail, where no reviewer will notice it was a choice at all. Surface it.
- **Endless deferral.** For reversible decisions, deciding slowly costs more than deciding wrong.

## Related

- [ENGINEERING_DOCTRINE.md](ENGINEERING_DOCTRINE.md) — the values this framework arbitrates between.
- [templates/DECISION_RECORD.md](../templates/DECISION_RECORD.md) — the record format.
- [examples/decision-record-example.md](../examples/decision-record-example.md) — a completed record.
- [skills/designing-a-change.md](../skills/designing-a-change.md) — applying this framework, including explicit dependency design, to a concrete change.
