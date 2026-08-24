# 002 Git Branching, Labeling and Issue Conventions

* **Status:** Accepted
* **Date:** 2026-08-24

## Context and Problem Statement
As the codebase grows, we need consistent tracking between GitHub Issues, Git branches, and code changes to maintain and enhance clarity.

## Decision Outcome
Adopt a 1:1 mapped convention across GitHub Issue naming, Labels naming and Git Branch naming:

1. **Branch Prefixes:** Mirror primary Issue labels (`feature/`, `bug/`, `docs/` and `refactor/`).
2. **Issue Labels:** Usually **1 Type + 1 Layer** label (`domain`, `application`, `adapters` and `infrastructure`) system on issues (e.g. `type: feature` + `layer: domain`), sometimes only **1 Type** label (e.g. `docs/`).
3. **Issue Scope:** Use action-oriented titles and Markdown task lists (`- [ ]`) for sub-tasks.
4. **Main Branch Protection:** Commit baseline setups directly to `main`, but route future changes through topic branches and  pull requests (PRs) linked to GitHub Issues.

## Consequences
* **Positive:**
  * Instant mental mapping between issue tracker and terminal CLI.
  * High scannability on GitHub boards using color-coded labels.
  * Clean history with automatic issue resolution via PR keywords (`Closes #X`).
* **Negative:**
  * Requires strict adherence to naming schemes before branching.
