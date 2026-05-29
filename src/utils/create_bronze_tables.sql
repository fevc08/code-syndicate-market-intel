-- ========================================================
-- Bronze Layer DDL
-- Code Syndicate Latam — Market Intelligence
-- Source: Get on Board public API v0
-- Created: 2026-05-29
-- ========================================================
-- --------------------------------------------------------
-- Tabla: raw.seniorities
-- Fuente: GET /api/v0/seniorities
-- Estrategia: full refresh
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw.seniorities (
    -- Business columns
    id VARCHAR(10) NOT NULL,
    name VARCHAR(50) NOT NULL,
    locale_key VARCHAR(50),

    -- Metadata columns
    _ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    _source VARCHAR(50) NOT NULL DEFAULT 'getonboard_api',
    _raw_payload JSONB,

    -- Constraint
    CONSTRAINT pk_raw_seniorities PRIMARY KEY (id)
);

-- --------------------------------------------------------
-- Tabla: raw.modalities
-- Fuente: GET /api/v0/modalities
-- Estrategia: full refresh
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw.modalities (
    id VARCHAR(10) NOT NULL,
    name VARCHAR(200) NOT NULL,
    locale_key VARCHAR(50),
    _ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    _source VARCHAR(50) NOT NULL DEFAULT 'getonboard_api',
    _raw_payload JSONB,
    CONSTRAINT pk_raw_modalities PRIMARY KEY (id)
);

-- --------------------------------------------------------
-- Tabla: raw.tags
-- Fuente: GET /api/v0/tags
-- Estrategia: Incremental upsert
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw.tags (
    id VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    keywords TEXT,
    _ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    _source VARCHAR(50) NOT NULL DEFAULT 'getonboard_api',
    _raw_payload JSONB,
    CONSTRAINT pk_raw_tags PRIMARY KEY (id)
);

-- --------------------------------------------------------
-- Tabla: raw.companies
-- Fuente: GET /api/v0/companies
-- Estrategia: Incremental upsert
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw.companies (
    id VARCHAR(200) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    long_description TEXT,
    projects TEXT,
    benefits TEXT,
    web VARCHAR(500),
    twitter VARCHAR(500),
    github VARCHAR(500),
    facebook VARCHAR(500),
    angellist VARCHAR(500),
    country_code CHAR(2), -- Nombre original en API: "country", renombrado a "country_code" para consistencia con ADR 0003
    response_time_in_days JSONB,
    logo JSONB,
    _ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    _source VARCHAR(50) NOT NULL DEFAULT 'getonboard_api',
    _raw_payload JSONB,
    CONSTRAINT pk_raw_companies PRIMARY KEY (id)
);

-- --------------------------------------------------------
-- Tabla: raw.jobs
-- Fuente: GET /api/v0/jobs
-- Estrategia: append-only
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw.jobs (
    job_id VARCHAR(200) NOT NULL,
    title VARCHAR(200) NOT NULL,
    category_name VARCHAR(200),
    description TEXT,
    functions TEXT,
    benefits TEXT,
    desirable TEXT,
    projects TEXT,
    remote BOOLEAN,
    remote_modality VARCHAR(50),
    remote_zone VARCHAR(50),
    countries JSONB,
    lang VARCHAR(50),
    response_time_in_days JSONB,
    location_cities JSONB,
    min_salary NUMERIC,
    max_salary NUMERIC,
    applications_count INTEGER,
    published_at BIGINT,
    -- Relaciones con otras tablas
    company_id INTEGER,
    seniority_id INTEGER,
    modality_id INTEGER,
    tags JSONB, -- Almacena un array de IDs de tags relacionados
    -- Columnas de Metadata
    _id BIGSERIAL, -- Surrogate key para tracking interno, no es la clave primaria de la tabla
    country_code CHAR(2), -- ADR 0003
    _ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    _source VARCHAR(50) NOT NULL DEFAULT 'getonboard_api',
    _search_keyword VARCHAR(200), -- Campo adicional para facilitar búsquedas y análisis de texto
    _raw_payload JSONB,
    -- Constraints
    CONSTRAINT pk_raw_jobs PRIMARY KEY (_id)
);

-- --------------------------------------------------------
-- Tabla: raw.job_tags
-- Fuente: Derivada de raw.jobs.tags
-- Estrategia: Append-only, con procesamiento incremental para evitar duplicados
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw.job_tags (
    job_id VARCHAR(200) NOT NULL,
    tag_id BIGINT NOT NULL,
    _id BIGSERIAL, -- Surrogate key para tracking interno
    country_code CHAR(2), -- ADR 0003
    _ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    _source VARCHAR(50) NOT NULL DEFAULT 'getonboard_api',
    -- Constraints
    CONSTRAINT pk_raw_job_tags PRIMARY KEY (_id)
);

-- ===========================================
-- Indexes
-- ===========================================

CREATE INDEX IF NOT EXISTS idx_raw_jobs_job_id
    ON raw.jobs (job_id);

CREATE INDEX IF NOT EXISTS idx_raw_jobs_country_code
    ON raw.jobs (country_code);

CREATE INDEX IF NOT EXISTS idx_raw_jobs_company_id
    ON raw.jobs (company_id);

CREATE INDEX IF NOT EXISTS idx_raw_jobs_ingested_at
    ON raw.jobs (_ingested_at);

CREATE INDEX IF NOT EXISTS idx_raw_jobs_keyword
    ON raw.jobs (_search_keyword);

CREATE INDEX IF NOT EXISTS idx_raw_job_tags_job_id
    ON raw.job_tags (job_id);

CREATE INDEX IF NOT EXISTS idx_raw_job_tags_tag_id
    ON raw.job_tags (tag_id);

CREATE INDEX IF NOT EXISTS idx_raw_companies_country
    ON raw.companies (country_code);