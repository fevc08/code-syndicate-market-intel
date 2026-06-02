# notebooks/explore_api.py
"""
API exploration script for Get on Board public API.
NOT production code — used for understanding API behavior.
Run from project root: python3 notebooks/explore_api.py
"""

import time
import json
import requests
from src.utils.config import config

BASE_URL = "https://www.getonbrd.com/api/v0"


def make_request(endpoint: str, params: dict = None) -> dict:
    """
    Makes a single GET request to the Get on Board API.
    Applies rate limiting as per ADR 0004.
    Returns the parsed JSON response.
    """
    url = f"{BASE_URL}/{endpoint}"
    headers = {"User-Agent": config.user_agent}

    # Esperá rate_limit_seconds antes de cada request (ADR 0004)
    time.sleep(config.rate_limit_seconds)

    response = requests.get(url, headers=headers, params=params)

    # Lanzá un error si el status code no es 2xx
    response.raise_for_status()

    return response.json()


def explore_seniorities():
    """Explore the seniorities endpoint."""
    print("\n=== SENIORITIES ===")
    data = make_request("seniorities")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def explore_jobs_sample():
    """Explore a small sample of jobs from Colombia."""
    print("\n=== JOBS SAMPLE (Colombia, 3 results) ===")
    data = make_request("search/jobs", params={"country_code": "co", "per_page": 3})
    print(f"Total pages: {data['meta']['total_pages']}")
    print(f"Total per page: {data['meta']['per_page']}")
    for job in data["data"]:
        attrs = job["attributes"]
        print(f"    - {attrs['title']}")
        print(f"    company_id: {attrs['company']['data']['id']}")
        print(f"    tags count: {len(attrs['tags']['data'])}")

def explore_pagination():
    """Understand pagination behavior."""
    print("\n=== PAGINATION TEST ===")
    page1 = make_request("search/jobs", params={"country_code": "co", "per_page": 2, "page": 1})
    page2 = make_request("search/jobs", params={"country_code": "co", "per_page": 2, "page": 2})
    
    print("Page 1 jobs:")
    for job in page1["data"]:
        print(f"    - {job['attributes']['title']}")

    print("Page 2 jobs:")
    for job in page2["data"]:
        print(f"    - {job['attributes']['title']}")
    
    ids_page1 = {job["id"] for job in page1["data"]}
    ids_page2 = {job["id"] for job in page2["data"]}
    overlap = ids_page1.intersection(ids_page2)
    print(f"Overlap between page 1 and 2: {len(overlap)} (should be 0)")

if __name__ == "__main__":
    print("Starting API exploration...")
    print(f"Rate limit: {config.rate_limit_seconds}s between requests")

    explore_seniorities()
    explore_jobs_sample()
    explore_pagination()

    print("\n✅ Exploration complete")