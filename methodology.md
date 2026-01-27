# Human vs AI Commit Tagging Methodology

This document defines the rules used by **Who Wrote This** to classify Git commits.

The goal is not perfect attribution.
The goal is **honest, reproducible tracking over time**.

---

## Core principle

Commits are tagged based on **who produced the code in that commit**, not:

- who had the idea
- who prompted the AI
- who reviewed the output
- who pressed Enter

Only the **final code content** matters.

---

## Tags and definitions

### `[human]`

Use this tag when:

- All code in the commit was written by a human
- No AI-generated code is included
- Manual typing, refactoring, or editing only

AI may have been used for:
- discussion
- explanation
- planning
- reviewing

As long as **no AI-generated code** appears in the commit, it is `[human]`.

---

### `[ai]`

Use this tag when:

- All code in the commit was generated or modified by AI
- The human did not edit the code after generation
- Human involvement was limited to:
  - prompting
  - selecting output
  - deciding to commit

If the commit contains only AI-produced code, it is `[ai]`.

---

### `[human + ai]`

Use this tag when:

- AI-generated code was edited by a human
- Human-written code and AI-written code coexist
- The final result is a collaborative artifact

This includes:
- fixing AI output
- refactoring generated code
- extending AI-written code manually

---

## What does *not* count as code

The following should be committed separately and tagged `[human]`:

- specifications
- design documents
- comments describing intent
- TODOs
- architecture notes

Ideas are important — but ideas are not code.

---

## One tag per commit

Each commit must contain **at most one** classification tag.

If multiple tags are present:
- the commit is considered invalid
- tooling may emit a warning
- results may exclude the commit

---

## Untagged commits

Commits without a recognized tag are:

- not classified
- excluded from percentage calculations
- reported separately as `unclassified`

This is intentional.

Missing data should remain missing.

---

## Why commits, not lines of code

Line counts are:
- language-dependent
- formatting-sensitive
- easy to game
- poor indicators of effort

Commits represent:
- intent
- decisions
- moments in time

This methodology measures **activity and authorship**, not volume.

---

## Limitations

This methodology:

- relies on self-reporting
- does not prevent misuse
- favors discipline over convenience
- trades precision for reproducibility

These trade-offs are explicit and accepted.

---

## Evolution

This methodology is versioned and may evolve as:

- AI tools change
- workflows adapt
- new edge cases emerge

Any changes must preserve:
- auditability
- simplicity
- backward compatibility where possible

---

## Applying this methodology

This methodology is not just a classification system — it is a **workflow discipline**.

Tagging happens **at commit time**, not retroactively.

### Practical implementation

To maintain consistency:

1. **Tag every commit** as you write the commit message
2. **Choose the appropriate tag** based on the definitions above
3. **Commit immediately** after code changes to avoid ambiguity

### Workflow tools

See **`RULES.md`** for operational guidelines when working with AI assistants.

These rules help enforce tagging discipline by:
- automating tag inclusion in commit messages
- reducing friction in the tagging process
- ensuring no commits are left untagged

The methodology defines **what** to measure.
The rules define **how** to measure it consistently.

---

## Final note

If you are not willing to tag your commits,
you are not measuring AI contribution.

And if you are not measuring it,
you probably shouldn't quote percentages.
