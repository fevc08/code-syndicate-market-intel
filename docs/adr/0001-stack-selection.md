# ADR 0001: Initial tech stack selection

## Status
Accepted — 2026-05-11

## Context

We need to define the initial technology stack for the Code Syndicate Latam Market Intelligence project. The constraints are:

- Single developer with a Junior profile, learning while building
- Zero budget: only open-source tools or free tiers
- The project must serve a dual purpose:
  1. Real business intelligence for Code Syndicate Latam's commercial strategy
  2. Technical portfolio for job applications in the Chilean market
- Focus on tools with high market demand in Chilean job postings

## Decision

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Language | **Python** | Mature data ecosystem; high demand in Chilean job postings |
| Database | **PostgreSQL** | Free, production-grade, transferable to any cloud later |
| Transformation | **dbt** | Industry standard in Analytics Engineering |
| Machine Learning | **Scikit-learn** | Sufficient for planned use cases; no overhead |
| Visualization | **Looker Studio** | Free, easy public sharing for portfolio |
| Version control | **Git + GitHub** | Industry standard; portfolio visibility |

## Consequences

### Positive
- 100% free stack
- All tools have high demand in Chilean job postings
- Fully reproducible locally without cloud dependencies
- No vendor lock-in

### Negative
- Local PostgreSQL does not scale like BigQuery or Snowflake (acceptable for expected MVP volume)
- No orchestrator (Airflow, Prefect) in MVP scope; manual or `cron`-based execution
- Looker Studio has limitations vs Power BI/Tableau for complex visualizations

## Alternatives considered

- **BigQuery / Snowflake**: rejected for MVP due to cost and over-engineering for current data volume.
- **Airflow**: rejected for MVP; complexity not justified for a single-developer project at this stage.
- **Pandas-only pipeline (no dbt)**: rejected; dbt provides testing, documentation, and lineage that align with industry practices.
