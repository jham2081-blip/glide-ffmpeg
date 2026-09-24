# OpenAI GPT-6 Family Field Guide

**Status:** model-specific, non-normative  
**Last verified:** 2026-09-23  
**Models:** GPT-6 Astra, GPT-6 Sol, GPT-6 Luna  
**Use when:** an OpenAI GPT-6 model is doing substantial coding, research, browser/computer, or multi-step professional work.

This guide translates current OpenAI guidance into a practical operating playbook. The neutral engineering rules still live in the handbook's doctrine and skills. Project-specific `AGENTS.md`, contracts, security rules, and current code/tests remain authoritative for repository behavior.

## Primary sources

- GPT-6 model guidance: https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra
- Model catalog: https://developers.openai.com/api/docs/models
- GPT-6 Astra: https://developers.openai.com/api/docs/models/gpt-6-astra
- GPT-6 Sol: https://developers.openai.com/api/docs/models/gpt-6-sol
- GPT-6 Luna: https://developers.openai.com/api/docs/models/gpt-6-luna
- OpenAI developer article, "Rethinking skills and prompts for GPT-6 Astra": https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra

## Pick the model by workload

Use the family as a capability ladder, not as permanent job titles:

- **Astra (`gpt-6-astra`)** — hardest end-to-end work: ambiguous multi-step reasoning, difficult software engineering, computer/browser use, research, and professional workflows where mistakes or missed dependencies are costly.
- **Sol (`gpt-6-sol`)** — strong default for demanding coding and agentic workflows when you want a better intelligence/cost balance than Astra.
- **Luna (`gpt-6-luna`)** — efficient focused work at scale: bounded transformations, extraction, classification, repetitive tool work, and well-specified subproblems.

Benchmark representative tasks. Prefer the least expensive model that reliably meets the same acceptance criteria. Escalate when evidence shows the cheaper tier is missing important reasoning, context, or tool-work quality.

## Working mental model

GPT-6 needs less procedural scaffolding than older frontier models. Give it a clear finish line and the real constraints.

For substantial work, define:

1. **Outcome** — the observable result that should exist.
2. **Relevant context** — only the files, evidence, prior decisions, and environment facts that matter.
3. **Hard constraints** — real product, security, contract, privacy, production, or cost boundaries.
4. **Safe autonomy** — which reversible/read-only/local actions are already authorized.
5. **Definition of done** — what must be true before the model stops.
6. **Verification bar** — evidence proportionate to the blast radius.
7. **Delegation guidance** — when parallel subagents would materially save time or improve coverage.

Avoid prescribing every keystroke. Duplicate process instructions, broad skills, and stale "ask first" rules can compete with the actual task.

## Initiative and follow-through

Astra is more likely than earlier models to ask when additional input could materially change the result. That caution is useful, but it can also cause an early stop when routine details are inferable.

For authorized build/fix/change work:

- infer routine implementation details from the repository and prior context;
- treat a clear request for action as authorization to do the in-scope work, not merely to describe how it could be done;
- continue through implementation, relevant verification, inspection, and fixes needed to reach the stated completion boundary;
- do reversible, read-only, local, and review-preparation work without repeated approval when the task already authorizes it;
- ask only when the missing decision would materially change scope or outcome, or before an unauthorized destructive, external, costly, or production action;
- when a question is non-blocking, continue useful independent work first.

Astra especially benefits from an explicit completion boundary. If the desired job is "implement, run, inspect, fix, and re-verify," say that once instead of repeatedly prompting "keep going."

## Instruction hierarchy and skills

GPT-6 Astra is unusually sensitive to instruction files such as `AGENTS.md` and skills. Keep those surfaces precise.

Within higher-level platform and safety constraints:

- explicit user task instructions should outrank generic handbook or skill suggestions;
- repository-specific safety, authority, compatibility, privacy, and production rules remain hard constraints;
- skill descriptions should be short and say when the skill actually applies;
- use progressive disclosure: load a small router first and deeper workflow detail only when the task needs it;
- point to architecture/runbooks conditionally rather than forcing a full repository map before every edit;
- remove stale model-compensation rules when they no longer protect a real invariant.

If an instruction file causes a surprising permission pause or task divergence, identify the exact file/rule before adding more prompting.

## Subagents and parallel work

Astra may delegate less than desired unless the workflow says when parallelism helps. Sol and Luna are useful workers for bounded subproblems when the harness supports mixed-model delegation.

Parallelize when work separates cleanly into independent lanes with clear return artifacts, such as:

- independent repository audits;
- separate data-source checks;
- unrelated failing-test investigations;
- parallel review perspectives;
- separable implementation slices with disjoint files.

Keep authority and side effects with the root/coordinator unless explicitly delegated. At fan-in, account for expected, received, failed, and missing results before declaring completion.

Do not fan out merely to increase activity, and do not assign several agents to edit the same file unless the merge strategy is explicit.

## Testing and verification

GPT-6 Astra tends to test thoroughly. Use that strength without forcing verification theater.

Calibrate to the change:

- tiny reversible mechanical change -> targeted static/lint/render/build check may be enough;
- meaningful behavior change -> executable test at the lowest useful level;
- bug fix -> deterministic reproduction or regression test when practical;
- cross-service, identity, auth, data, or production-facing change -> broader integration/end-to-end evidence.

Once the relevant checks pass, broaden or repeat only when new changes, failures, or unresolved concerns justify it. Do not create tests that merely restate a trivial implementation.

## Writing and handoffs

GPT-6 often defaults to detailed Markdown and repeated stock phrasing. Repository instructions may specify a plainer style.

For engineering handoffs:

- state the main result early;
- use concise paragraphs and lists only when they improve scanning;
- distinguish observed facts from inference;
- report exact files changed and checks actually run;
- do not claim broader verification than the evidence supports.

## API and harness notes

Prefer the Responses API for GPT-6 tool workflows.

Model IDs:

- `gpt-6-astra`
- `gpt-6-sol`
- `gpt-6-luna`

Reasoning effort:

- Astra: `low | medium | high | xhigh | max`
- Sol/Luna: `none | low | medium | high | xhigh | max`

Important compatibility points:

- Astra tool calling requires the Responses API.
- Sol/Luna function calling in Chat Completions is supported only with `reasoning_effort: "none"`; use Responses for reasoning with tools.
- When reasoning effort is not `none`, remove `temperature`, `top_p`, and `top_logprobs`; in Chat Completions also remove `logprobs`.
- GPT-6 supports async function/custom-tool calls: mark a supported tool `async: true`, continue independent work, and later return the result with the original `call_id`.
- GPT-6 supports mid-turn steering. Send only the changed requirement; preserve completed work that still applies.
- For standard single-agent conversations that change reasoning effort, prefer a `configuration_update` item so the stable prompt prefix can remain cacheable.
- When migrating older prompt caching, use `prompt_cache_options.ttl: "30m"` instead of the older `prompt_cache_retention` parameter.

## Migration checklist from GPT-5.x / 5.6 assumptions

When upgrading a repository or agent harness:

1. Replace old model IDs/aliases with explicit GPT-6 Astra, Sol, or Luna routing.
2. If an older request used `minimal` reasoning, start with `low` and compare representative results.
3. Move reasoning + tool workflows to the Responses API.
4. Remove sampling/logprob parameters that are incompatible with active reasoning.
5. Update prompt-cache configuration.
6. Audit `AGENTS.md`, skills, prompts, and checklists for duplicated process, mandatory broad context loading, unnecessary approval pauses, and excessive test requirements.
7. Define completion boundaries so Astra does not stop at the first reviewable implementation.
8. Specify when subagents should be used; do not assume automatic fan-out.
9. Keep real domain constraints and authority boundaries intact. Model migration never grants a new side effect or production permission.

## Practical task contract

For substantial work, a compact prompt shape is usually enough:

```text
Outcome:
{{observable result}}

Context / evidence:
{{relevant issue, files, logs, prior decisions, URLs, screenshots, data}}

Constraints:
{{hard requirements and what must not change}}

Safe autonomy:
Proceed without asking for reversible, in-scope local work, including reading,
analysis, isolated edits, relevant local verification, and preparing reviewable
changes. Pause before unauthorized destructive, external, costly, production,
or materially scope-expanding actions.

Definition of done:
{{specific end state, including run/inspect/fix/re-verify if desired}}

Verification:
Use checks proportionate to the blast radius. Broaden only when failures,
dependencies, or unresolved risk justify it.

Delegation:
Parallelize independent work when it materially improves time or coverage.
Keep side-effect authority bounded and account for fan-in completeness.

Deliverable:
{{implementation / PR / report / decision memo / artifact}}
```

## Failure modes to watch

- **premature review stop** — the first plausible implementation is returned before the requested outcome is complete;
- **instruction overcompliance** — stale or broad skills cause unnecessary reading, approvals, or ceremony;
- **under-delegation** — separable work stays serial despite available subagents;
- **verification overshoot** — testing expands after sufficient evidence already exists;
- **context tax** — always-on rules crowd out the actual problem;
- **tier mismatch** — Luna is asked to solve an unusually ambiguous task without escalation, or Astra is used for routine high-volume work with no measured benefit.

The usual fix is a clearer outcome, completion boundary, routing rule, or model-selection criterion — not a longer master prompt.
