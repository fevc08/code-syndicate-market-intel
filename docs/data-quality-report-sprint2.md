# Data Quality Report — Sprint 2 Bronze Layer

**Date:** 2026-06-05
**Source:** Get on Board public API v0
**Country:** Colombia (CO)
**Ingestion runs:** 2 (initial + fix for numeric_id)

---

## Summary

| Table | Rows | Notes |
|-------|------|-------|
| raw.jobs | 260 | 130 unique jobs × 2 ingestion runs |
| raw.job_tags | 2,192 | Append-only, mirrors raw.jobs duplication |
| raw.companies | 33 | Unique companies, 100% coverage |
| raw.tags | 5,832 | Full catalog loaded |
| raw.seniorities | 5 | Full catalog loaded |
| raw.modalities | 4 | Full catalog loaded |

---

## Field Coverage — raw.jobs

| Field | Coverage | Notes |
|-------|----------|-------|
| title | 100% | ✅ |
| company_id | 100% | ✅ Integer ID |
| seniority_id | 100% | ✅ |
| modality_id | 100% | ✅ |
| published_at | 100% | ✅ Unix timestamp |
| _search_keyword | 100% | ✅ |
| min_salary | 56.2% | ⚠️ Many postings omit salary |
| max_salary | 56.2% | ⚠️ Many postings omit salary |

---

## Duplicates in raw.jobs

By design, raw.jobs is **append-only**. The same job_id appears
multiple times when:
1. The job matches multiple search keywords
2. The extractor runs multiple times

**Top duplicate example:**
`technical-account-manager-factor-it` appeared 8 times
across keywords: SAP, AWS, GCP, Azure (× 2 runs)

**Silver layer deduplication strategy:**
```sql
SELECT DISTINCT ON (job_id) *
FROM raw.jobs
ORDER BY job_id, _ingested_at DESC
```

---

## Key Market Findings (Colombia, June 2026)

### Demand by vertical (unique keywords)
| Keyword | Jobs |
|---------|------|
| AWS | 55 |
| GCP | 24 |
| Azure | 22 |
| SAP | 17 |
| ERP | 7 |
| ciberseguridad | 3 |
| cybersecurity | 2 |
| Odoo | 0 |
| pentesting | 0 |

### Seniority distribution
| Level | Jobs | % |
|-------|------|---|
| Senior | 82 | 63% |
| Semi Senior | 25 | 19% |
| Expert | 21 | 16% |
| Sin experiencia | 2 | 2% |
| Junior | 0 | 0% |

### Salary coverage
56.2% of job postings include salary range.
Sufficient for approximate pricing benchmarks in Silver layer.

---

## Known Issues

### 1. company_id type mismatch (RESOLVED)
raw.jobs.company_id is INTEGER, raw.companies.id is VARCHAR slug.
**Resolution:** Added numeric_id column to raw.companies.
JOIN: `ON raw.jobs.company_id = raw.companies.numeric_id`

### 2. Tag ID type mismatch (OPEN)
raw.job_tags.tag_id is BIGINT (integer from jobs response),
raw.tags.id is VARCHAR slug.
**Resolution:** To be addressed in Silver layer with mapping table.
See Backlog: "Resolve API inconsistency: tag IDs"

### 3. Duplicate rows from multiple ingestion runs
First run loaded 130 jobs before numeric_id fix.
Second run loaded 130 jobs after fix.
**Resolution:** Silver deduplication will use most recent ingestion.

---

## Next Steps (Sprint 3)

1. Build Silver layer with dbt
2. Deduplicate raw.jobs → stg_getonboard__jobs
3. Resolve tag_id mismatch
4. Parse published_at Unix timestamps to DATE
5. Strip HTML from description/functions/benefits fields
6. Build Gold dimensional model for analytics
