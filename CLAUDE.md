# Shaktra — Claude Code Plugin

Shaktra is an opinionated software development framework distributed as a Claude Code plugin. It orchestrates specialized AI agents through agile-inspired workflows to produce industry-standard, reliable, production code.

## How We Work on This Project

This is a **collaborative build**. For every aspect of Shaktra:

1. **Reference Forge first** — Before building any component, review the corresponding Forge implementation at `~/workspace/applications/forge-claudify`. Understand what exists, what worked, what didn't.
2. **Discuss before implementing** — Present findings, propose the Shaktra approach, discuss tradeoffs. No implementation until we've aligned on the approach.
3. **Implement after agreement** — Only after discussion, build the component following the agreed design.
4. **Validate against constraints** — Check every deliverable against the design constraints below.

## Starting a Phase

When the user says "work on Phase X" or "let's start Phase X":

1. **Read** `docs/shaktra-plan/high-level.md` — architecture and philosophy context
2. **Read** `docs/shaktra-plan/architecture-overview.md` — plugin structure, components, constraints
3. **Read** `docs/shaktra-plan/phases/phase-XX-*.md` — the specific phase file
4. **Read each Forge file** listed in the phase's Forge Reference table (at `~/workspace/applications/forge-claudify`)
5. **Present** — what Forge does, what Shaktra should do differently, proposed approach
6. **Wait for approval** — no implementation until we've aligned
7. **Validate** — after implementation, check the phase's Validation list AND `docs/shaktra-plan/appendices.md` (Appendix A anti-patterns)

For Forge analysis reference: `docs/Forge-analysis/analysis-report.md`
For phase index and dependency graph: `docs/shaktra-plan/execution-plan.md`

## Plugin Structure

This is a **Claude Code plugin** (NOT a regular project). The directory layout follows the plugin spec:

```
.claude-plugin/plugin.json    # Plugin manifest (required)
agents/                        # Sub-agent definitions (at root, NOT inside .claude/)
skills/                        # Skill definitions (at root, NOT inside .claude/)
hooks/hooks.json               # Hook configurations
scripts/                       # Hook implementation scripts (Python)
templates/                     # State file templates for /shaktra:init
```

Skills are namespaced as `/shaktra:skill-name` when installed by users.

## Key Design Decisions

These were explicitly chosen and must not be overridden:

- **Full persona descriptions** for all agents (detailed experience-based identity)
- **Full sprint planning** with velocity tracking and capacity planning
- **SW Quality and Code Reviewer are separate** — SW Quality checks story-level during TDD, Code Reviewer checks app-level after completion and reviews PRs
- **Quality depth must match or exceed Forge** — we reduce bloat, not capability
- **Plugin distribution** via `/plugin install shaktra` (marketplace.json at `.claude-plugin/marketplace.json`)

## Design Constraints

Check every file against these before considering any phase complete:

- No single file over 300 lines
- No content duplication across layers (skill defines, agent references — never both)
- No dead code, disabled stubs, or orphaned files
- Severity taxonomy (P0-P3) defined in exactly ONE file: `skills/shaktra-reference/severity-taxonomy.md`
- All threshold values read from `.shaktra/settings.yml` — never hardcoded
- All hook scripts in Python (cross-platform, no `grep -oP`)
- Hooks block or don't exist — no warn-only
- No always-on rules consuming context every turn
- No ASCII art in agent/skill prompts
- No naming ambiguity between components

## Git Conventions

- **Never** include a `Co-Authored-By` line in commit messages

## Component Overview

**5 Main Agent Skills:** `/shaktra:tpm`, `/shaktra:dev`, `/shaktra:review`, `/shaktra:analyze`, `/shaktra:general`
**3 Utility Skills:** `/shaktra:init`, `/shaktra:doctor`, `/shaktra:workflow`
**4 Internal Skills:** shaktra-quality, shaktra-tdd, shaktra-reference, shaktra-stories
**11 Sub-Agents:** architect, tpm-quality, scrummaster, product-manager, sw-engineer, test-agent, developer, sw-quality, cba-analyzer, cr-analyzer, memory-curator
**4 Hooks:** block-main-branch, check-p0, validate-story-scope, validate-schema
