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

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-commit-audit.git
cd ai-commit-audit

# Install in development mode
pip install -e .

# Or install with dev dependencies for testing
pip install -e ".[dev]"
```

---

## Usage

### Basic usage

Analyze any Git repository (local or remote):

```bash
# Analyze the current repository
python run.py analyze .

# Analyze a specific local repository
python run.py analyze /path/to/your/repo

# Analyze a GitHub repository (clone it first)
git clone https://github.com/username/repo.git
python run.py analyze ./repo
```

### Command-line options

```bash
# Filter by date range
python run.py analyze . --since 2024-01-01 --until 2024-12-31

# Filter by author
python run.py analyze . --author "Your Name"

# Output formats
python run.py analyze . --format table    # default, human-readable
python run.py analyze . --format json     # machine-readable
python run.py analyze . --format csv      # spreadsheet-friendly

# Save to file
python run.py analyze . --format json --out results.json
python run.py analyze . --format csv --out results  # creates results_summary.csv and results_timeline.csv

# Strict mode (fail if untagged commits exist)
python run.py analyze . --strict
```

### Testing with this repository

To test the tool on this repository itself:

```bash
# First, make sure some commits have tags
# Check existing commit messages:
git log --oneline

# Analyze this repository
python run.py analyze .
```

### Testing with a GitHub repository

```bash
# Clone any public GitHub repo
git clone https://github.com/username/repository.git
cd repository

# Go back to ai-commit-audit directory
cd ../ai-commit-audit

# Analyze the cloned repository
python run.py analyze ../repository
```

### Example: Creating tagged commits for testing

If you want to test with properly tagged commits:

```bash
# Create a test repository
mkdir test-repo
cd test-repo
git init

# Create some tagged commits
echo "print('hello')" > test.py
git add test.py
git commit -m "[human] Initial implementation"

echo "# AI generated function" >> test.py
git add test.py
git commit -m "[ai] Add AI-generated helper"

echo "# Manual fix" >> test.py
git add test.py
git commit -m "[human + ai] Refactor AI code with manual edits"

# Now analyze it
cd ../ai-commit-audit
python run.py analyze ../test-repo
```

---

## Status

This project is intentionally minimal.
The methodology comes first; tooling exists to support it.

Contributions and discussion are welcome — especially around edge cases and limitations.
