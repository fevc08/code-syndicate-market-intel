# src/ingestion/get_on_board.py
"""
Get on Board API extractor for Code Syndicate Market Intelligence.
Loads job market data from Colombia into the Bronze layer.

Usage:
    python3 -m src.ingestion.get_on_board
"""

import time
import json
import logging
from datetime import datetime, timezone

import requests
from sqlalchemy import text

from src.utils.config import config
from src.utils.db import get_engine

# -------------------------------------------------------
# Logging configuration
# -------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------------------------------------------
# Constants
# -------------------------------------------------------
BASE_URL = "https://www.getonbrd.com/api/v0"
COUNTRY_CODE = "co"
MAX_PER_PAGE = 50

SEARCH_KEYWORDS = [
    "Odoo", "SAP", "ERP",
    "ciberseguridad", "cybersecurity", "pentesting",
    "AWS", "GCP", "Azure",
]


# -------------------------------------------------------
# HTTP layer
# -------------------------------------------------------
def _make_request(endpoint: str, params: dict = None) -> dict:
    """
    Makes a single GET request to the Get on Board API.
    Applies rate limiting per ADR 0004.
    Raises requests.HTTPError on non-2xx responses.
    """
    try:
        url = f"{BASE_URL}/{endpoint}"
        headers = {"User-Agent": config.user_agent}
        time.sleep(config.rate_limit_seconds)
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        logger.error(f"HTTP error on {endpoint}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error on {endpoint}: {e}")
        raise

# -------------------------------------------------------
# Reference data loaders
# -------------------------------------------------------
def _upsert_seniorities(conn) -> int:
    """
    Loads all seniority levels from the API into raw.seniorities.
    Returns the number of records upserted.
    """
    data = _make_request("seniorities")
    count = 0

    for record in data["data"]:
        attrs = record["attributes"]
        conn.execute(text("""
            INSERT INTO raw.seniorities
                (id, name, locale_key, _raw_payload)
            VALUES
                (:id, :name, :locale_key, :raw_payload)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                locale_key = EXCLUDED.locale_key
        """), {
            "id": record["id"],
            "name": attrs["name"],
            "locale_key": attrs.get("locale_key"),
            "raw_payload": json.dumps(record, ensure_ascii=False)
        })
        count += 1

    logger.info(f"Upserted {count} seniorities")
    return count


def _upsert_modalities(conn) -> int:
    """
    Loads all employment modalities from the API into raw.modalities.
    Returns the number of records upserted.
    """

    data = _make_request("modalities")
    count = 0

    for record in data["data"]:
        attrs = record["attributes"]
        conn.execute(text("""
            INSERT INTO raw.modalities
                (id, name, locale_key, _raw_payload)
            VALUES
                (:id, :name, :locale_key, :raw_payload)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                locale_key = EXCLUDED.locale_key
        """), {
            "id": record["id"],
            "name": attrs["name"],
            "locale_key": attrs.get("locale_key"),
            "raw_payload": json.dumps(record, ensure_ascii=False)
        })
        count += 1

    logger.info(f"Upserted {count} modalities")
    return count


def _upsert_tags(conn) -> int:
    """
    Loads all skill tags from the API into raw.tags.
    Handles pagination (~1169 pages with per_page=5,
    but ~59 pages with per_page=100).
    Returns the total number of records upserted.
    """
    total = 0
    page = 1

    while True:
        data = _make_request("tags", params={"per_page": 100, "page": page})
        records = data["data"]

        if not records:
            break

        for record in records:
            attrs = record["attributes"]
            conn.execute(text("""
                INSERT INTO raw.tags
                    (id, name, keywords, _raw_payload)
                VALUES
                    (:id, :name, :keywords, :raw_payload)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    keywords = EXCLUDED.keywords
            """), {
                "id": record["id"],
                "name": attrs["name"],
                "keywords": attrs.get("keywords"),
                "raw_payload": json.dumps(record, ensure_ascii=False)
            })
            total += 1

        meta = data["meta"]
        logger.info(
            f"Tags: page {page}/{meta['total_pages']} "
            f"({total} records so far)"
        )

        if page >= meta["total_pages"]:
            break

        page += 1

    logger.info(f"Upserted {total} tags total")
    return total

# -------------------------------------------------------
# Job data loaders
# -------------------------------------------------------
def _upsert_company(conn, company_data: dict, numeric_id: int = None) -> None:
    """
    Inserts or updates a company record in raw.companies.
    numeric_id: the integer ID used to query the API (from raw.jobs).
    """
    conn.execute(text("""
        INSERT INTO raw.companies
            (id, name, description, long_description,
             web, twitter, github, facebook, angellist,
             country_code, response_time_in_days, logo,
             numeric_id, _raw_payload)
        VALUES
            (:id, :name, :description, :long_description,
             :web, :twitter, :github, :facebook, :angellist,
             :country_code, :response_time_in_days, :logo,
             :numeric_id, :raw_payload)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            description = EXCLUDED.description,
            web = EXCLUDED.web,
            country_code = EXCLUDED.country_code,
            numeric_id = EXCLUDED.numeric_id
    """), {
        "id": company_data["id"],
        "name": company_data["attributes"].get("name"),
        "description": company_data["attributes"].get("description"),
        "long_description": company_data["attributes"].get("long_description"),
        "web": company_data["attributes"].get("web"),
        "twitter": company_data["attributes"].get("twitter"),
        "github": company_data["attributes"].get("github"),
        "facebook": company_data["attributes"].get("facebook"),
        "angellist": company_data["attributes"].get("angellist"),
        "country_code": company_data["attributes"].get("country"),
        "response_time_in_days": json.dumps(
            company_data["attributes"].get("response_time_in_days")
        ),
        "logo": json.dumps(company_data["attributes"].get("logo")),
        "numeric_id": numeric_id,
        "raw_payload": json.dumps(company_data, ensure_ascii=False)
    })


def _insert_job(conn, job: dict, keyword: str) -> None:
    """
    Inserts a job record into raw.jobs.
    Bronze is append-only: no ON CONFLICT here.
    job: full job dict from the API (including id and attributes).
    keyword: the search keyword that returned this job.
    """
    attrs = job["attributes"]

    conn.execute(text("""
        INSERT INTO raw.jobs (
            job_id, title, category_name,
            description, functions, benefits,
            desirable, projects,
            remote, remote_modality, remote_zone,
            countries, lang, response_time_in_days,
            location_cities,
            min_salary, max_salary, applications_count,
            published_at,
            company_id, seniority_id, modality_id, tags,
            country_code, _search_keyword, _raw_payload
        ) VALUES (
            :job_id, :title, :category_name,
            :description, :functions, :benefits,
            :desirable, :projects,
            :remote, :remote_modality, :remote_zone,
            :countries, :lang, :response_time_in_days,
            :location_cities,
            :min_salary, :max_salary, :applications_count,
            :published_at,
            :company_id, :seniority_id, :modality_id, :tags,
            :country_code, :search_keyword, :raw_payload
        )
    """), {
        "job_id": job["id"],
        "title": attrs.get("title"),
        "category_name": attrs.get("category_name"),
        "description": attrs.get("description"),
        "functions": attrs.get("functions"),
        "benefits": attrs.get("benefits"),
        "desirable": attrs.get("desirable"),
        "projects": attrs.get("projects"),
        "remote": attrs.get("remote"),
        "remote_modality": attrs.get("remote_modality"),
        "remote_zone": attrs.get("remote_zone"),
        "countries": json.dumps(attrs.get("countries")),
        "lang": attrs.get("lang"),
        "response_time_in_days": json.dumps(
            attrs.get("response_time_in_days")
        ),
        "location_cities": json.dumps(
            attrs.get("location_cities")
        ),
        "min_salary": attrs.get("min_salary"),
        "max_salary": attrs.get("max_salary"),
        "applications_count": attrs.get("applications_count"),
        "published_at": attrs.get("published_at"),
        "company_id": attrs["company"]["data"]["id"]
            if attrs.get("company") and attrs["company"].get("data")
            else None,
        "seniority_id": str(attrs["seniority"]["data"]["id"])
            if attrs.get("seniority") and attrs["seniority"].get("data")
            else None,
        "modality_id": attrs["modality"]["data"]["id"]
            if attrs.get("modality") and attrs["modality"].get("data")
            else None,
        "tags": json.dumps(attrs.get("tags")),
        "country_code": COUNTRY_CODE.upper(),
        "search_keyword": keyword,
        "raw_payload": json.dumps(job, ensure_ascii=False)
    })


def _insert_job_tags(conn, job_id: str, tags_data: list) -> int:
    """
    Inserts one row per tag into raw.job_tags.
    tags_data: the list from job["attributes"]["tags"]["data"]
    Returns the number of tags inserted.
    """
    count = 0
    for tag in tags_data:
        conn.execute(text("""
            INSERT INTO raw.job_tags
                (job_id, tag_id, country_code)
            VALUES
                (:job_id, :tag_id, :country_code)
        """), {
            "job_id": job_id,
            "tag_id": tag["id"],
            "country_code": COUNTRY_CODE.upper()
        })
        count += 1
    return count

# -------------------------------------------------------
# Orchestration
# -------------------------------------------------------
def _extract_keyword(conn, keyword: str) -> dict:
    """
    Extracts all job pages for a single search keyword.
    Returns a summary dict with counts.
    """
    logger.info(f"Starting extraction for keyword: '{keyword}'")
    jobs_inserted = 0
    tags_inserted = 0
    companies_loaded = set()
    page = 1

    while True:
        data = _make_request("search/jobs", params={
            "query": keyword,
            "country_code": COUNTRY_CODE,
            "per_page": MAX_PER_PAGE,
            "page": page
        })

        jobs = data["data"]
        meta = data["meta"]

        if not jobs:
            break

        logger.info(
            f"  Keyword '{keyword}': "
            f"page {page}/{meta['total_pages']} "
            f"({len(jobs)} jobs)"
        )

        for job in jobs:
            attrs = job["attributes"]

            # Cargar la empresa si no la cargamos todavía
            company_data = attrs.get("company", {}).get("data")
            if company_data:
                company_id = company_data["id"]
                if company_id not in companies_loaded:
                    company_detail = _make_request(f"companies/{company_id}")
                    if "data" in company_detail:
                        _upsert_company(conn, company_detail["data"], numeric_id=company_id)
                        companies_loaded.add(company_id)

            # Insertar el job
            _insert_job(conn, job, keyword)
            jobs_inserted += 1

            # Insertar los tags del job
            tags_data = attrs.get("tags", {}).get("data", [])
            tags_inserted += _insert_job_tags(conn, job["id"], tags_data)

        if page >= meta["total_pages"]:
            break

        page += 1

    summary = {
        "keyword": keyword,
        "jobs_inserted": jobs_inserted,
        "tags_inserted": tags_inserted,
        "companies_loaded": len(companies_loaded)
    }
    logger.info(f"Keyword '{keyword}' done: {summary}")
    return summary


def run() -> None:
    """
    Main entry point for the Get on Board extractor.
    Loads reference data and then extracts jobs for all keywords.
    """
    start_time = datetime.now(timezone.utc)
    logger.info("=" * 60)
    logger.info("Get on Board extractor started")
    logger.info(f"Country: {COUNTRY_CODE.upper()}")
    logger.info(f"Keywords: {SEARCH_KEYWORDS}")
    logger.info("=" * 60)

    engine = get_engine()

    with engine.begin() as conn:
        # 1. Cargar catálogos de referencia
        logger.info("Loading reference catalogs...")
        _upsert_seniorities(conn)
        _upsert_modalities(conn)
        _upsert_tags(conn)

        # 2. Extraer jobs por keyword
        logger.info("Starting job extraction...")
        total_jobs = 0
        total_tags = 0

        for keyword in SEARCH_KEYWORDS:
            summary = _extract_keyword(conn, keyword)
            total_jobs += summary["jobs_inserted"]
            total_tags += summary["tags_inserted"]

    elapsed = (datetime.now(timezone.utc) - start_time).seconds
    logger.info("=" * 60)
    logger.info("Extraction complete")
    logger.info(f"Total jobs inserted: {total_jobs}")
    logger.info(f"Total job_tags inserted: {total_tags}")
    logger.info(f"Elapsed time: {elapsed}s")
    logger.info("=" * 60)


if __name__ == "__main__":
    run()