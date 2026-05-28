# ADR 0004: API integration policy and rate limiting

## Status
Accepted — 2026-05-27

## Context

The Market Intelligence system ingests data from Get on Board's public API (api/v0).
This API is free, requires no authentication, and has no explicitly documented rate limits.

Before writing any ingestion code, we need to define a responsible usage policy that:
1. Respects the API provider's infrastructure
2. Avoids IP blocking or service disruption
3. Is documented and auditable
4. Serves as a template for future API integrations

### Why this ADR exists

The previous investigation (pre-Sprint 2.1) confirmed:
- Scraping Get on Board HTML violates their Terms of Use
- The public API is the authorized access method
- Rate limits are not documented explicitly
- The robots.txt signals caution with automated access

When rate limits are undocumented, the responsible approach is to apply conservative self-imposed limits rather than assuming no limits exist.

## Decision

### 1. Rate limiting policy

| Rule | Value | Rationale |
|------|-------|-----------|
| Max requests per second | 1 req/sec | Conservative default for undocumented limits |
| Backoff on HTTP 429 | Exponential: 2s → 4s → 8s → 16s → abort | Standard retry pattern |
| Max retries per request | 3 | Avoid infinite loops |
| Daily request budget | < 5.000 requests | Self-imposed cap for MVP volume |

### 2. Request identification

Every HTTP request made by the system must include an identifying User-Agent header:
**User-Agent:** code-syndicate-market-intel/0.1 (fevera@codesyndicatelatam.com)

**Why this matters:**
If our requests cause any issue on Get on Board's infrastructure, they can contact us directly instead of silently blocking our IP. This is standard professional practice in data engineering.

### 3. Session behavior

- All requests use a persistent `requests.Session()` object (connection reuse, better performance)
- Sessions are closed explicitly after each ingestion run
- No parallel/concurrent requests in MVP (single-threaded ingestion only)

### 4. Error handling policy

| HTTP Status | Action |
|-------------|--------|
| 200 | Process normally |
| 429 Too Many Requests | Exponential backoff + retry |
| 404 Not Found | Log and skip (data may have been removed) |
| 500 Server Error | Exponential backoff + retry (max 3) |
| Other 4xx | Log as warning, skip record, continue |
| Connection timeout | Retry once after 5 seconds, then abort |

### 5. Data freshness policy

For MVP, ingestion runs **manually** (no scheduler).
Target frequency: once per week.

This is explicitly a technical debt item (see Backlog: "Add orchestrator — Airflow or Prefect").
Automated scheduling will be evaluated in a future sprint once the pipeline is stable.

### 6. Compliance statement

This integration uses only the public API endpoints documented at https://www.getonbrd.com/api-doc.html.
No HTML scraping is performed.
No authentication credentials are used or stored.
No data is redistributed publicly.
The data is used exclusively for internal market intelligence purposes by Code Syndicate Latam.

## Consequences

### Positive
- Zero risk of IP blocking with conservative limits
- Identifiable requests build trust with API provider
- Error handling prevents silent data loss
- Policy is reusable as template for future API integrations (datos.gov.co, LinkedIn, etc.)

### Negative
- 1 req/sec means full Colombia ingestion takes several minutes (acceptable for weekly batch)
- Manual execution is not scalable long-term (mitigated by backlog item for orchestrator)

## References
- Business Context Section 7: Risks and restrictions (R5 — API changes, Restriction 2 — rate limiting)
- ADR 0005: Data source selection (Get on Board)
- Pre-Sprint 2.1 investigation findings
