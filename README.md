# AI Commit Audit

A small CLI tool to **analyze human vs AI contribution over time** based on explicit Git commit tags.

This project does **not** attempt to detect AI-generated code.
Instead, it provides a reproducible way to measure collaboration between humans and AI **as declared by the author at commit time**.

> If you don’t track it while you work, you can’t measure it later.

---

## Why this exists

People increasingly claim things like:

- “90% of this code was written by AI”
- “Most of the work was done by Copilot / ChatGPT”

Honest question:
**how do you know?**

Unless contributions are tracked from day one, separating human and AI work retroactively is almost impossible.
This is not a tooling problem — it’s a methodology problem.

This project proposes:
1. A **simple commit-tagging methodology**
2. A **CLI that turns that history into data**

---

## Core idea

Git commit history is already:
- chronological
- immutable
- auditable

This tool treats commit messages as the **source of truth**, using explicit tags to indicate who produced the code in each commit.

No inference. No guessing.

---

## Supported tags (v1)

Commits are classified using one of the following tags:

- `[human]`
- `[ai]`
- `[human + ai]`

Tags are applied based on **who wrote the code**, not who had the idea.

Full definitions live in [`methodology.md`](./methodology.md).

---

## What the CLI does

Given a Git repository, the tool:

- Parses commit history
- Classifies commits by tag
- Aggregates results over time
- Outputs reproducible statistics

Example outputs include:
- total commits per category
- percentages
- monthly timelines
- machine-readable exports (JSON / CSV)

---

## What this tool is *not*

This project does **not**:

- detect AI-generated code
- count lines of code
- judge correctness or quality
- validate whether a tag is “true”
- replace human judgment

If a commit is untagged, it is **unclassified**.
No assumptions are made.

---

## Who this is for

- Developers who want to speak about AI usage with data
- Teams experimenting with AI-assisted development
- Researchers studying human–AI collaboration
- Anyone tired of vague percentages

---

## Philosophy

> Ideas belong to history.  
> Tags belong to commits.

If you care about measuring AI contribution, the cost is simple:
**you must annotate your work as you do it.**

---

## Status

This project is intentionally minimal.
The methodology comes first; tooling exists to support it.

Contributions and discussion are welcome — especially around edge cases and limitations.
