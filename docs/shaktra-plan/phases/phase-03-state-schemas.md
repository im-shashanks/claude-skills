# Phase 3 — State Management Schemas

> **Context Required:** Read [architecture-overview.md](../architecture-overview.md) before starting.
> **Depends on:** Phase 2 (Reference System) — schemas reference severity taxonomy and tier definitions.
> **Blocks:** Phases 4, 5, 6, 9

---

## Objective

Define all state file schemas that agents produce and consume. These schemas are the contracts between components — changing them requires updating all consumers. Also delivers the memory curator agent (shared across all workflows).

## Deliverables

| File | Lines | Purpose |
|------|-------|---------|
| `skills/shaktra-reference/schemas/handoff-schema.md` | ~90 | Per-story TDD state machine |
| `skills/shaktra-reference/schemas/story-schema.md` | ~100 | Story YAML format by tier |
| `skills/shaktra-reference/schemas/settings-schema.md` | ~40 | Framework settings format |
| `skills/shaktra-reference/schemas/decisions-schema.md` | ~40 | Decisions log format |
| `skills/shaktra-reference/schemas/lessons-schema.md` | ~30 | Lessons learned format |
| `skills/shaktra-reference/schemas/sprint-schema.md` | ~50 | Sprint planning format |
| `skills/shaktra-reference/schemas/design-doc-schema.md` | ~60 | Design document structure |
| `agents/shaktra-memory-curator.md` | ~60 | Memory curator agent (shared across all workflows) |

## File Content Outlines

**handoff-schema.md (critical — the TDD state machine):**

```yaml
# Handoff State File: .shaktra/.tmp/{story-id}/handoff.yml
story_id: "ST-001"
tier: trivial | small | medium | large  # Detected or assigned
current_phase: plan | tests | code | quality | complete | failed
completed_phases: []                  # Append-only list

plan_summary:                         # Written by sw-engineer
  components: []                      # List of components with SRP
  test_plan:
    test_count: 0
    test_types: []                    # unit, integration, contract
    mocks_needed: []
    edge_cases: []
  implementation_order: []            # File sequence for implementation
  patterns_applied: []                # Quality principles applied
  scope_risks: []                     # Pre-identified pitfalls

test_summary:                         # Written by test-agent
  all_tests_red: false                # Guard: must be true before GREEN
  test_count: 0
  test_files: []

code_summary:                         # Written by developer
  all_tests_green: false              # Guard: must be true to complete
  coverage: 0                         # Percentage
  files_modified: []

important_decisions: []               # Captured during development
quality_findings: []                  # Latest quality gate results
memory_captured: false                # Guard: must be true before marking complete

# Phase transition rules:
# plan -> tests: requires plan_summary populated
# tests -> code: requires test_summary.all_tests_red == true
# code -> quality: requires code_summary.all_tests_green == true
# quality -> complete: requires no P0 findings AND memory_captured == true
```

**story-schema.md (tier-aware, NOT one-size-fits-all):**

Trivial tier (3 fields — minimum viable story, used for hotfix):
```yaml
id: ST-001
title: ""
description: ""
files: []
```

Small tier (5 fields):
```yaml
id: ST-001
title: ""
description: ""
scope: ""              # One of: skeleton, validation, diff, data, response,
                       #         integration, observability, coverage, perf, security, refactor
acceptance_criteria: []
files: []
```

Medium tier adds (5 more):
```yaml
interfaces: []
io_examples: []         # MUST include at least one error case
error_handling: []
test_specs:
  unit: []              # Each has function_name (exact, used by test agent)
invariants: []          # Each has test field matching a test_specs function_name
```

Large tier adds (5+ more):
```yaml
failure_modes: []       # Each has test field matching test_specs
edge_cases: []          # Categorized, each has test field
feature_flags: []       # Mandatory for large tier
concurrency: {}
resource_safety: {}
```

**Single-scope rule:** Every story has exactly ONE scope. Multi-scope features split into multiple stories with `blocked_by` fields.

**Test name contract:** All `test` fields in invariants, failure_modes, and edge_cases MUST reference an exact `function_name` from `test_specs.unit[]`.

**lessons-schema.md (minimal — only actionable content):**

```yaml
# Lessons Learned: .shaktra/memory/lessons.yml
lessons:
  - id: L-001
    date: "2025-01-15"
    source: ST-001                # Story ID or workflow name (e.g., "tpm", "review")
    insight: "SQLite WAL mode requires all connections closed before schema migration"
    action: "Always close connection pool before running migrations"
```

5 fields per entry. No ceremony — the memory curator determines what clears the bar: "Would this materially change how a future workflow step executes?" If not, don't capture it. Max 100 entries; when full, oldest entries are archived (moved to `lessons-archive.yml`).

**decisions-schema.md (ported from Forge — good design, keep as-is):**

```yaml
# Architectural Decisions: .shaktra/memory/decisions.yml
decisions:
  - id: ID-001
    story_id: ST-001
    title: "Email validation timeout strategy"
    summary: "DNS lookups must timeout after 5s with graceful degradation"
    categories: [reliability, performance]    # 1-3 from allowed list
    guidance:                                 # 1-5 actionable rules
      - "DNS lookups MUST have 5s timeout"
      - "On timeout, accept email but flag for async verification"
    status: active                            # active | superseded
    supersedes: null                          # ID of superseded decision, if any
    created: "2025-01-15T10:00:00Z"
```

Allowed categories (14): correctness, reliability, performance, security, maintainability, testability, observability, scalability, compatibility, accessibility, usability, cost, compliance, consistency.

Lifecycle: CAPTURE (during TDD, stored in handoff) → CONSOLIDATE (sw-quality promotes to decisions.yml) → APPLY (future stories read at start) → SUPERSEDE (new decision replaces old, append-only, never delete).

**sprint-schema.md:**

```yaml
# Sprint Planning: .shaktra/memory/sprints.yml
current_sprint:
  id: sprint-3
  start_date: "2025-01-15"
  end_date: "2025-01-29"
  stories: [ST-005, ST-006, ST-007]       # Allocated story IDs
  capacity_points: 15                      # Team capacity for this sprint
  committed_points: 13                     # Sum of allocated story points

velocity:
  history:                                  # Last N sprints for velocity calculation
    - sprint_id: sprint-2
      planned_points: 15
      completed_points: 12
      completion_rate: 0.80
    - sprint_id: sprint-1
      planned_points: 10
      completed_points: 10
      completion_rate: 1.0
  average: 11                               # Rolling average of completed points
  trend: improving                          # improving | stable | declining

backlog:                                    # Unallocated stories
  - story_id: ST-008
    points: 5
    priority: high
    blocked_by: [ST-006]
```

**design-doc-schema.md:**

```yaml
# Design Document: .shaktra/designs/{feature-name}.md
# Sections scale by project complexity (not all always present)

# Core (always present):
#   - Overview: Problem statement, goals, non-goals
#   - Contract Specs: API signatures, input/output contracts
#   - Error Taxonomy: Error types, handling strategy, user-facing messages
#   - State Machines: State transitions, guards, side effects
#   - Data Model: Schema definitions, relationships, constraints
#   - Dependencies: External services, libraries, internal modules
#   - Test Strategy: Test types needed, coverage approach

# Extended (medium+ projects):
#   - Threat Model: Attack surface, mitigations
#   - Invariants: System-wide guarantees that must hold
#   - Observability: Logging, metrics, alerting plan
#   - ADRs: Architecture Decision Records for key choices

# Advanced (large projects):
#   - Failure Modes: What can go wrong, blast radius, recovery
#   - Concurrency: Race conditions, locking strategy
#   - Resource Safety: Connection pools, file handles, memory bounds
#   - Edge Case Matrix: Boundary conditions enumerated
```

Format is Markdown (not YAML) — the schema describes expected sections by complexity tier. tpm-quality reviews against this structure.

**shaktra-memory-curator.md (agent — shared across all workflows):**

- **Role:** Extract actionable insights from workflow sessions and persist to lessons.yml
- **Skills loaded:** `shaktra-reference` (for context on quality dimensions and severity)
- **Tools:** Read, Write, Glob
- **Model:** haiku (lightweight — fast extraction task, not deep analysis)
- **Input contract:** Workflow type (dev | tpm | review | analyze), session artifacts path
- **Capture bar:** "Would this materially change how a future workflow step executes?" Zero entries is valid.
- **Process:**
  1. Read workflow artifacts (handoff.yml for dev, design docs for tpm, findings for review/analyze)
  2. Read existing lessons.yml to check for duplicates and near-duplicates
  3. Identify insights that are: (a) actionable, (b) reusable across stories, (c) not already captured
  4. Write new entries to lessons.yml following the schema (id, date, source, insight, action)
  5. If lessons.yml hits 100 entries, archive oldest to lessons-archive.yml
- **Critical rules:**
  - Never capture routine operations (tests passing normally, standard patterns applied)
  - Never duplicate existing lessons or decisions
  - Each lesson must have a concrete `action` field — not just an observation
  - Bias toward fewer, higher-quality entries over volume
- **Note:** Decisions (architectural choices) captured separately by sw-quality during QUALITY phase. Memory curator focuses on *lessons* — gotchas, surprising behaviors, process insights.

## Validation

- [ ] Handoff schema covers all TDD phases with clear transition rules (including `memory_captured` guard)
- [ ] Story schema includes Trivial tier (3 fields) through Large tier (15+)
- [ ] Single-scope rule is documented
- [ ] Test name contract is documented
- [ ] Lessons schema is minimal (5 fields per entry, no ceremony)
- [ ] Decisions schema has lifecycle documented (CAPTURE → CONSOLIDATE → APPLY → SUPERSEDE)
- [ ] Sprint schema covers velocity tracking and backlog
- [ ] Design-doc schema scales sections by project complexity
- [ ] Memory-curator agent defined with capture bar and critical rules
- [ ] All schemas under 100 lines each
- [ ] Total lines for this phase < 450

## Forge Reference

| Forge Source | What to Port | What to Change |
|-------------|-------------|----------------|
| forge-tdd/handoff-schema.md | Phase state machine | Simplify, add tier-awareness |
| forge-plan/story-schema.md (1060 lines) | Story fields by tier | **Reduce from 1060 to ~100 lines** |
| forge/memory/important_decisions.yml | Decisions format | Keep as-is (good design) |
