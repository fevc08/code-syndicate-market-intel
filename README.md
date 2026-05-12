# Code Syndicate Latam — Market Intelligence

End-to-end data project for B2B tech consulting market analysis in Chile.

## 🎯 Business context

Code Syndicate Latam is a B2B technology consultancy based in Chile. This project provides the market intelligence required to define its initial commercial strategy: customer segmentation, service demand analysis, pricing benchmarks, and tech skills trends in the Chilean market.

## 🛠️ Tech stack

| Layer | Tool |
|-------|------|
| Language | Python 3.10 |
| Database | PostgreSQL 16 |
| Transformation | dbt |
| Machine Learning | Scikit-learn |
| Visualization | Looker Studio |
| Version control | Git + GitHub |

## 🏛️ Architecture

The project follows a **medallion architecture** with three layers:

- **Bronze (`raw`)** — Raw data as ingested from sources, append-only.
- **Silver (`staging`)** — Cleaned and typed data.
- **Gold (`marts`)** — Dimensional model optimized for analytics.

See [docs/architecture.md](docs/architecture.md) for details.

## 📁 Project structure

\`\`\`
.
├── docs/              # Documentation and ADRs
│   ├── adr/           # Architecture Decision Records
│   └── img/           # Diagrams and images
├── src/               # Production Python code
│   ├── ingestion/     # Data extractors
│   └── utils/         # Shared utilities
├── notebooks/         # Exploratory analysis
├── tests/             # Automated tests
├── data/              # Local data (gitignored)
├── requirements.txt   # Python dependencies
└── .env.example       # Environment variables template
\`\`\`

## 🚀 Local setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Git

### Steps

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/fevc08/code-syndicate-market-intel.git
   cd code-syndicate-market-intel
   \`\`\`

2. Create and activate a virtual environment:
   \`\`\`bash
   python3 -m venv .venv
   source .venv/bin/activate
   \`\`\`

3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Configure environment variables:
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your real credentials
   \`\`\`

5. Create the PostgreSQL database and schemas (see project documentation).

## 📊 Project status

🟡 **In progress** — Sprint 1: Foundation and architecture

## 📐 Architecture decisions

All architectural decisions are documented as ADRs in [docs/adr/](docs/adr/).

- [ADR 0001 — Initial tech stack selection](docs/adr/0001-stack-selection.md)
- [ADR 0002 — Temporary acceptance of Python 3.10](docs/adr/0002-python-version.md)

## 👤 Author

Built by Fidel Vera Chourio — Data Analyst & Data Engineer.
