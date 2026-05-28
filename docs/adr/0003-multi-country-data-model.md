# ADR 0003: Multi-country data model design

## Status
Accepted — 2026-05-27

## Context

Code Syndicate Latam operates commercially in multiple countries (Colombia, Uruguay) and plans geographic expansion starting with Chile (Iteration 2).
The Market Intelligence system must support analysis across multiple markets without requiring architectural changes as new countries are added.

Two design options were considered:

**Option A — Single-country model (Chile-only MVP)**
Build the initial model exclusively for Chile, migrate to multi-country later if needed.

**Option B — Multi-country model from day one**
Design every geographically-sensitive entity with an explicit `country_code` dimension from the start, even if the MVP only ingests data from one country.

The business context that drives this decision:
- Colombia is the primary commercial market (MVP country)
- Chile is the first expansion target (Iteration 2)
- The team already operates across 3 countries
- Adding a country later should require zero refactoring of the data model

## Decision

**Option B — Multi-country model from day one.**

Every geographically-sensitive table in the Bronze, Silver, and Gold layers will include a `country_code` field (ISO 3166-1 alpha-2 standard: CO, CL, UY, etc.) as a required, non-nullable column.

### Implementation rules

**Bronze layer (raw):**
Every raw table ingested from an external source includes two mandatory metadata columns:

| Column | Type | Description |
|--------|------|-------------|
| `country_code` | VARCHAR(2) | ISO country code of the data source |
| `ingested_at` | TIMESTAMP | UTC timestamp of ingestion |
| `source` | VARCHAR(50) | Source system identifier |

**Silver layer (staging):**
All staging models inherit `country_code` from Bronze.
Naming convention: `stg_<source>__<entity>`
Example: `stg_getonboard__jobs`

**Gold layer (marts):**
Dimension and fact tables include `country_code` as a filterable dimension.
Dashboards and ML models can slice by country without model changes.

### Countries supported in MVP

| country_code | Country | Scope |
|-------------|---------|-------|
| CO | Colombia | MVP — primary market |
| CL | Chile | Iteration 2 |

Additional countries (UY, MX, PE, AR) are extensible by configuration, not by code change.

## Consequences

### Positive
- Adding Colombia → Chile requires only a parameter change in the extractor, zero model refactoring
- Dashboards support country filtering from day one
- Data lineage is explicit: every row knows where it came from
- Supports future ML models trained on multi-country data

### Negative
- Slight overhead in every table definition (one extra column)
- Requires discipline: every new table added in future sprints must follow the convention

## References
- Business Context Section 4: Markets and clients
- Business Context Section 4.7: MVP scope
- ADR 0001: Initial tech stack selection
