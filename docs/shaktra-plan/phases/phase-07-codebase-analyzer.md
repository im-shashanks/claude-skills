# Phase 7 — Codebase Analyzer

> **Context Required:** Read [architecture-overview.md](../architecture-overview.md) before starting.
> **Depends on:** Phase 1 (Foundation). Standalone workflow — most independent phase.
> **Blocks:** Phase 11 (Workflow Router)

---

## Objective

Build the codebase analysis workflow for brownfield projects. Produces structured analysis consumed by architect agent for informed design decisions.

## Deliverables

| File | Lines | Purpose |
|------|-------|---------|
| `skills/shaktra-analyze/SKILL.md` | ~200 | Analysis orchestrator |
| `skills/shaktra-analyze/analysis-dimensions.md` | ~150 | Analysis framework (distinct from quality-dimensions — brownfield discovery lens) |
| `agents/shaktra-cba-analyzer.md` | ~80 | Analysis executor |

## Workflow

```
User: /shaktra:analyze "Analyze codebase for development readiness"

Analyze Skill (main thread):
  1. Read project context (.shaktra/memory/decisions.yml, .shaktra/memory/lessons.yml)
  2. Determine analysis scope (full | targeted dimensions)
  3. Spawn CBA Analyzer agents in parallel for different dimensions:
     - Architecture & patterns
     - Dependencies & tech stack
     - Code quality metrics
     - Test coverage & gaps
     - Security posture
     - API surface area
  4. Aggregate results into structured report
  5. Generate mermaid diagrams for key architectural connections
  6. Output to .shaktra/analysis/ directory
  7. MEMORY CAPTURE (mandatory final step):
     a. Spawn shaktra-memory-curator
        - Reviews analysis findings (patterns, risks, architecture insights)
        - Evaluates: "Would this materially change future workflow execution?"
        - Writes actionable insights to .shaktra/memory/lessons.yml (if any)
  8. Report analysis summary to user
```

## Validation

- [ ] Analysis produces structured, actionable output
- [ ] Mermaid diagrams generated for architecture
- [ ] Output consumable by architect agent (for brownfield design)
- [ ] Parallel execution works for independent dimensions
- [ ] Memory capture invoked as final step

## Forge Reference

| Forge Source | What to Port | What to Change |
|-------------|-------------|----------------|
| forge-analyzer agent | Multi-phase analysis | **Simplify from 13 sequential phases to parallel dimensions** |
| forge-analyze skill | Analysis framework | Targeted, not exhaustive |
