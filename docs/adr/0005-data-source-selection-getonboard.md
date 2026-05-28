# ADR 0005: Data source selection — Get on Board public API

## Status
Accepted — 2026-05-27

## Context

The Market Intelligence system requires a primary data source for job market analysis in Colombia, covering three service verticals of Code Syndicate Latam:
- Product Lab / Odoo (ERP implementation)
- Ciberseguridad (cybersecurity services)
- Arquitectura Cloud (cloud architecture consulting)

Four candidate sources were evaluated before making this decision.

## Candidates evaluated

### Candidate A — Get on Board (public API)
LATAM-focused tech job platform.
Public API available at https://www.getonbrd.com/api/v0
No authentication required.

### Candidate B — Trabajando.com / Laborum
Large generalist job portals in Colombia.
No public API. Anti-scraping measures active (Cloudflare, JavaScript rendering).
Would require Selenium/Playwright.

### Candidate C — datos.gov.co
Colombian government open data portal.
Real documented API, free, no restrictions.
Contains company registry data, not job postings.
Relevant as complementary source, not primary.

### Candidate D — LinkedIn Jobs
Largest job dataset in LATAM.
Official API restricted and expensive.
Aggressive anti-scraping measures.
Terms of Use prohibit unauthorized data collection.
Risk: account blocking, legal exposure.

## Decision

**Candidate A — Get on Board public API.**

### Justification

**1. Legal and ethical compliance**
Pre-Sprint 2.1 investigation confirmed:
- HTML scraping of Get on Board violates their Terms of Use explicitly
  (sections ii, v, vi of their agreement)
- The public API is the authorized access method
- Using the API is the only compliant option among sources with job posting data

**2. Technical fitness**
The public API provides structured JSON data covering all entities needed for the analysis:

| Endpoint | Use in this project |
|----------|---------------------|
| `GET /api/v0/search/jobs` | Primary fact table: job postings |
| `GET /api/v0/companies` | Dimension: companies + buyer profiling |
| `GET /api/v0/tags` | Dimension: skills demanded per vertical |
| `GET /api/v0/seniorities` | Dimension: seniority levels |
| `GET /api/v0/cities` | Dimension: geographic distribution |
| `GET /api/v0/regions` | Dimension: regional aggregation |
| `GET /api/v0/countries` | Dimension: country reference |
| `GET /api/v0/industries` | Dimension: industry classification |
| `GET /api/v0/headcounts` | Dimension: company size |
| `GET /api/v0/modalities` | Dimension: employment modality |
| `GET /api/v0/insights/{id}` | Supplementary: market benchmarks |

**3. LATAM coverage**
Get on Board covers Colombia, Chile, and other LATAM markets in a single API.
This directly supports the multi-country architecture defined in ADR 0003:
- MVP: Colombia (`country_code = CO`)
- Iteration 2: Chile (`country_code = CL`)
No source change required between iterations.

**4. Data quality**
Job postings on Get on Board are tech-focused, reducing noise from non-relevant sectors.
Company profiles are structured and maintained by the companies themselves.

## Search strategy by vertical

The `/search/jobs` endpoint supports keyword search.
The following keywords will be used to filter
job postings relevant to each Code Syndicate vertical:

### Product Lab / Odoo
**Primary keywords:**
`Odoo`, `ERP`, `SAP`

**Secondary keywords:**
`Salesforce`, `HubSpot`, `CRM`,
`implementación ERP`, `transformación digital`,
`digitalización`

**Rationale:**
Code Syndicate targets the mid-market ERP segment where SAP is too expensive and Odoo is the cost-effective alternative. Salesforce and HubSpot signal companies investing in business digitalization, a related buyer profile.

---

### Ciberseguridad
**Primary keywords:**
`ciberseguridad`, `cybersecurity`, `seguridad informática`, `pentesting`, `penetration testing`, `Zero Trust`, `DevSecOps`

**Regulatory signal keywords:**
`ISO 27001`, `SOC 2`, `GDPR`, `PCI-DSS`, `Ley 1581`, `SFC`, `compliance`

**Rationale:**
Regulatory keywords identify companies under compliance pressure — the highest-propensity buyers for cybersecurity services.
International frameworks (SOC 2, GDPR) signal companies with global operations and higher security budgets.

---

### Arquitectura Cloud
**Primary keywords:**
`AWS`, `GCP`, `Azure`, `cloud`, `arquitectura cloud`, `cloud architecture`

**Infrastructure keywords:**
`Terraform`, `Kubernetes`, `Docker`, `serverless`, `microservicios`, `DevOps`, `infraestructura como código`

**Certification keywords:**
`AWS Solutions Architect`, `GCP Professional`, `Azure Architect`

**Rationale:**
Certification mentions signal companies with mature cloud investment.
Infrastructure-as-code keywords identify companies in cloud modernization phases — the primary buyer profile for cloud architecture consulting.

## Endpoints excluded from MVP scope

| Endpoint | Reason for exclusion |
|----------|---------------------|
| `GET /api/v0/perks` | Benefits data not relevant to commercial decisions |
| `GET /api/v0/categories` | Redundant with `/tags` for our use case |
| Private API endpoints | Require paid subscription, out of budget |

## Complementary sources (future iterations)

| Source | Iteration | Purpose |
|--------|-----------|---------|
| `datos.gov.co` | Iteration 2 | Company registry enrichment for buyer profiling |
| `datos.gob.cl` | Iteration 2 | Chilean company data when Chile scope opens |
| LinkedIn (if API becomes accessible) | Iteration 3+ | Broader market validation |

## Consequences

### Positive
- Zero legal/ethical risk: using authorized API
- Structured JSON eliminates HTML parsing complexity
- Single source covers Colombia + Chile + other LATAM markets (supports ADR 0003)
- Reference endpoints provide pre-normalized dimensions (no manual taxonomy needed)
- Search strategy directly maps to Code Syndicate's three MVP verticals

### Negative
- Get on Board covers tech-focused companies primarily. Traditional industries (manufacturing, retail) adopting Odoo may be underrepresented
- No salary data guaranteed: many postings omit compensation ranges (documented in Business Context R7)
- Dependency on a single source (mitigated by complementary sources in roadmap)

## References
- Business Context Section 6: Business questions (P4-P15, search strategy per vertical)
- Business Context Section 7: R5, R7, Restriction 2
- ADR 0003: Multi-country data model design
- ADR 0004: API integration policy and rate limiting
- Pre-Sprint 2.1 investigation findings (robots.txt, Terms of Use, API documentation)
