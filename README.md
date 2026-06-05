# Code Syndicate Latam — Market Intelligence

End-to-end data project for B2B tech consulting market analysis in LATAM. MVP built for Colombia, expanding to Chile and other countries.

## 🎯 Business context

Code Syndicate Latam is a B2B technology consultancy operating across LATAM. This project provides the market intelligence required to define its commercial strategy: customer segmentation, service demand analysis, pricing benchmarks, and tech skills trends — starting with Colombia (MVP) and expanding to Chile and other LATAM markets.

## 🛠️ Tech stack

| Layer | Tool |
|-------|------|
| Language | Python 3.10 |
| Database | PostgreSQL 16 |
| Transformation | dbt |
| Machine Learning | Scikit-learn |
| Visualization | Looker Studio |
| Version control | Git + GitHub |
> Developed and tested on PostgreSQL 16.

## 🏛️ Architecture

The project follows a **medallion architecture** with three layers:

- **Bronze (`raw`)** — Raw data as ingested from sources, append-only.
- **Silver (`staging`)** — Cleaned and typed data.
- **Gold (`marts`)** — Dimensional model optimized for analytics.

See [docs/architecture.md](docs/architecture.md) for details.

## 📁 Project structure

```
.
├── docs/                    # Documentation and ADRs
│   ├── adr/                 # Architecture Decision Records (5)
│   └── img/                 # Diagrams and images
├── src/                     # Production Python code
│   ├── ingestion/           # Data extractors
│   │   ├── get_on_board.py  # Get on Board API extractor
│   │   └── README.md        # Ingestion module docs
│   └── utils/               # Shared utilities
│       ├── config.py        # Environment configuration
│       └── db.py            # PostgreSQL connection
├── notebooks/               # Exploratory analysis
│   └── explore_api.py       # API exploration script
├── tests/                   # Automated tests
├── data/                    # Local data (gitignored)
├── requirements.txt         # Python dependencies
└── .env.example             # Environment variables template
```

## 🚀 Local setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Git

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/fevc08/code-syndicate-market-intel.git
   cd code-syndicate-market-intel
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your real credentials
   ```

5. Create the PostgreSQL database and schemas. Follow the guide at [docs/setup-database.md](docs/setup-database.md).

## 📊 Project status

🟠 **In progress** — Sprint 2 complete: Bronze ingestion layer live

**What's working:**
- Get on Board API extractor (Colombia)
- 130 job postings ingested, 5,832 skill tags loaded
- 33 companies profiled with buyer data
- Full Bronze layer: 6 tables, 8 indexes

**Next:** Sprint 3 — Silver layer with dbt transformations

## 📐 Architecture decisions

All architectural decisions are documented as ADRs in [docs/adr/](docs/adr/).

- [ADR 0001 — Initial tech stack selection](docs/adr/0001-stack-selection.md)
- [ADR 0002 — Temporary acceptance of Python 3.10](docs/adr/0002-python-version.md)
- [ADR 0003 — Multi-country data model design](docs/adr/0003-multi-country-data-model.md)
- [ADR 0004 — API integration policy and rate limiting](docs/adr/0004-api-integration-policy.md)
- [ADR 0005 — Data source selection: Get on Board](docs/adr/0005-data-source-selection-getonboard.md)

## 👤 Author

Built by Fidel Vera Chourio — Data Analyst & Data Engineer.
