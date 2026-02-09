# Shaktra

**Opinionated software development framework for Claude Code.**

Shaktra is a Claude Code plugin that orchestrates specialized AI agents through agile-inspired workflows to produce industry-standard, production-quality code.

| | |
|---|---|
| **Version** | 0.1.0 |
| **License** | MIT |
| **Plugin files** | ~60 files, ~7,000 lines |

---

## What is Shaktra?

Shaktra turns Claude Code into a full software development team. Instead of a single assistant, you get specialized agents — a TPM, architect, developer, test engineer, quality reviewer, and more — each with deep domain expertise, working together through structured workflows.

**Five pillars:**

1. **TDD-first development** — tests are written before code, always
2. **Multi-agent orchestration** — 11 specialized agents, each with a distinct role
3. **Quality gates at every phase** — P0-P3 severity taxonomy with automated enforcement
4. **Sprint-based planning** — velocity tracking, capacity allocation, backlog management
5. **Ceremony scaling** — story tiers (XS/S/M/L) determine how much process each task gets

Quality enforcement is built into the workflow, not bolted on. Every code change passes through story-level quality checks during TDD and app-level review after completion. P0 findings block merge — no exceptions.

---

## Installation

### Marketplace (recommended)

```
/plugin marketplace add https://github.com/im-shashanks/shaktra-plugin.git
/plugin install shaktra@shaktra-marketplace
```

### Direct from GitHub

```
/plugin install https://github.com/im-shashanks/shaktra-plugin.git
```

---

## Quick Start

### Greenfield project

1. **Initialize** — `/shaktra:init` to create `.shaktra/` config and project structure
2. **Plan** — `/shaktra:tpm` to create a design doc, break it into user stories, and plan your sprint
3. **Build** — `/shaktra:dev` to implement stories with TDD (red-green-refactor)
4. **Review** — `/shaktra:review` to run a comprehensive code review or review a PR

### Brownfield project

1. **Initialize** — `/shaktra:init` (select "brownfield")
2. **Analyze** — `/shaktra:analyze` to assess the existing codebase across 8 dimensions
3. **Plan and build** — same as greenfield, informed by analysis results

### Hotfix

```
/shaktra:tpm hotfix: <description of the issue>
```

Creates a hotfix story and routes directly to development.

---

## Commands

### Workflow Agents

| Command | Agent | Purpose |
|---|---|---|
| `/shaktra:tpm` | Technical Project Manager | Design docs, user stories, sprint planning, hotfixes |
| `/shaktra:dev` | Developer | TDD implementation — red, green, refactor |
| `/shaktra:review` | Code Reviewer | PR reviews, app-level quality checks |
| `/shaktra:analyze` | Analyzer | Brownfield codebase analysis (8 dimensions) |
| `/shaktra:general` | General Assistant | Domain expertise, architectural guidance, questions |

### Utility Commands

| Command | Purpose |
|---|---|
| `/shaktra:init` | Initialize Shaktra in a project (creates `.shaktra/`) |
| `/shaktra:doctor` | Diagnose framework health — plugin structure, config, constraints |
| `/shaktra:workflow` | Natural language router — describe what you need, get routed to the right agent |

---

## Architecture

Shaktra uses a layered agent system:

- **Skill layer** — user-facing commands (8 invocable skills) define the workflow and orchestrate agents
- **Agent layer** — 11 specialized sub-agents execute specific tasks (architect, developer, test engineer, etc.)
- **Reference layer** — shared constants, schemas, and quality standards (single source of truth)
- **Hook layer** — 4 blocking hooks enforce constraints at commit/push time

**Quality system:** Two distinct reviewers operate at different scopes:
- **SW Quality** checks story-level quality during TDD (after each implementation cycle)
- **Code Reviewer** checks app-level quality after completion and reviews PRs

**TDD pipeline:** Every implementation follows red-green-refactor with a structured handoff schema tracking phase transitions, test counts, and coverage.

---

## Configuration

All thresholds and settings live in `.shaktra/settings.yml` — nothing is hardcoded in the plugin.

| Section | Controls |
|---|---|
| `project` | Name, type (greenfield/brownfield), language, test framework, coverage tool |
| `tdd` | Coverage threshold (default: 90%), hotfix threshold (default: 70%) |
| `quality` | Max P1 findings allowed (default: 2) |
| `review` | Verification test count, persistence behavior |
| `analysis` | Summary token budget, incremental refresh toggle |
| `sprints` | Sprint duration, default velocity, tracking toggle |

---

## Design Philosophy

- **Prompt-driven, not script-driven** — agents and skills are markdown prompts, not Python scripts. The plugin leverages Claude's native tools (Glob, Read, Grep, Bash) instead of reimplementing them.
- **No file over 300 lines** — complexity stays manageable, every file has a single clear purpose.
- **Single source of truth** — severity taxonomy, quality dimensions, and schemas are defined once in the reference skill and referenced everywhere else.
- **Hooks block or don't exist** — no warn-only hooks. If a constraint matters, it's enforced.
- **Ceremony scales with complexity** — XS stories skip design docs; L stories get full architecture review. The framework adapts to the task.
- **Read-only diagnostics** — `/shaktra:doctor` reports problems but never fixes them. The user stays in control.

---

## License

MIT License. See [LICENSE](LICENSE).

---

## Development

Development happens on the [`main`](https://github.com/im-shashanks/shaktra-plugin/tree/main) branch. See the main branch for architecture docs, phase plans, and contribution guidelines.
