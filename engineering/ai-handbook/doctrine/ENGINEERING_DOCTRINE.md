# Engineering Doctrine

This repository captures engineering practices that have proven valuable across multiple software projects.

Its purpose is not to teach an AI how to write code.

Its purpose is to teach an AI how to engineer software.

The principles in this document should guide every Skill, Checklist, Template, Prompt, and Example contained in this repository.

---

## Engineering Priorities

When engineering decisions involve tradeoffs, prefer the option that best satisfies the following priorities, in order:

1. Correctness
2. Simplicity
3. Maintainability
4. Observability
5. Determinism
6. Performance

Performance optimizations should not reduce correctness, maintainability, or observability without compelling evidence.

Cleverness is deliberately absent from the list: clever solutions are valuable only when they also improve simplicity — otherwise they are a cost dressed as an achievement.

---

## Core Principles

## 1. Extend Before Creating

Prefer extending existing systems before introducing new ones.

Every new engine, abstraction, workflow, or dependency increases long-term maintenance cost.

Build new systems only when extending existing ones would clearly make the software worse.

---

## 2. Prefer Deterministic Solutions

Use deterministic solutions whenever they can reasonably solve the problem.

Rules, schemas, validation, measurements, and reproducible processes should be preferred over probabilistic reasoning whenever practical.

Use AI where judgment creates value—not where deterministic software is sufficient.

---

## 3. Evidence Before Automation

Do not automate assumptions.

Collect examples.

Measure reality.

Understand failure modes.

Only then automate.

---

## 4. Build the Smallest Complete Vertical Slice

Prefer complete, end-to-end slices over partially implemented architectures.

A working slice teaches more than an unfinished framework.

Avoid building infrastructure for hypothetical future needs.

---

## 5. Optimize for Maintainability

Software will be modified far more often than it will be written.

Prefer designs that are:

- understandable
- testable
- observable
- maintainable

Avoid cleverness that reduces clarity.

---

## 6. Make Systems Observable

A system that cannot explain what it is doing cannot be trusted.

Prefer:

- explicit outputs
- measurable behavior
- diagnostics
- ledgers
- reports
- validation

Hidden behavior should be minimized.

---

## 7. Preserve Evidence

Whenever practical:

- preserve measurements
- preserve artifacts
- preserve decision history

Prefer append-only records over destructive updates.

Evidence is often more valuable than conclusions.

---

## 8. Separate Measurement from Interpretation

Measurement should describe reality.

Interpretation should explain reality.

Recommendations should remain separate from both.

Mixing these responsibilities makes systems difficult to validate and improve.

---

## 9. Keep Documentation Synchronized

Implementation, tests, and documentation should evolve together.

Documentation should describe reality rather than aspiration.

Outdated documentation is worse than missing documentation.

---

## 10. Design for Future Humans and Future AI

Assume future contributors know nothing about the project.

Software should explain itself through:

- organization
- naming
- documentation
- diagnostics
- tests

Every improvement should make the project easier—not harder—to understand.

---

## 11. Make Failures Explicit

Failures should be visible.

Systems should fail clearly rather than silently producing misleading results.

Operators should understand:

- what failed
- why it failed
- what to do next

---

## 12. Avoid Unnecessary Abstraction

Do not introduce abstraction before there is demonstrated need.

Prefer concrete implementations until recurring patterns justify extraction.

Abstraction should reduce complexity—not create it.

---

## 13. Respect Scope

Solve the problem being addressed.

Avoid unrelated refactoring.

Avoid expanding project scope without explicit justification.

Small, focused changes are easier to review, test, and maintain.

---

## 14. Build for Operators

Good engineering considers the people operating the software.

Prefer:

- clear CLI interfaces
- informative output
- predictable behavior
- safe defaults
- useful diagnostics

A good operator experience improves reliability.

---

## Applying the Doctrine

- When principles conflict on a concrete decision, use the [Decision Framework](DECISION_FRAMEWORK.md).
- Each principle is put into practice by one or more [Skills](../skills/README.md): the doctrine states *what to value*; the skills show *how*.
- Evolution rules for this document are in the [doctrine README](README.md#evolution): changes are rare, deliberate, and must reflect practice proven across multiple projects.