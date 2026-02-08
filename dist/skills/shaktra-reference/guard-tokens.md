# Guard Tokens

15 core workflow tokens used for signaling across Shaktra agents. Tokens are emitted as plain text markers in agent output. Domain-specific skills define additional tokens (review: 4, analyze: 3, general: 3) in their respective SKILL.md files.

## Phase Progression

| Token | When Emitted | Emitter | What Happens Next |
|---|---|---|---|
| `TESTS_NOT_RED` | Test suite does not have a failing test before implementation begins | Orchestrator, Test Agent | Block implementation — write a failing test first |
| `TESTS_NOT_GREEN` | Implementation complete but tests still failing | Developer | Return to implementation — fix until tests pass |
| `PHASE_GATE_FAILED` | A TDD phase transition check failed (red/green/refactor) | SW Quality | Block phase transition — resolve the failure |
| `COVERAGE_GATE_FAILED` | Coverage falls below the tier's required threshold | Developer, SW Quality | Block completion — add tests to meet threshold |

## Quality Gates

| Token | When Emitted | Emitter | What Happens Next |
|---|---|---|---|
| `CHECK_PASSED` | A quality check passed during development | SW Quality | Continue to next check or phase |
| `CHECK_BLOCKED` | A quality check failed during the TDD fix loop | SW Quality | Return to fix loop — address the finding |
| `QUALITY_PASS` | Quality gate passed (0 P0, P1 within threshold) | SW Quality, TPM Quality | Proceed to next phase or allow merge |
| `QUALITY_BLOCKED` | Quality gate failed (P0 exists or P1 exceeds threshold) | SW Quality, TPM Quality | Block — resolve findings first |

## Workflow

| Token | When Emitted | Emitter | What Happens Next |
|---|---|---|---|
| `STORY_COMPLETE` | All acceptance criteria met, all gates passed | SW Quality | Mark story done, update sprint state |
| `STORY_FAILED` | Story cannot be completed (blocker, scope issue, infeasible) | Developer | Escalate to TPM for re-planning |
| `WORKFLOW_STEP_SKIPPED` | A workflow step was intentionally skipped (e.g., tier allows it) | Any Agent | Log reason and continue to next step |
| `MAX_LOOPS_REACHED` | A fix/retry loop hit its iteration cap without resolution | Any Agent | Stop loop, escalate to user with findings |

## Communication

| Token | When Emitted | Emitter | What Happens Next |
|---|---|---|---|
| `GAPS_FOUND` | Story or design has gaps that must be filled before work begins | Architect, TPM Quality | Return to planning — fill gaps before proceeding |
| `CLARIFICATION_NEEDED` | Ambiguity that cannot be resolved from available context | Any Agent | Ask user for clarification |
| `VALIDATION_FAILED` | Schema or state file validation failed | Any Agent | Report invalid fields, block until corrected |
