# Phase 6 — Code Reviewer

> **Context Required:** Read [architecture-overview.md](../architecture-overview.md) before starting.
> **Depends on:** Phase 3 (State Schemas — for review-dimensions.md to reference quality-dimensions.md). Phase 5 (SDM) recommended but not required.
> **Blocks:** Phase 11 (Workflow Router)

---

## Objective

Build the app-level code review workflow. This is distinct from SW Quality (story-level): Code Reviewer examines how code fits the overall application, reviews PRs, and generates independent test scenarios.

## Deliverables

| File | Lines | Purpose |
|------|-------|---------|
| `skills/shaktra-review/SKILL.md` | ~200 | Code review orchestrator |
| `skills/shaktra-review/review-dimensions.md` | ~150 | App-level review template (references quality-dimensions.md, applies app-level lens) |
| `agents/shaktra-cr-analyzer.md` | ~80 | Review dimension executor |

## Workflow

```
User: /shaktra:review "Review story ST-001"
  OR: /shaktra:review "Review PR #42"

Review Skill (main thread):
  1. Read project context (.shaktra/memory/decisions.yml, .shaktra/memory/lessons.yml)
  2. Determine mode: story-review | pr-review
  3. For story-review:
     a. Load story spec + all changed files
     b. Load application context (architecture, existing patterns)
     c. Spawn CR Analyzer agents in parallel for different dimension groups
     d. Aggregate findings
     e. Generate independent test scenarios (not from story spec)
  4. For pr-review:
     a. Load PR diff via `gh pr diff`
     b. Load PR context (description, comments)
     c. Spawn CR Analyzer agents for relevant dimensions
     d. Aggregate and format review
  5. Produce structured review report with P0-P3 severity
  6. MEMORY CAPTURE (mandatory final step):
     a. Spawn shaktra-memory-curator
        - Reviews review findings (architectural observations, cross-cutting concerns)
        - Evaluates: "Would this materially change future workflow execution?"
        - Writes actionable insights to .shaktra/memory/lessons.yml (if any)
  7. Report review summary to user
```

## Dimensions Relationship

Three "dimensions" files exist in the framework. They serve different purposes and are NOT duplicated:

| File | Location | Purpose | Lens |
|------|----------|---------|------|
| `quality-dimensions.md` | shaktra-reference (Phase 2) | 13 canonical dimensions (A-M) | Definition — what each dimension IS |
| `review-dimensions.md` | shaktra-review (Phase 6) | App-level review template | Application — how to apply dimensions when reviewing code in context of the full application |
| `analysis-dimensions.md` | shaktra-analyze (Phase 7) | Brownfield analysis framework | Discovery — 6 analysis areas for understanding an existing codebase |

`review-dimensions.md` **references** `quality-dimensions.md` and adds app-level context (architecture fit, cross-cutting concerns, integration). `analysis-dimensions.md` uses a different categorization because brownfield analysis serves a fundamentally different purpose than quality review.

## Key Distinction: SW Quality vs Code Reviewer

| Aspect | SW Quality (Phase 5) | Code Reviewer (Phase 6) |
|--------|---------------------|------------------------|
| **Scope** | Story-level: does implementation match story spec? | App-level: does this fit the overall application? |
| **When** | During TDD phases (plan, test, code gates) | After story completion or for PR review |
| **Focus** | Spec compliance, TDD quality, check adherence | Integration, architecture fit, independent testing |
| **Test generation** | Verifies story's own tests are behavioral | Creates NEW test scenarios not in original spec |
| **Depth** | Quick-check (~35 checks) during gates | Comprehensive 13-dimension review |

## Validation

- [ ] Story review produces app-level findings (not just story-level)
- [ ] PR review works with `gh pr diff`
- [ ] Independent test scenarios are generated
- [ ] Parallel analyzer spawning works
- [ ] No overlap with SW Quality findings (different scope)
- [ ] Memory capture invoked as final step
- [ ] review-dimensions.md references quality-dimensions.md without duplicating content

## Forge Reference

| Forge Source | What to Port | What to Change |
|-------------|-------------|----------------|
| forge-quality agent | 13-dim review concept | App-level scope, not story-level |
| PE Review (final-review) | Independent verification testing | Keep concept, drop LLM self-critique format |
