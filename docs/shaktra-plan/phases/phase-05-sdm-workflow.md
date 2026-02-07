# Phase 5 — SDM Workflow & TDD Pipeline

> **Context Required:** Read [architecture-overview.md](../architecture-overview.md) before starting.
> **Depends on:** Phase 2 (Reference System), Phase 3 (State Schemas)
> **Blocks:** Phase 11 (Workflow Router)
> **Critical path phase** — this is the backbone of code quality.

---

## Objective

Build the core development workflow: Software Development Manager orchestrating TDD. Covers: planning, test writing (RED), code implementation (GREEN), and quality gates at each transition.

## Deliverables — Skills

| File | Lines | Purpose |
|------|-------|---------|
| `skills/shaktra-dev/SKILL.md` | ~250 | SDM orchestrator — TDD pipeline dispatch |
| `skills/shaktra-dev/tdd-pipeline.md` | ~200 | Step-by-step TDD orchestration template |
| `skills/shaktra-tdd/SKILL.md` | ~100 | TDD knowledge manifest |
| `skills/shaktra-tdd/testing-practices.md` | ~200 | Test writing guide, behavioral testing, patterns |
| `skills/shaktra-tdd/coding-practices.md` | ~200 | Implementation guide, patterns, anti-patterns |
| `skills/shaktra-quality/SKILL.md` | ~100 | Quality engine manifest |
| `skills/shaktra-quality/quick-check.md` | ~200 | ~35 high-impact checks for TDD gates |
| `skills/shaktra-quality/comprehensive-review.md` | ~200 | Full 13-dimension review template |

## Deliverables — Agents

| File | Lines | Purpose |
|------|-------|---------|
| `agents/shaktra-sw-engineer.md` | ~100 | Unified planning (implementation + tests) |
| `agents/shaktra-test-agent.md` | ~100 | Test writing — RED phase |
| `agents/shaktra-developer.md` | ~100 | Code implementation — GREEN phase |
| `agents/shaktra-sw-quality.md` | ~80 | SW quality review per story |

## Workflow

```
User: /shaktra:dev "Develop story ST-001"

SDM Skill (main thread):
  1. Read .shaktra/settings.yml (coverage thresholds — NEVER hardcode)
  2. Read .shaktra/stories/ST-001.yml (story spec)
  3. Read .shaktra/.tmp/ST-001/handoff.yml (if exists — for resume)
  4. Read .shaktra/memory/decisions.yml (prior decisions)
  5. Read .shaktra/memory/lessons.yml (prior lessons)

  PRE-FLIGHT CHECKS (before any TDD work):

    Language config check:
    - Verify .shaktra/settings.yml has language, test_framework, coverage_tool set
    - If missing → prompt user: "Project language config not set. Run /shaktra:init
      or update .shaktra/settings.yml with language, test_framework, coverage_tool"
    - Do not proceed until language config is present

    Story dependency check:
    - If story has blocked_by field → check if blocking stories are complete
    - If dependencies unresolved → block with: "Story ST-001 is blocked by ST-000
      (status: in_progress). Complete blocking stories first."

    Story quality guard:
    - Auto-detect tier based on story complexity and scope
    - Check: does story have all tier-required fields?
    - If sparse (missing required fields for detected tier):
      → Block TDD pipeline
      → Report to user: "Story ST-001 is sparse (X of Y required fields for [tier] tier).
         Missing: test_specs, io_examples, error_handling, ...
         Run: /shaktra:tpm enrich ST-001"
      → Exit (do not proceed with incomplete story)
    - If Trivial tier → apply hotfix_coverage_threshold from settings
    - If sufficient → proceed

  5. Detect current phase from handoff (or start fresh)

  Phase: PLAN
    a. Spawn shaktra-sw-engineer → Implementation Plan + Test Plan (unified)
       - Engineer reads story, creates comprehensive plan
       - Output: implementation_plan.md + handoff.plan_summary
    b. If tier >= Medium:
       Spawn shaktra-sw-quality → Review Plan (max 3 loops)
       - Quality: "What would bite us in production?"
       - Focus: top 3-5 critical gaps, not laundry list
    c. Update handoff: completed_phases: [plan]

  BRANCH CREATION (after PLAN, before RED):
    - Spawn shaktra-developer → Create feature branch
      - Convention: feat/{story-description} | fix/{story-description} | chore/{story-description}
      - Derived from story scope and title
      - No commits — staging only throughout TDD pipeline
      - Commits and PRs are user-managed (never automated by framework)

  Phase: RED (Tests)
    a. Spawn shaktra-test-agent → Write Failing Tests
       - MUST use exact test names from story's test_specs
       - Tests must be behavioral (assert outcomes, not mock.called)
       - All tests must fail initially (RED state)
       - Update handoff: test_summary.all_tests_red = true
    b. Spawn shaktra-sw-quality → Review Tests (max 3 loops)
       - Check: behavioral assertions, error path coverage, no over-mocking
       - Gate: P0 > 0 OR P1 > threshold = BLOCKED
    c. Update handoff: completed_phases: [plan, tests]

  Phase: GREEN (Code)
    a. Spawn shaktra-developer → Implement Code
       - Follow implementation_order from plan
       - Apply patterns from plan_summary
       - Avoid scope_risks from plan
       - Make all tests pass, hit coverage threshold
       - Update handoff: code_summary.all_tests_green = true, coverage = X%
    b. Spawn shaktra-sw-quality → Review Code (max 3 loops)
       - Quick-check mode: ~35 checks, P0/P1 focus
       - Gate: P0 > 0 OR P1 > threshold = BLOCKED
    c. Update handoff: completed_phases: [plan, tests, code]

  Phase: QUALITY (Final)
    a. Spawn shaktra-sw-quality → Comprehensive Review
       - Full 13-dimension review
       - Verification: run actual tests, check coverage
       - Decision consolidation: promote important_decisions to decisions.yml
    b. Update handoff: completed_phases: [plan, tests, code, quality]

  MEMORY CAPTURE (mandatory final step — orchestrator must not skip):
    a. Spawn shaktra-memory-curator
       - Reads handoff.yml (decisions, findings, patterns applied, scope risks)
       - Reads code changes (diff summary from files_modified)
       - Reads quality findings from comprehensive review
       - Evaluates: "Would this materially change how a future workflow step executes?"
       - Writes actionable insights to .shaktra/memory/lessons.yml (if any clear the bar)
       - Note: decisions.yml already updated during QUALITY phase (decision consolidation)
    b. Update handoff: memory_captured = true, current_phase = complete

  6. Report completion summary to user
```

## Quality Engine Design (shaktra-quality skill)

Two modes, one engine — solving Forge's quadruple overlap:

**QUICK_CHECK (during TDD gates):**
- ~35 highest-impact checks organized by severity
- Always load ALL ~35 checks regardless of tier (no tier-aware loading — risk of missing checks outweighs token savings)
- Max 3 fix loops per gate
- Focus areas by gate:
  - Plan gate: Architecture soundness, test strategy quality, missed edge cases
  - Test gate: Behavioral assertions, error path coverage, no over-mocking, test isolation
  - Code gate: Timeouts, credentials, exception handling, hallucinated imports, bounded operations

**COMPREHENSIVE REVIEW (final gate):**
- Full 13-dimension review (A-M from shaktra-reference)
- Coverage verification (actual test execution, not self-reported)
- Decision consolidation (extract decisions from development, promote to memory)
- Cross-story consistency check (does this fit with prior decisions?)

**Checks to port from Forge (highest value):**

| Check | Severity | Gate | Why It Matters |
|-------|----------|------|---------------|
| Error path coverage | P0 | Test | LLMs skip error paths entirely |
| External calls have timeouts | P0 | Code | Missing timeouts = production cascading failures |
| No hardcoded credentials | P0 | Code | Security incident if shipped |
| Bounded user input operations | P0 | Code | Prevents DoS via unbounded loops |
| Hallucinated imports | P0 | Code | LLMs invent library names |
| Missing input validation | P0 | Code | User input to eval/SQL/system calls |
| No mock-only assertions | P1 | Test | `mock.called` tests prove nothing |
| Placeholder logic | P1 | Code | TODO/NotImplementedError in critical paths |
| Generic error messages | P1 | Code | `raise Exception("Failed")` is undebuggable |
| No over-mocking | P1 | Test | Tests with 5+ mocks test nothing real |
| Test isolation | P1 | Test | Shared state = flaky suites |
| No exception swallowing | P1 | Code | `except: pass` hides real failures |
| Cyclomatic complexity | P2 | Code | Functions with 10+ branches untestable |
| Over-commenting | P2 | Code | `# Import requests` above `import requests` |
| Tests mirror implementation | P2 | Test | Tests that copy code structure break on refactor |

## Memory Curator Agent Usage

Shared across all main workflows. Agent file delivered in Phase 3; detailed usage here because SDM has the richest memory flow.

- **Capture bar:** "Would this materially change how a future workflow step executes?" Zero entries is valid.
- **Process:** Read handoff → Read existing lessons → Identify actionable, reusable, non-duplicate insights → Write to lessons.yml
- **Note:** Decisions captured separately by sw-quality during QUALITY phase. Memory curator focuses on *lessons* — gotchas, surprising behaviors, process insights.

## Validation

- [ ] Language config check blocks SDM if settings.yml missing language/test_framework
- [ ] Story dependency check blocks if blocked_by stories are incomplete
- [ ] Story quality guard catches sparse stories and blocks with actionable recommendation
- [ ] Developer creates feature branch after PLAN phase (feat/fix/chore convention)
- [ ] No automated commits — staging only
- [ ] Trivial tier stories use hotfix_coverage_threshold
- [ ] Full TDD cycle completes: plan → red (tests fail) → green (tests pass)
- [ ] Handoff state machine tracks phases correctly
- [ ] Phase resume works: stop mid-cycle, `/shaktra:dev "Resume ST-001"` continues from last phase
- [ ] Quality gates catch real issues (test with intentionally bad code)
- [ ] Coverage threshold enforcement from settings.yml (not hardcoded)
- [ ] Important decisions captured and persisted to decisions.yml
- [ ] Memory curator invoked as mandatory final step (memory_captured = true in handoff)
- [ ] Lessons.yml entries are actionable (insight + action, not just observations)
- [ ] Memory curator captures nothing for routine sessions (zero entries is valid)
- [ ] Fix loops cap at 3 per gate
- [ ] Gate activation varies by tier (Small skips plan gate) but all checks always loaded
- [ ] No content duplication between quality skill and reference skill
- [ ] All files under 300 lines (check every file)

## Forge Reference

| Forge Source | What to Port | What to Change |
|-------------|-------------|----------------|
| forge-developer agent (205 lines) | TDD phase execution, settings consumption | Split into 3 agents (engineer, test, developer) |
| forge-checker agent (329 lines) | 4 checker modes | Merge into sw-quality with modes |
| forge-quality agent (163 lines) | 13-dim review | Comprehensive mode of unified quality |
| forge-tdd skill (1142 lines) | Handoff state machine, RED/GREEN phases | **Split into testing-practices + coding-practices** |
| forge-check skill (417 lines) | Test quality, tech debt, AI slop checklists | **Merge into quick-check.md (~35 checks)** |
| forge-quality skill (88 lines) | Severity taxonomy reference | Reference shaktra-reference, don't redefine |
