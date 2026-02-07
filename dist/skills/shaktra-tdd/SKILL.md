---
name: shaktra-tdd
description: >
  TDD knowledge base — testing practices, coding practices, and implementation patterns.
  Loaded by SDM workflow agents (sw-engineer, test-agent, developer) for behavioral testing
  guidance and production-grade coding standards.
user-invocable: false
---

# Shaktra TDD — Testing & Coding Knowledge

This skill provides the knowledge base for writing tests and production code. It is loaded by agents during the TDD pipeline — it does not orchestrate any workflow.

## Boundary

**This skill defines:** HOW to write tests (practices, patterns, anti-patterns) and HOW to write production code (implementation patterns, security, observability, resilience).

**shaktra-quality defines:** HOW to evaluate code and tests (checks, review dimensions, gate logic).

**shaktra-reference defines:** WHAT severity levels mean (`severity-taxonomy.md`), WHAT quality principles apply (`quality-principles.md`), and WHAT the handoff state machine looks like (`schemas/handoff-schema.md`).

This skill never restates severity definitions, quality dimensions, or schema structures — it references them.

## Sub-Files

| File | Purpose |
|---|---|
| `testing-practices.md` | 12 core testing principles — behavioral testing, TDD cycle, isolation, mocking, edge cases |
| `coding-practices.md` | Implementation patterns, error handling, security, observability, resilience essentials |

## How Agents Use This Skill

**sw-engineer** loads this skill to inform implementation and test planning:
- Reads `testing-practices.md` for test strategy guidance
- Reads `coding-practices.md` for pattern selection during plan creation

**test-agent** loads this skill to write behavioral tests:
- Follows `testing-practices.md` for test structure, naming, assertions
- References edge case strategy and mocking boundaries

**developer** loads this skill to write production code:
- Follows `coding-practices.md` for implementation patterns
- Applies security, observability, and resilience essentials

## References

- `shaktra-reference/quality-principles.md` — 10 core principles guiding all code
- `shaktra-reference/severity-taxonomy.md` — severity definitions (never duplicated here)
- `shaktra-reference/schemas/handoff-schema.md` — TDD state machine phases
