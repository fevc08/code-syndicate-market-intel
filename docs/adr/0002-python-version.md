# ADR 0002: Temporary acceptance of Python 3.10

## Status
Accepted — 2026-05-11
Review at: end of Sprint 6 (MVP completion)

## Context

The local development environment has Python 3.10.20 installed by default on Ubuntu.

The industry-recommended standard for new projects in 2026 is Python 3.11 or 3.12, because of:

- Significant interpreter performance improvements introduced in 3.11
- Improved error messages
- Python 3.10 reaches end-of-life in October 2026

Upgrading requires installing `pyenv` and managing multiple Python versions, which adds ~45 minutes to Sprint 1 and additional learning complexity for a Junior developer.

## Decision

Keep Python 3.10.20 during the MVP phase of the project (Sprints 1–6).

Dependencies in `requirements.txt` use flexible version ranges (`>=X.Y,<Z.0`) to ensure compatibility without strict pinning.

## Consequences

### Positive
- Immediate MVP progress without setup overhead
- Focus on Sprint 1's primary objective: architecture and repository setup

### Negative
- Some modern libraries may require Python 3.11+ in the future (low risk in MVP)
- Loss of Python 3.11+ performance improvements
- Explicit technical debt that must be resolved before October 2026

## Mitigation plan

At the end of Sprint 6 (MVP completion), install `pyenv`, migrate to Python 3.12, regenerate the virtual environment, and validate all dependencies. Document the migration in a new ADR.

## References
- [ADR 0001 — Initial tech stack selection](0001-stack-selection.md)
- Python 3.10 end-of-life: October 2026
