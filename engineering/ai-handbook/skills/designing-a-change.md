# Designing a Change

## Purpose

Turn a request into a plan worth executing: correctly scoped, built on the existing system, and verifiable. Design is where the cheapest corrections happen — a wrong plan costs minutes to fix; wrong code costs hours; wrong shipped behavior costs days.

## When To Use

- Any change bigger than a mechanical edit.
- When a request arrives as a solution ("add a cache") rather than a problem.
- When multiple implementation approaches are plausible.
- Before writing code as an AI agent, whenever the task involves more than one file or one decision.
- When work spans multiple steps, workers, specialists, providers, or side effects and the true dependencies are not obvious.

Do not force a graph-shaped design onto a small isolated task or a genuinely linear process. Explicit dependency design is useful only where the work actually branches, joins, waits on authority, or competes for shared resources.

## Principles

- **Restate the problem before accepting the solution.** Requests often arrive pre-solved, and the embedded solution skips the alternatives. Confirm what problem is being solved and how success will be observed.
- **The burden of proof is on the new thing.** Extending existing code, reusing an existing pattern, or doing nothing are the defaults. New modules, dependencies, and abstractions must justify themselves (see [Decision Framework](../doctrine/DECISION_FRAMEWORK.md)).
- **Scope is a design input, not an afterthought.** Decide explicitly what is out of scope. Adjacent problems get recorded, not absorbed.
- **Plan the verification with the change.** If you cannot say how the change will be shown to work, the design is not done.
- **Prefer designs that fail loudly.** Between two designs, choose the one whose failure modes are visible and diagnosable.
- **Model dependencies, not narration order.** A step should wait for another step only because it needs that step's data, authority, shared-resource release, or timing/readiness condition. If none applies, the edge is probably artificial.
- **Parallelism buys breadth, not truth.** Running more workers can reduce latency and widen evidence gathering, but agreement among workers does not outrank authoritative evidence, deterministic checks, or observed external results.
- **Fan-out requires explicit fan-in accounting.** A merge must know which results were expected and which were received, accepted, rejected, failed, or missing. Missing required work must never disappear inside a successful synthesis.
- **Separate evidence from execution authority.** Research, extraction, drafting, scoring, or review output may justify a proposal; it must not inherit external side-effect authority merely because it is upstream of an action.
- **Use the graph as a design, not as a framework requirement.** A dependency graph can be represented with ordinary code, queues, state machines, jobs, or functions. Introduce a graph/orchestration framework only when measured complexity justifies the dependency and operational cost.

## Workflow

1. **State the problem and the definition of done.** One or two sentences each. If you cannot, the task is not understood yet — go gather the missing context.
2. **Survey prior art in the repository.** How does this codebase already solve similar problems? The best design usually already exists locally; a design that ignores local precedent creates a second way of doing the same thing.
3. **Choose the approach.** Enumerate the plausible options (including "extend what exists"), evaluate against the doctrine's priority order, pick one, and note *why* — one paragraph is enough for most changes.
4. **Map the real dependencies when the work is multi-step.** Treat each bounded work unit as a node with a defined output. For every proposed edge, classify the reason:
   - `D` — data dependency: the downstream step consumes an upstream result;
   - `A` — authority dependency: the downstream step may proceed only after an approval, capability, or policy gate;
   - `R` — resource/exclusivity dependency: steps contend for a shared file, lock, browser profile, rate limit, device, writer, or other scarce resource;
   - `T` — timing/readiness dependency: an external system, settlement interval, freshness condition, or scheduled state must be ready first.

   If an edge has none of these reasons, mark it `FAKE` and remove it. Then identify independent fan-out, required fan-in, and the authoritative anchors that will settle disputes: tests that actually ran, provider/source facts, immutable source evidence, exact approvals, durable state, or reconciled external results. Define what happens when a required branch is missing before writing the merge logic.
5. **Slice it.** If the change is large, cut it into the smallest complete vertical slice that produces observable value, per [vertical-slice-development](vertical-slice-development.md). Plan subsequent slices only in outline.
6. **Identify the risks and the irreversibles.** Data migrations, interface changes, dependency additions, new authority, and external side effects get extra scrutiny and, if warranted, a [decision record](../templates/DECISION_RECORD.md).
7. **Write the verification plan.** Which tests will be added or extended, what manual/end-to-end check will demonstrate the behavior, what the rollback is if it goes wrong. For parallel work, include completeness/accounting checks rather than validating only successful child results.
8. **Sanity-check the plan's size.** If the plan touches many subsystems for a small stated problem, either the problem statement is wrong or the design is. Revisit before coding.

## Common Failure Modes

- **Solutioneering.** Executing the requested solution without ever surfacing the underlying problem, then discovering the solution doesn't solve it.
- **Second-system design.** Designing the general framework this change "will eventually need" instead of the change itself. Speculative generality is the most expensive form of debt.
- **Fake-edge serialization.** Running work sequentially because the plan was written in that order, even though the later step consumes nothing from the earlier one. Latency and failure coupling increase for no benefit.
- **False independence.** Parallelizing steps that secretly share a writable file, provider quota, browser session, mutable state, or other exclusive resource. The missing `R` edge reappears later as races and intermittent failures.
- **Voting as truth.** Treating agreement among several model workers or reviewers as stronger evidence than a deterministic test, authoritative source, or observed provider result.
- **Silent fan-in loss.** A reducer or synthesizer receives four of five required results and emits a polished "complete" answer anyway.
- **Context collapse.** Fan-out workers return large unbounded prose blobs that are concatenated into one overloaded synthesis context. Prefer typed/bounded outputs, layered reduction, and only the evidence the next step needs.
- **Authority laundering.** A worker's recommendation, confidence score, or successful review is silently converted into permission to write, send, publish, spend, or mutate an external system.
- **Framework-first graphing.** Installing a workflow/graph framework before the real dependency structure or operational failure modes have been demonstrated.
- **Invisible decisions.** Adding a dependency or changing a contract as a silent implementation detail. Hard-to-reverse choices must be surfaced in the plan, not buried in the diff.
- **Scope osmosis.** Each adjacent problem absorbed "while we're here" doubles review surface and halves the odds anyone can reason about the change.
- **Designing in a vacuum.** Producing a plan that conflicts with existing conventions because prior art was never surveyed.

## Success Criteria

- The plan states: problem, chosen approach and why, out-of-scope items, risks, and verification.
- A reviewer can evaluate the plan without reading any code.
- For multi-step work, every retained dependency has an explicit `D`, `A`, `R`, or `T` reason; artificial sequencing has been removed.
- Independent work can proceed independently without weakening authority or resource safety.
- Required fan-in identifies expected, received, failed, rejected, and missing work before completion can be declared.
- Authoritative anchors are explicit, and model agreement cannot override stronger evidence.
- Evidence-producing steps do not acquire external side-effect authority by position in the workflow.
- Implementation proceeds without discovering that the approach is fundamentally wrong.
- No new system, dependency, or abstraction appears in the diff that wasn't in the plan.

## Checklist

- [ ] Problem and definition of done stated in plain language
- [ ] Repository surveyed for existing patterns and prior art
- [ ] "Extend / reuse / do nothing" considered before anything new
- [ ] Out-of-scope items listed explicitly
- [ ] Multi-step dependencies classified `D | A | R | T`, with `FAKE` edges removed
- [ ] Hidden shared resources/exclusivity checked before parallelizing
- [ ] Required fan-out/fan-in and missing-result behavior defined
- [ ] Authoritative/deterministic anchors identified where judgment could disagree
- [ ] Evidence/review output kept separate from side-effect authority
- [ ] Graph/orchestration framework avoided unless real complexity justifies it
- [ ] Hard-to-reverse elements identified (decision record if warranted)
- [ ] Verification plan written (tests + observable end-to-end check)

## Related Skills

- [orienting-in-a-codebase.md](orienting-in-a-codebase.md) — the prerequisite context.
- [vertical-slice-development.md](vertical-slice-development.md) — slicing large designs.
- [testing.md](testing.md) — turning fan-in, authority, and failure assumptions into executable checks.
- [building-observable-systems.md](building-observable-systems.md) — making branch, retry, and completion state inspectable.
- [implementing-changes.md](implementing-changes.md) — executing the plan.
- [../doctrine/DECISION_FRAMEWORK.md](../doctrine/DECISION_FRAMEWORK.md) — deciding among approaches.
