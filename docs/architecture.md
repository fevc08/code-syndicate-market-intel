# Architecture

## Overview

The project follows a **medallion architecture** (Bronze / Silver / Gold) for data processing. This is the same pattern used in modern data platforms (Databricks, Snowflake, dbt-based stacks).

\`\`\`
┌─────────────────────┐
│  External sources   │   APIs, scraping, public datasets
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Python ingestion   │   src/ingestion/*.py
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Bronze (raw)       │   Raw data, append-only
└──────────┬──────────┘
           │  dbt
           ▼
┌─────────────────────┐
│  Silver (staging)   │   Cleaned, typed, deduplicated
└──────────┬──────────┘
           │  dbt
           ▼
┌─────────────────────┐
│  Gold (marts)       │   Dimensional model for analytics
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Consumption        │   Looker Studio + ML notebooks
└─────────────────────┘
\`\`\`

## Layers

### Bronze — schema `raw`

- Data as it arrives from the source, **without transformations**.
- Append-only: history is never overwritten.
- Metadata tracked: ingestion timestamp, source, raw payload.
- Goal: full traceability and ability to reprocess from source.

### Silver — schema `staging`

- One staging table per raw table.
- Cleaning: correct data types, null handling, deduplication.
- Naming convention: \`stg_<source>__<entity>\` (e.g. \`stg_getonboard__jobs\`).
- Built and tested with **dbt**.

### Gold — schema `marts`

- **Dimensional model**: fact tables and dimension tables.
- Optimized for analytical queries (denormalized where needed).
- Consumed by Looker Studio dashboards and ML pipelines.
- Documented and tested with **dbt**.

## Technology choices

See [ADR 0001](adr/0001-stack-selection.md) for the rationale behind each technology selection.

## Future evolution

The current architecture is intentionally minimal for the MVP. Planned evolutions:

- Add an orchestrator (Airflow or Prefect) once pipelines stabilize.
- Migrate from local PostgreSQL to a cloud warehouse (BigQuery / Snowflake) if data volume grows.
- Introduce a feature store for ML use cases beyond the MVP.
