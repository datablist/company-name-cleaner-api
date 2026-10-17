"""Clean company names with the Datablist API using requests.

This standalone example submits a small list of company names, waits for the
background task to finish, and reads all pages of results. The HTTP calls and
three-second polling pauses block until they finish.

The API fixes casing and spacing and removes legal suffixes by default. Each
result includes the cleaned name, confidence, status, and credits used.
Set keepLegalSuffix to True in the payload to keep legal suffixes.

Set DATABLIST_API_KEY and run: python sync_requests.py
Edit the companies list at the bottom to try your own names. This example
submits one task of up to 10,000 names. Calls can consume account credits.
"""

import os
import time
import uuid

import requests


def clean_company_names(company_names: list[str], api_key: str) -> list[dict]:
    """Submit one task, wait for it to finish, and return its results."""
    tasks_url = "https://api.datablist.com/v1/enrichments/tasks"
    headers = {"X-API-Key": api_key}
    inputs = [
        {"inputId": f"row-{index}", "data": {"companyName": name}}
        for index, name in enumerate(company_names, start=1)
    ]

    # 1. Submit the company names.
    payload = {
        "enrichmentId": "company-name-cleaner",
        "uniqueId": str(uuid.uuid4()),
        "settings": {"keepLegalSuffix": False},
        "inputs": inputs,
    }
    response = requests.post(tasks_url, headers=headers, json=payload)
    response.raise_for_status()
    task = response.json()
    task_id = task["@id"]
    task_url = f"{tasks_url}/{task_id}"

    # 2. Wait for the background task to finish.
    while task["status"] not in ("completed", "failed", "stopped"):
        time.sleep(3)
        response = requests.get(task_url, headers=headers)
        response.raise_for_status()
        task = response.json()

    if task["status"] != "completed":
        raise RuntimeError(f"Task {task_id} {task['status']}: {task.get('error')}")

    # 3. Read the results, following pagination when needed.
    results = []
    results_url = f"{task_url}/results"
    params = {"limit": 100}
    while True:
        response = requests.get(results_url, headers=headers, params=params)
        response.raise_for_status()
        page = response.json()
        results.extend(page["results"])
        next_cursor = page["nextCursor"]
        if next_cursor is None:
            break
        params["cursor"] = next_cursor

    return results


if __name__ == "__main__":
    api_key = os.environ["DATABLIST_API_KEY"]
    companies = [
        "TRansformFactory Limited",
        "NGF Immobilien GmbH & Co. KG",
        "Lenßen + Partner Immobilien",
        "Studio 54",
        "AT&T",
    ]

    results = clean_company_names(companies, api_key)
    for result in results:
        print(result)
